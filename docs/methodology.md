# Methodology

## 1. Yield and trend
Yield is `output × 1000 ÷ harvested area` (kg/ha), computed on summed output and area for regions, so it is **area-weighted**.

Productivity grows over time (genetics, management), so a fixed yield is a poor benchmark. For every crop and region we fit a **Theil–Sen** line on 2000–2025:

- slope *b* = median of the slopes between every pair of years;
- intercept *a* = median(yield) − *b* × median(year);
- trend(*year*) = *a* + *b* × *year*.

Theil–Sen was chosen over ordinary least squares because a few very bad years (2005, 2012, 2022) would otherwise pull the line down. Slope for the whole state: soybean +47, wheat +49, rice +133, maize +169 kg/ha per year.

## 2. Deviation from trend
`deviation (%) = (observed yield ÷ trend − 1) × 100`. −28 means the year yielded 28% less than expected for that year. It isolates yield shortfalls from technology-driven growth and from changes in planted area.

## 3. Risk metrics
- **Coefficient of variation (CV):** standard deviation (n−1) ÷ mean × 100 of a municipality's yearly yield, 2010–2025. Computed on observed yield, so it includes the long-run growth and slightly overstates instability. Rule of thumb used in the dashboard (not a standard): below 15% stable, 15–30% moderate, above 30% high. Median CV by crop: rice 10, soybean 27, maize 32, wheat 32.
- **Worst deviation / worst year:** minimum deviation in the series and the year it happened. Shows severity, not frequency.
- Municipality-crop pairs need ≥ 10 years of data in 2010–2025 and a mean harvested area ≥ 500 ha.

## 4. Climate
- Source: ERA5 reanalysis through the Open-Meteo archive API. Modeled data, not station measurements.
- **One reference municipality per mesoregion** (Palmeira das Missões, Vacaria, Santa Maria, Santa Cruz do Sul, Camaquã, Alegrete, Pelotas), chosen by hand.
- Daily values are aggregated over each crop's assumed cycle (see data dictionary); anomalies are measured against the 2001–2025 mean of the same crop and region.
- **Correlation:** Pearson (and Spearman as a check) between the rainfall anomaly and the yield deviation, with the 7 regions stacked (n ≈ 175 per crop). Regions in the same year are not independent observations, so p-values are not reported.

## 5. Data checks
Municipal sums reproduce IBGE's state totals (`code/08_validate_against_state_totals.py`). The pipeline output is deterministic: rerunning the scripts regenerates the `data/powerbi/` files exactly.

## 6. Limitations
- Yield is a municipal annual average; it hides differences between farms.
- One climate point per mesoregion; local rainfall can differ a lot, and ERA5 is modeled.
- The windows differ by design: yield series 2000–2025, CV 2010–2025, climate 2001–2025.
- Cycles are assumed (not crop-calendar data by municipality). Annual data cannot capture timing of rainfall within the cycle.
- The trend assumes steady productivity growth; correlation does not imply causation.
- Production value is nominal.
- One municipality (Pinto Bandeira, created in 2013) is missing from the map boundaries used in the dashboard.
