"""Build the Power BI tables (data/powerbi/): robust yield trend (Theil-Sen), deviation from trend, municipal risk (CV).
Outputs: fato_pam.csv, dim_municipio.csv (without coordinates; see 05), serie_rendimento_regiao.csv, risco_municipio.csv"""
from pathlib import Path
import pandas as pd
from scipy.stats import theilslopes

DATA = Path(__file__).resolve().parents[1] / "data"
O = DATA / "powerbi"
O.mkdir(exist_ok=True)
w = pd.read_csv(DATA / "processed/pam_rs_fato.csv", dtype={"cod_municipio": str})
w[["cod_municipio", "municipio", "mesorregiao"]].drop_duplicates().sort_values("municipio").to_csv(O / "dim_municipio.csv", index=False)
w.to_csv(O / "fato_pam.csv", index=False)

def trend_dev(x):
    """Theil-Sen line of yield on year; deviation = observed / trend - 1 (in %)."""
    s, i, *_ = theilslopes(x.rend, x.ano)
    x = x.copy()
    x["tendencia_kg_ha"] = i + s * x.ano
    x["desvio_pct"] = (x.rend / x.tendencia_kg_ha - 1) * 100
    return x

def agg(df, keys):
    a = df.groupby(keys + ["ano"]).agg(producao_t=("producao_t", "sum"), area_colhida_ha=("area_colhida_ha", "sum")).reset_index()
    a["rend"] = a.producao_t * 1000 / a.area_colhida_ha  # area-weighted yield
    return a

d = w[w.ano >= 2000]
# state level and mesoregion level, per year
est = pd.concat([trend_dev(x) for _, x in agg(d, ["cultura"]).groupby("cultura")])
est.insert(1, "mesorregiao", "Rio Grande do Sul (total)")
mes = pd.concat([trend_dev(x) for _, x in agg(d, ["cultura", "mesorregiao"]).groupby(["cultura", "mesorregiao"]) if len(x) >= 20])
serie = pd.concat([est, mes]).rename(columns={"rend": "rendimento_kg_ha"})
serie.round(2).to_csv(O / "serie_rendimento_regiao.csv", index=False)

# municipal risk (2010-2025): only municipality-crop pairs with >= 10 years of data and mean harvested area >= 500 ha
m = w[w.ano >= 2010].copy()
rows = []
for (c, cod), x in m.groupby(["cultura", "cod_municipio"]):
    if len(x) < 10 or x.area_colhida_ha.mean() < 500:
        continue
    x = x.rename(columns={"rendimento_kg_ha": "rend"})
    s, i, *_ = theilslopes(x.rend, x.ano)
    dev = (x.rend / (i + s * x.ano) - 1) * 100
    rows.append({"cultura": c, "cod_municipio": cod, "municipio": x.municipio.iloc[0], "mesorregiao": x.mesorregiao.iloc[0],
                 "anos_com_dado": len(x), "area_media_ha": x.area_colhida_ha.mean(), "producao_media_t": x.producao_t.mean(),
                 "rendimento_medio_kg_ha": x.rend.mean(), "cv_rendimento_pct": x.rend.std() / x.rend.mean() * 100,  # std with ddof=1
                 "pior_desvio_pct": dev.min(), "ano_pior": int(x.ano.iloc[dev.values.argmin()])})
rm = pd.DataFrame(rows)
rm.round(2).to_csv(O / "risco_municipio.csv", index=False)
print(len(rm), rm.groupby("cultura").size().to_dict())
for c in ["Soja", "Milho", "Arroz", "Trigo"]:
    x = est[est.cultura == c]
    print(c, "worst years (year, deviation %):", x.nsmallest(3, "desvio_pct")[["ano", "desvio_pct"]].round(0).astype(int).values.tolist())
