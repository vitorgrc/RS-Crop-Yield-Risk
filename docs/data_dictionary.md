# Data dictionary

Column names are kept in Portuguese because they match the Power BI model. Crop names: *Soja* = soybean, *Milho* = maize, *Arroz* = rice (paddy), *Trigo* = wheat.
**Origin:** *Extracted* = taken as published by the source. *Calculated* = built in this project.

## `data/powerbi/fato_pam.csv` — fact table (68,457 rows)
One row per municipality, crop and year with harvested area > 0, 1974–2025, 497 RS municipalities. Source: IBGE, PAM, SIDRA table 5457.

| Column | Type | Description | Origin |
|---|---|---|---|
| `cod_municipio` | text | IBGE 7-digit municipality code | Extracted |
| `municipio` | text | Municipality name | Extracted |
| `mesorregiao` | text | IBGE mesoregion (7 in RS) | Calculated (join with `municipio_meso.csv`) |
| `ano` | integer | Harvest year | Extracted |
| `cultura` | text | Crop | Extracted |
| `area_plantada_ha` | number | Planted area (ha) | Extracted (variable 8331) |
| `area_colhida_ha` | number | Harvested area (ha) | Extracted (variable 216) |
| `producao_t` | number | Output (tonnes) | Extracted (variable 214) |
| `rendimento_kg_ha` | number | Yield (kg/ha) = `producao_t` × 1000 ÷ `area_colhida_ha` | Calculated |
| `valor_mil_reais` | number | Gross production value, thousand BRL, nominal (not inflation-adjusted) | Extracted (variable 215) |

## `data/powerbi/dim_municipio.csv` — municipality dimension (497 rows)
| Column | Type | Description | Origin |
|---|---|---|---|
| `cod_municipio`, `municipio`, `mesorregiao` | text | As above | Extracted / Calculated |
| `latitude`, `longitude` | number | Approximate municipality centroid | Extracted from kelvins/municipios-brasileiros (MIT) |

## `data/powerbi/serie_rendimento_regiao.csv` — yearly series by region (2000–2025)
One row per crop, region and year. Regions are the 7 mesoregions plus `Rio Grande do Sul (total)`.

| Column | Type | Description | Origin |
|---|---|---|---|
| `cultura`, `mesorregiao`, `ano` | text/integer | Keys | — |
| `producao_t` | number | Sum of municipal output | Calculated |
| `area_colhida_ha` | number | Sum of municipal harvested area | Calculated |
| `rendimento_kg_ha` | number | Area-weighted yield = Σ output × 1000 ÷ Σ harvested area | Calculated |
| `tendencia_kg_ha` | number | Expected yield from the Theil–Sen trend fitted on 2000–2025 | Calculated |
| `desvio_pct` | number | Deviation from trend, in **percentage points** (−27.64 = 27.64% below trend) = (yield ÷ trend − 1) × 100 | Calculated |

## `data/powerbi/risco_municipio.csv` — municipal risk (1,093 municipality-crop pairs)
Only pairs with at least 10 years of data in 2010–2025 and a mean harvested area of at least 500 ha.

| Column | Type | Description | Origin |
|---|---|---|---|
| `cultura`, `cod_municipio`, `municipio`, `mesorregiao` | text | Keys and labels | — |
| `anos_com_dado` | integer | Years with data in 2010–2025 | Calculated |
| `area_media_ha`, `producao_media_t` | number | Means over those years | Calculated |
| `rendimento_medio_kg_ha` | number | Mean yield | Calculated |
| `cv_rendimento_pct` | number | Coefficient of variation = standard deviation ÷ mean × 100 of the yearly yield | Calculated |
| `pior_desvio_pct` | number | Largest negative deviation from the municipal Theil–Sen trend (percentage points) | Calculated |
| `ano_pior` | integer | Year in which that largest deviation occurred | Calculated |

## `data/powerbi/clima_ciclo_x_rendimento.csv` — climate over the crop cycle vs yield (2001–2025)
One row per crop, mesoregion and year. Climate is from **one reference point per mesoregion** (see `code/06_collect_climate.py`).

| Column | Type | Description | Origin |
|---|---|---|---|
| `chuva_ciclo_mm` | number | Total rainfall in the crop cycle (mm) | Calculated |
| `temp_media_ciclo_c`, `temp_max_media_ciclo_c` | number | Mean of daily mean / daily maximum temperature in the cycle (°C) | Calculated |
| `dias_secos_ciclo` | integer | Days with rainfall below 1 mm in the cycle | Calculated |
| `chuva_anomalia_pct` | number | (cycle rainfall ÷ 2001–2025 mean for the same crop and region − 1) × 100 | Calculated |
| `temp_anomalia_c` | number | Cycle mean temperature minus its 2001–2025 mean (°C) | Calculated |
| `rendimento_kg_ha`, `desvio_pct` | number | From `serie_rendimento_regiao.csv` | Calculated |

Assumed cycles (harvest year *y*): soybean Nov(*y*−1)–Mar(*y*), maize and rice Oct(*y*−1)–Mar(*y*), wheat Jun–Nov(*y*).

## Raw files (`data/raw/`)
| File | Description |
|---|---|
| `clima_diario_rs.csv` | Daily rainfall and temperature (ERA5 via Open-Meteo) at 7 reference points, 2000–2025: `mesorregiao`, `ponto_referencia`, `data`, `chuva_mm`, `temp_media_c`, `temp_max_c` |
| `municipio_meso.csv` | `cod_municipio` → `cod_meso` (IBGE mesoregion codes 4301–4307) |
| `pam_rs_raw.csv` | Not versioned (35 MB). Regenerate with `code/01_collect_pam.py` |

## `data/validation_sum_of_municipalities_vs_ibge_rs.csv`
For each crop and year, the sum of municipal values versus IBGE's published state total. Output and area match exactly in all 208 crop-years; value differs by at most 0.02% (rounding in the source).
