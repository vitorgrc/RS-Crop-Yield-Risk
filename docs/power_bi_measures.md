# Power BI model and DAX

## Tables and relationships
- `fato_pam` ← `dim_municipio` (by `cod_municipio`), `dim_ano`, `dim_cultura`.
- `dim_cultura = DISTINCT ( fato_pam[cultura] )`, related one-to-many to `fato_pam`, `serie_rendimento_regiao`, `risco_municipio` and `clima_ciclo_x_rendimento` (single direction).
- `dim_mesorregiao = UNION ( DISTINCT ( dim_municipio[mesorregiao] ), ROW ( "mesorregiao", "Rio Grande do Sul (total)" ) )`, related to the series and climate tables. The "total" row is hidden from the slicer: **no selection = whole state**.
- `dicionario_indicadores` (from `docs/indicator_dictionary_pt.csv`) is a stand-alone table for the guide page.

## Measures (reference implementation; names are in Portuguese as in the report)
```DAX
Produção (t) = SUM ( fato_pam[producao_t] )
Área colhida (ha) = SUM ( fato_pam[area_colhida_ha] )
Rendimento (kg/ha) = DIVIDE ( [Produção (t)] * 1000, [Área colhida (ha)] )

Produção ano anterior =
CALCULATE ( [Produção (t)], FILTER ( ALL ( dim_ano[ano] ), dim_ano[ano] = MAX ( dim_ano[ano] ) - 1 ) )
Variação de produção = DIVIDE ( [Produção (t)] - [Produção ano anterior], [Produção ano anterior] )

-- state total when no region is selected
Rendimento real (kg/ha) =
IF ( ISFILTERED ( dim_mesorregiao[mesorregiao] ),
     AVERAGE ( serie_rendimento_regiao[rendimento_kg_ha] ),
     CALCULATE ( AVERAGE ( serie_rendimento_regiao[rendimento_kg_ha] ),
                 serie_rendimento_regiao[mesorregiao] = "Rio Grande do Sul (total)" ) )

-- worst deviation ignores the year slicer
Pior desvio (%) =
CALCULATE ( MIN ( serie_rendimento_regiao[desvio_pct] ), REMOVEFILTERS ( dim_ano[ano] ),
            serie_rendimento_regiao[mesorregiao] = "Rio Grande do Sul (total)" )
Pior ano =
VAR p = [Pior desvio (%)]
RETURN CALCULATE ( MIN ( serie_rendimento_regiao[ano] ), FILTER ( serie_rendimento_regiao, serie_rendimento_regiao[desvio_pct] = p ) )

-- yield in 60 kg bags (50 kg for rice) when a single crop is selected
Kg por saca = SWITCH ( SELECTEDVALUE ( dim_cultura[cultura] ), "Soja", 60, "Milho", 60, "Trigo", 60, "Arroz", 50, BLANK () )
Rendimento exibido =
VAR k = [Kg por saca]
RETURN IF ( ISBLANK ( k ), [Rendimento (kg/ha)], DIVIDE ( [Rendimento (kg/ha)], k ) )
```
Notes: `desvio_pct` is already in percentage points, so format it as a number, not as a percentage. The measures that read the series and climate tables follow the same "state total when nothing is selected" pattern. Percent indicators (CV, deviation) do not change with the yield unit.

## Report pages (Portuguese interface)
1. **Panorama:** production, area, yield, value, variation vs previous harvest; production by mesoregion; top 10 municipalities.
2. **Risco de produtividade:** trend and deviation, worst year, CV, map and ranking of riskiest municipalities.
3. **Clima e Rendimento:** rainfall and temperature anomalies, dry days, correlation, scatter, mesoregion × year heatmap of deviations.
4. **Guia de leitura:** plain-language dictionary of every indicator (`docs/indicator_dictionary_pt.csv`).

Design kit: `dashboard/theme_agro_rs_dark.json` (Power BI theme) and `dashboard/background.png` (page background).
