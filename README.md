# Asset Allocation Skill (知行温度计)

A Claude Code Skill that provides A-share market temperature analysis and asset allocation advice based on the 有知有行 (youzhiyouxing.cn) thermometer data.

## Features

- Real-time A-share market temperature monitoring
- 12 major index valuation tracking
- Macro data integration (bond temp, treasury yield, GDP, CPI)
- Systematic investment advice based on temperature bands
- Stock-bond comparison analysis

## How It Works

The skill fetches live thermometer data via webReader, parses the Markdown content, and generates structured investment advice based on three temperature bands:

| Band | Range | Historical Frequency | 5-Year Profit Probability |
|------|-------|---------------------|--------------------------|
| Low (低估) | 0°-30° | 40% | >95% |
| Medium (中估) | 30°-70° | 38% | >90% |
| High (高估) | 70°-100° | 22% | >35% |

## Project Structure

```
asset-allocation/
├── SKILL.md                              # Skill definition (Claude Code)
├── README.md                             # This file
├── scripts/
│   └── fetch_thermometer.py             # Data parser and advice generator
└── references/
    └── thermometer_methodology.md        # Thermometer methodology docs
```

## Data Source

- **Source**: 有知有行 (youzhiyouxing.cn)
- **Methodology**: Equal-weighted PE/PB across all A-share listed companies
- **History**: Two complete bull/bear market cycles
- **Update**: After each trading day close (~20:00 CST)

## Tracked Indices

800消费, 中国互联网, 全指医药, 中证养老, 中证红利, 沪深300, 中证1000, 上证50, 创业板指, 中证2000, 中证500, 全指信息

## Usage (as Claude Code Skill)

Install this skill in your Claude Code skills directory, then trigger with keywords like:

- "温度计" / "市场温度" / "全市场温度"
- "现在能不能买" / "该不该加仓"
- "资产配置" / "定投建议"

## Standalone Script Usage

```bash
# Parse from file
python3 scripts/fetch_thermometer.py --file thermometer.md

# Parse from stdin (pipe from webReader output)
echo "$MARKDOWN" | python3 scripts/fetch_thermometer.py

# JSON output
python3 scripts/fetch_thermometer.py --file data.md --json

# Investment advice report
python3 scripts/fetch_thermometer.py --file data.md --advice
```

## Core Investment Principle

> 低估多买，中估少买，高估不买

## Disclaimer

This tool is for educational and reference purposes only. It does not constitute investment advice. Historical data does not predict future performance. Investment involves risk; please invest cautiously based on your own risk tolerance and financial situation.

## License

MIT

## Acknowledgments

- Temperature data: 有知有行 (youzhiyouxing.cn)
- Built as a Claude Code Skill
