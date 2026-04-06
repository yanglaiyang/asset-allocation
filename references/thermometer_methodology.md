# YouZhiYouXing Market Thermometer: Methodology Reference

## Overview

The YouZhiYouXing (YZYX) Market Thermometer is a valuation-based market timing tool for China's A-share market. It synthesizes two fundamental valuation metrics -- Price-to-Earnings (PE) and Price-to-Book (PB) ratios -- across all A-share listed companies to produce a single temperature reading on a 0-100 degree scale, providing investors with an intuitive measure of market heat.

**Data source**: [YouZhiYouXing (youzhiyouxing.cn)](https://youzhiyouxing.cn)

---

## 1. Core Methodology

### 1.1 Universe and Sample Space

- **Coverage**: All A-share listed companies (excludes ST stocks and companies with incomplete financial data).
- **Exchange coverage**: Shanghai Stock Exchange (SSE), Shenzhen Stock Exchange (SZSE), and ChiNext board.
- **Historical range**: Two complete bull/bear market cycles, providing robust statistical significance for percentile-based temperature readings.

### 1.2 Valuation Metrics

The thermometer uses two complementary valuation indicators:

| Metric | Full Name | Description |
|--------|-----------|-------------|
| **PE** | Price-to-Earnings Ratio (市盈率) | Stock price divided by earnings per share. Reflects how much investors are willing to pay per unit of earnings. |
| **PB** | Price-to-Book Ratio (市净率) | Stock price divided by book value per share. Reflects how much investors are willing to pay per unit of net asset value. |

Using both PE and PB together mitigates the limitations of each individual metric:
- PE can be distorted by one-time gains/losses, cyclical earnings swings, or negative earnings.
- PB can be misleading for asset-light companies or those with significant intangible assets.

### 1.3 Equal-Weight Aggregation

**Critical design choice**: The thermometer uses an **equal-weight** (等权) approach rather than market-cap-weighted (市值加权) aggregation.

This means every listed company contributes equally to the overall PE and PB calculations, regardless of its market capitalization. This design decision has important implications:

| Aspect | Equal-Weight | Market-Cap-Weighted |
|--------|-------------|-------------------|
| Representation | Reflects the "typical" company | Dominated by large caps |
| Sensitivity | More responsive to broad market sentiment | Skewed by mega-cap moves |
| Small-cap signal | Captures small-cap valuation shifts | Dilutes small-cap influence |
| Interpretation | "How is the average stock valued?" | "How is total market cap valued?" |

The equal-weight approach better captures the investment experience of a diversified retail investor and avoids the scenario where a few mega-cap stocks mask broad market over- or under-valuation.

### 1.4 Temperature Calculation

The temperature is derived from the historical percentile ranking of the current equal-weighted PE and PB composite:

1. Calculate the current equal-weighted PE and PB across all A-share companies.
2. Determine the historical percentile of the current composite valuation relative to the full historical range (two complete bull/bear cycles).
3. Map the percentile to a 0-100 degree scale.

A higher temperature indicates the market is more expensive relative to its own history; a lower temperature indicates cheaper valuations.

---

## 2. Temperature Bands

### 2.1 Band Definitions

| Band | Temperature Range | Historical Frequency | 5-Year Holding Profit Probability | Investment Implication |
|------|------------------|---------------------|-----------------------------------|----------------------|
| Low (低估) | 0 - 30 degrees | ~40% of trading days | > 95% | Attractive entry point; increase allocation |
| Medium (中估) | 30 - 70 degrees | ~38% of trading days | > 90% | Fair valuation; maintain regular investment pace |
| High (高估) | 70 - 100 degrees | ~22% of trading days | > 35% | Expensive; reduce new purchases, consider taking profits |

### 2.2 Key Observations

- **Low-temperature zones occur most frequently** (approximately 40% of the time), meaning attractive buying opportunities are the norm rather than the exception.
- **High-temperature zones**, while less frequent, can persist for extended periods, testing investor patience and discipline.
- The profit probability differential between low and high zones is dramatic (>95% vs. >35%), underscoring the value of disciplined valuation-based investing.

### 2.3 Core Investment Principle

> **Buy more when undervalued, buy less when fairly valued, and do not buy (or sell) when overvalued.**

In Chinese: **低估多买，中估少买，高估不买，甚至要在高估时逐渐兑现收益。**

This principle acknowledges that:
- Market timing cannot be precise; the goal is "approximate accuracy" (模糊的准确).
- The thermometer is designed for **long-cycle tactical allocation**, not short-term trading.
- Patience and discipline are essential: the market can remain in any temperature zone for months or even years.

---

## 3. Return Attribution Analysis

A fundamental insight from the thermometer's historical data is the decomposition of long-term A-share returns into their constituent sources.

### 3.1 Wind All-A Index (万得全A) Return Decomposition

Over the full historical measurement period (two complete bull/bear cycles):

| Component | Cumulative Contribution | Share of Total Return |
|-----------|----------------------|-----------------------|
| **Net Asset Growth (净资产增长)** | +535.64% | ~75% |
| **Dividend Yield (股息收益)** | +37.91% | ~5% |
| **Valuation Change (估值变化)** | -7.34% | ~-1% |
| **Total Cumulative Return (累计收益率)** | **712.31%** | **100%** |

### 3.2 Interpretation

This decomposition reveals a critical truth about long-term equity returns:

1. **Earnings growth is the dominant driver**: Approximately 75% of total return comes from the compounding of corporate net assets (i.e., retained earnings reinvested by companies). This is the engine of long-term wealth creation.

2. **Dividends provide a meaningful contribution**: The 5% contribution from dividends represents a real cash return stream that compounds over time and provides downside cushion during market declines.

3. **Valuation change is a net negative over the full cycle**: Despite significant valuation expansion during bull markets, the net effect of valuation changes across a full cycle is slightly negative. This means that, on average, **you cannot rely on valuation expansion to generate returns**.

**Implication for investors**: The primary reason to invest in equities is to participate in corporate earnings growth, not to speculate on valuation multiples expanding. The thermometer helps investors avoid the common mistake of buying when valuations are already high (which historically leads to poor outcomes) and encourages buying when valuations are low (when the probability of strong future returns is highest).

---

## 4. Bond Market Temperature

In addition to the equity market thermometer, YZYX also provides a **bond market temperature** (债市温度) to help investors assess the relative attractiveness of stocks versus bonds.

### 4.1 Bond Temperature Methodology

- The bond market temperature uses a similar percentile-based approach, measuring current bond yields (primarily 10-year Chinese government bond yields) against their historical distribution.
- A **high bond temperature** indicates bond yields are low relative to history (bond prices are high; bonds are expensive).
- A **low bond temperature** indicates bond yields are high relative to history (bond prices are low; bonds are cheap).

### 4.2 Stock-Bond Comparison Framework

| Scenario | Stock Temperature | Bond Temperature | Interpretation |
|----------|------------------|------------------|----------------|
| Stocks cheap, bonds expensive | Low | High | Favorable environment for equity allocation; consider reducing bond exposure |
| Both fairly valued | Medium | Medium | Maintain balanced allocation |
| Stocks expensive, bonds cheap | High | Low | Consider reducing equity exposure; bonds offer relatively better value |
| Both expensive | High | High | Exercise caution across asset classes; consider cash or alternative assets |

This stock-bond comparison provides a second dimension to the allocation decision beyond the equity temperature alone.

---

## 5. Tracked Indices

The thermometer monitors 12 major A-share and China-related indices, each with its own temperature reading, intrinsic yield (内在收益率), and dividend yield (股息率):

| Index Name | Index Code | Full Name | Description |
|-----------|-----------|-----------|-------------|
| 800消费 | 000932.SH | CSI 800 Consumer Index | Broad consumption sector covering large, mid, and small-cap consumer stocks |
| 中国互联网 | H11136.CSI | China Internet Index | Tracks China's leading internet and technology companies |
| 全指医药 | 000991.SH | CSI All Share Pharmaceutical Index | Comprehensive pharmaceutical and healthcare sector index |
| 中证养老 | 399812.SZ | CSI Pension Industry Index | Companies benefiting from China's aging demographics |
| 中证红利 | 000922.CSI | CSI Dividend Index | High-dividend-yield companies with consistent dividend records |
| 沪深300 | 000300.SH | CSI 300 Index | Top 300 stocks by market cap on SSE and SZSE; the core large-cap benchmark |
| 中证1000 | 000852.SH | CSI 1000 Index | The next 1,000 stocks after CSI 300 by market cap; mid/small-cap benchmark |
| 上证50 | 000016.SH | SSE 50 Index | The 50 largest stocks on the Shanghai Stock Exchange; mega-cap benchmark |
| 创业板指 | 399006.SZ | ChiNext Index | Top 100 stocks on the ChiNext board; growth and tech-oriented |
| 中证2000 | 932000.CSI | CSI 2000 Index | Small-cap stocks outside CSI 800; micro-cap benchmark |
| 中证500 | 000905.SH | CSI 500 Index | Mid-cap stocks outside CSI 300; mid-cap benchmark |
| 全指信息 | 000993.SH | CSI All Share Information Technology Index | Comprehensive IT sector covering hardware, software, and services |

### Index Temperature Interpretation

Each index temperature is calculated independently using the same equal-weight PE/PB methodology applied to the constituent stocks of that index. This allows for:

- **Cross-index comparison**: Identify which sectors are relatively cheap or expensive.
- **Sector rotation**: Shift allocation toward lower-temperature sectors.
- **Concentration risk detection**: When a single index reaches extreme temperatures, it signals potential risk in that sector.

---

## 6. Macro Data Integration

The thermometer dashboard also tracks key macroeconomic indicators to provide broader economic context:

| Indicator | Description | Update Frequency |
|-----------|-------------|-----------------|
| Bond Market Temperature (债市温度) | Bond market valuation temperature | Daily (after trading close) |
| 10-Year Government Bond Yield (10期国债到期收益率) | Risk-free rate proxy; key for equity risk premium calculation | Daily |
| GDP Quarterly YoY Growth (GDP季度同比增速) | Economic growth rate; measures overall economic health | Quarterly |
| CPI Monthly YoY Growth (CPI月度同比增速) | Consumer price inflation; monetary policy reference | Monthly |

---

## 7. Data Access

### 7.1 API Endpoints

| Endpoint | URL | Description |
|----------|-----|-------------|
| Thermometer (current) | `https://youzhiyouxing.cn/thermometer?format=md` | Current market temperature in Markdown format |
| Historical data | `https://youzhiyouxing.cn/data/market?format=md` | Historical temperature statistics and charts |
| Macro data | `https://youzhiyouxing.cn/data/macro?format=md` | Macroeconomic indicators |
| Documentation | `https://youzhiyouxing.cn/n/materials/172?format=md` | Official thermometer usage guide |
| LLM index | `https://youzhiyouxing.cn/llms.txt` | Content index for LLM integration |

### 7.2 Update Schedule

- **Equity temperature data**: Updated after each trading day close, typically around 20:00 China Standard Time (CST).
- **Macro data**: Updated according to the release schedule of each indicator (daily for bond yields, quarterly for GDP, monthly for CPI).
- **Caching**: The API supports `Cache-Control: public, max-age=300` (5-minute cache).

---

## 8. Methodology Limitations and Caveats

1. **Historical percentile dependency**: The temperature is meaningful only to the extent that the historical range (two complete cycles) is representative of future market behavior. Structural changes in the market (e.g., inclusion of ChiNext STAR Market, changes in listing rules) may affect the baseline.

2. **Equal-weight vs. investable**: While the equal-weight approach is analytically informative, most investable indices (CSI 300, CSI 500) are market-cap-weighted. Actual portfolio returns may differ from the equal-weight composite.

3. **No forward-looking information**: The thermometer is purely backward-looking (based on historical valuations). It does not incorporate earnings forecasts, macro outlook, or policy expectations.

4. **Temperature is not timing**: Even within a low-temperature zone, the market can decline further before recovering. The thermometer indicates probability, not certainty.

5. **Bond temperature comparability**: The equity and bond temperature scales are calculated independently and may not be directly comparable in magnitude. The comparison is most meaningful in relative terms (which asset class is cheaper relative to its own history).

---

## 9. References

- YouZhiYouXing Thermometer Page: [https://youzhiyouxing.cn/thermometer](https://youzhiyouxing.cn/thermometer)
- YouZhiYouXing Official Documentation: [https://youzhiyouxing.cn/n/materials/172](https://youzhiyouxing.cn/n/materials/172)
- Historical Data: [https://youzhiyouxing.cn/data/market](https://youzhiyouxing.cn/data/market)
- Wind All-A Index (万得全A): Provided by Wind Info (万得)
