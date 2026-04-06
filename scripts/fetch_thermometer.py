#!/usr/bin/env python3
"""
知行温度计数据解析脚本

数据来源: 有知有行 (youzhiyouxing.cn)
用途: 从 Markdown 文本中解析 A 股全市场温度及主要指数估值数据

使用方法:
    # 方式1: 从 stdin 接收 Markdown 文本（配合 webReader 使用）
    echo "$MARKDOWN" | python3 fetch_thermometer.py

    # 方式2: 直接传入文件
    python3 fetch_thermometer.py --file thermometer.md

    # 输出选项:
    python3 fetch_thermometer.py --json       # 仅 JSON 格式
    python3 fetch_thermometer.py --advice     # 仅投资建议报告
    python3 fetch_thermometer.py --version    # 版本信息
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import warnings
from datetime import datetime
from typing import Optional

__version__ = "1.0.0"
__all__ = ["parse_temperature", "generate_advice", "get_band", "get_index_advice"]


# ---------------------------------------------------------------------------
# 类型定义
# ---------------------------------------------------------------------------

class IndexEntry(dict):
    """单条指数数据"""
    name: str
    code: str
    temperature: int
    intrinsic_yield: Optional[str]
    dividend_yield: Optional[str]
    band: str


class MarketSummary(dict):
    """全市场温度摘要"""
    temperature: int
    band: str
    trend: str


class MacroData(dict):
    """宏观经济数据"""
    bond_temperature: Optional[int]
    treasury_10y: Optional[str]
    treasury_10y_date: Optional[str]
    gdp_growth: Optional[str]
    gdp_date: Optional[str]
    cpi_growth: Optional[str]
    cpi_date: Optional[str]


# ---------------------------------------------------------------------------
# 预编译正则
# ---------------------------------------------------------------------------

_RE_UPDATE_TIME = re.compile(
    r"温度更新时间[：:]\s*(\d{4}年\d{1,2}月\d{1,2}日\s*\d{1,2}:\d{2})"
)

_RE_MARKET_TEMP = re.compile(
    r"全市场温度.*?(\d{1,3})°.*?(低估|中估|高估).*?(温度上升|温度下降)",
    re.DOTALL,
)

_RE_MARKET_TEMP_SIMPLE = re.compile(r"(\d{1,3})°\s*\n\s*(低估|中估|高估)")

_RE_INDEX_ROW = re.compile(
    r"\|\s*([^|]*?)\s+([A-Za-z]?\d{5,6}\.(?:SH|SZ|CSI))\s*\|\s*(\d{1,3})°"
    r"\s*\|\s*([^|]*)\s*\|\s*([^|]*)\s*\|"
)

_RE_CJK_START = re.compile(r"^[\u4e00-\u9fff\w]")

_HEADER_KEYWORDS = frozenset(["指数名称", "指数温度", "内在收益率", "股息率", "---"])

_RE_BOND_TEMP = re.compile(r"债市温度\s*\n\s*(\d{1,3})°")
_RE_TREASURY = re.compile(r"10年期国债到期收益率\s*\n\s*([\d.]+%)")
_RE_TREASURY_DATE = re.compile(
    r"10年期国债.*?[\d.]+%\s*\n+(?:\n+)?\s*(\d{4}年\d{1,2}月\d{1,2}日)", re.DOTALL
)
_RE_GDP = re.compile(r"GDP季度同比增速\s*\n\s*([\d.]+%)")
_RE_GDP_DATE = re.compile(
    r"GDP季度同比增速.*?[\d.]+%\s*\n+(?:\n+)?\s*(\d{4}年\d{1,2}季度)", re.DOTALL
)
_RE_CPI = re.compile(r"CPI月度同比增速\s*\n\s*([\d.]+%)")
_RE_CPI_DATE = re.compile(
    r"CPI月度同比增速.*?[\d.]+%\s*\n+(?:\n+)?\s*(\d{4}年\d{1,2}月)", re.DOTALL
)

# 期望解析到的指数名称集合，用于数据质量校验
_EXPECTED_INDICES = frozenset([
    "800消费", "中国互联网", "全指医药", "中证养老", "中证红利",
    "沪深300", "中证1000", "上证50", "创业板指", "中证2000",
    "中证500", "全指信息",
])


# ---------------------------------------------------------------------------
# 辅助函数
# ---------------------------------------------------------------------------

def _safe_int(match, group: int = 1) -> Optional[int]:
    """安全地从正则匹配中提取整数"""
    if match:
        try:
            return int(match.group(group))
        except (ValueError, IndexError):
            pass
    return None


def _extract_str(match, group: int = 1) -> Optional[str]:
    """安全地从正则匹配中提取字符串"""
    if match:
        try:
            return match.group(group).strip()
        except IndexError:
            pass
    return None


# ---------------------------------------------------------------------------
# 核心解析
# ---------------------------------------------------------------------------

def parse_temperature(text: str) -> dict:
    """
    从 Markdown 文本中解析温度计数据。

    Parameters
    ----------
    text : str
        由 webReader 获取的温度计页面 Markdown 内容。

    Returns
    -------
    dict
        包含 market、indices、macro 等字段的结构化数据。
    """
    result = {
        "indices": [],
        "raw_text": text[:5000],
        "fetched_at": datetime.now().isoformat(),
    }

    # 更新时间
    result["update_time"] = _extract_str(_RE_UPDATE_TIME.search(text))

    # ---- 全市场温度 ----
    market_temp = None
    band_text = None
    trend_text = None

    m = _RE_MARKET_TEMP.search(text)
    if m:
        market_temp = _safe_int(m, 1)
        band_text = m.group(2)
        trend_text = "下降" if "下降" in m.group(3) else "上升"

    if market_temp is None:
        m = _RE_MARKET_TEMP_SIMPLE.search(text)
        if m:
            market_temp = _safe_int(m, 1)
            band_text = m.group(2)

    if market_temp is not None:
        result["market"] = {
            "temperature": market_temp,
            "band": band_text or get_band(market_temp),
            "trend": trend_text or "未知",
        }

    # ---- 指数数据 ----
    parsed_names = set()
    for m in _RE_INDEX_ROW.finditer(text):
        name = m.group(1).strip().lstrip("|").strip()
        code = m.group(2).strip()
        if any(kw in name for kw in _HEADER_KEYWORDS):
            continue
        if not _RE_CJK_START.match(name):
            continue
        temp = _safe_int(m, 3)
        if temp is None:
            continue

        intrinsic = m.group(4).strip()
        dividend = m.group(5).strip()

        result["indices"].append({
            "name": name,
            "code": code,
            "temperature": temp,
            "intrinsic_yield": intrinsic if intrinsic and intrinsic != "--" else None,
            "dividend_yield": dividend if dividend and dividend != "--" else None,
            "band": get_band(temp),
        })
        parsed_names.add(name)

    # ---- 宏观数据 ----
    result["macro"] = {
        "bond_temperature": _safe_int(_RE_BOND_TEMP.search(text)),
        "treasury_10y": _extract_str(_RE_TREASURY.search(text)),
        "treasury_10y_date": _extract_str(_RE_TREASURY_DATE.search(text)),
        "gdp_growth": _extract_str(_RE_GDP.search(text)),
        "gdp_date": _extract_str(_RE_GDP_DATE.search(text)),
        "cpi_growth": _extract_str(_RE_CPI.search(text)),
        "cpi_date": _extract_str(_RE_CPI_DATE.search(text)),
    }

    # 数据质量校验
    _validate_result(result, parsed_names)

    return result


def _validate_result(result: dict, parsed_names: set) -> None:
    """对解析结果进行数据质量校验，异常时发出警告"""
    if "market" not in result:
        warnings.warn("未能解析全市场温度数据", UserWarning, stacklevel=3)

    indices = result.get("indices", [])
    if len(indices) < 10:
        warnings.warn(
            f"仅解析到 {len(indices)} 个指数（期望 12 个），数据可能不完整",
            UserWarning,
            stacklevel=3,
        )

    missing = _EXPECTED_INDICES - parsed_names
    if missing:
        warnings.warn(
            f"以下指数未被解析到: {', '.join(sorted(missing))}",
            UserWarning,
            stacklevel=3,
        )

    macro = result.get("macro", {})
    if macro.get("bond_temperature") is None:
        warnings.warn("未能解析债市温度", UserWarning, stacklevel=3)


# ---------------------------------------------------------------------------
# 温度带与建议
# ---------------------------------------------------------------------------

def get_band(temperature: int) -> str:
    """根据温度返回温度带：低估 / 中估 / 高估"""
    if temperature < 30:
        return "低估"
    elif temperature < 70:
        return "中估"
    else:
        return "高估"


def get_index_advice(temperature: int) -> str:
    """根据指数温度给出简短操作建议"""
    if temperature < 15:
        return "积极买入"
    elif temperature < 30:
        return "可以买入"
    elif temperature < 50:
        return "正常定投"
    elif temperature < 70:
        return "适度配置"
    else:
        return "谨慎对待"


def generate_advice(data: dict) -> str:
    """
    根据温度数据生成投资建议报告。

    Parameters
    ----------
    data : dict
        parse_temperature() 的返回值。

    Returns
    -------
    str
        格式化的投资建议文本。
    """
    if "market" not in data:
        return "无法获取市场温度数据，请确认输入内容包含温度计数据。"

    temp = data["market"]["temperature"]
    band = data["market"]["band"]
    trend = data["market"]["trend"]

    lines = [
        "=" * 50,
        "  A股市场温度分析报告",
        "=" * 50,
        f"数据来源: 有知有行温度计",
        f"更新时间: {data.get('update_time', '未知')}",
        f"获取时间: {data['fetched_at']}",
        "",
        "一、市场概览",
        "-" * 30,
        f"  全市场温度: {temp}\u00b0 ({band})",
        f"  温度趋势:   {trend}",
        "",
    ]

    if band == "低估":
        lines.append("  [当前处于低估区间] 市场整体估值较低，是较好的投资时机。")
        lines.append("  历史数据显示，低估区间买入并持有5年，盈利概率 >95%。")
    elif band == "中估":
        lines.append("  [当前处于中估区间] 市场估值处于正常水平。")
        lines.append("  建议维持正常定投节奏，持有5年盈利概率 >90%。")
    else:
        lines.append("  [当前处于高估区间] 市场整体估值偏高，需注意风险。")
        lines.append("  高估区间买入并持有5年，盈利概率仅 >35%，建议谨慎。")
    lines.append("")

    # 指数估值一览
    if data.get("indices"):
        lines.append("二、指数估值一览")
        lines.append("-" * 30)
        lines.append(
            f"  {'指数':<12} {'温度':>4} {'温带':<4}"
            f" {'内在收益率':>10} {'股息率':>8} {'建议'}"
        )
        lines.append(
            f"  {'─' * 12} {'─' * 4} {'─' * 4}"
            f" {'─' * 10} {'─' * 8} {'─' * 10}"
        )
        for idx in sorted(data["indices"], key=lambda x: x["temperature"]):
            advice = get_index_advice(idx["temperature"])
            name = idx["name"][:10]
            intrinsic = idx.get("intrinsic_yield") or "--"
            dividend = idx.get("dividend_yield") or "--"
            lines.append(
                f"  {name:<12} {idx['temperature']:>3}\u00b0 {idx['band']:<4}"
                f" {intrinsic:>10} {dividend:>8} {advice}"
            )
        lines.append("")

    # 宏观数据
    macro = data.get("macro", {})
    if macro.get("bond_temperature") is not None:
        lines.append("三、宏观数据")
        lines.append("-" * 30)
        lines.append(f"  债市温度:         {macro['bond_temperature']}\u00b0")
        if macro.get("treasury_10y"):
            date_str = macro.get("treasury_10y_date", "")
            lines.append(f"  10Y国债收益率:    {macro['treasury_10y']} ({date_str})")
        if macro.get("gdp_growth"):
            date_str = macro.get("gdp_date", "")
            lines.append(f"  GDP增速:          {macro['gdp_growth']} ({date_str})")
        if macro.get("cpi_growth"):
            date_str = macro.get("cpi_date", "")
            lines.append(f"  CPI增速:          {macro['cpi_growth']} ({date_str})")
        lines.append("")

        bond_temp = macro["bond_temperature"]
        if temp < bond_temp:
            lines.append(
                f"  股市温度({temp}\u00b0) < 债市温度({bond_temp}\u00b0)"
                f" \u2192 股票性价比更高"
            )
        else:
            lines.append(
                f"  股市温度({temp}\u00b0) > 债市温度({bond_temp}\u00b0)"
                f" \u2192 需注意股市风险"
            )
        lines.append("")

    # 投资建议
    lines.append("四、投资建议")
    lines.append("-" * 30)
    lines.append("  【定投策略】")
    if band == "低估":
        lines.append("  \u2192 建议加倍定投（1.5-2倍），把握低估机会")
    elif band == "中估":
        lines.append("  \u2192 维持正常定投金额，保持纪律")
    else:
        lines.append("  \u2192 减少或暂停定投，注意风险控制")

    sorted_indices = sorted(data.get("indices", []), key=lambda x: x["temperature"])
    lines.append("  【板块配置】")
    low = [i["name"] for i in sorted_indices if i["temperature"] < 30]
    mid = [i["name"] for i in sorted_indices if 30 <= i["temperature"] < 70]
    high = [i["name"] for i in sorted_indices if i["temperature"] >= 70]
    if low:
        lines.append(f"  \u2192 低估板块（可积极配置）: {', '.join(low)}")
    if mid:
        lines.append(f"  \u2192 中估板块（正常配置）: {', '.join(mid)}")
    if high:
        lines.append(f"  \u2192 高估板块（谨慎对待）: {', '.join(high)}")

    lines.append("  【持有建议】")
    lines.append("  \u2192 建议投资期限: 3-5年以上")
    lines.append("  \u2192 投资心态: 低估多买、中估少买、高估不买")
    lines.append("")
    lines.append(
        "  以上建议基于历史数据回测，不构成投资建议。投资有风险，入市需谨慎。"
    )
    lines.append("=" * 50)

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="知行温度计数据解析工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="示例:\n"
               "  python3 fetch_thermometer.py -f thermometer.md\n"
               "  python3 fetch_thermometer.py -f thermometer.md --advice\n"
               "  cat thermometer.md | python3 fetch_thermometer.py --json\n",
    )
    parser.add_argument(
        "--file", "-f", help="从文件读取 Markdown 内容"
    )
    parser.add_argument(
        "--json", action="store_true", dest="json_output",
        help="以 JSON 格式输出",
    )
    parser.add_argument(
        "--advice", action="store_true", help="仅输出投资建议报告"
    )
    parser.add_argument(
        "--version", action="version", version=f"%(prog)s {__version__}"
    )
    args = parser.parse_args()

    # 获取输入
    text = ""
    if args.file:
        with open(args.file, "r", encoding="utf-8") as f:
            text = f.read()
    elif not sys.stdin.isatty():
        text = sys.stdin.read()
    else:
        parser.print_help()
        sys.exit(1)

    if not text.strip():
        print("错误: 输入内容为空", file=sys.stderr)
        sys.exit(1)

    # 解析
    data = parse_temperature(text)

    # 输出
    if args.advice:
        print(generate_advice(data))
    elif args.json_output:
        print(json.dumps(data, ensure_ascii=False, indent=2))
    else:
        print(json.dumps(data, ensure_ascii=False, indent=2))
        print("\n")
        print(generate_advice(data))


if __name__ == "__main__":
    main()
