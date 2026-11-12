"""Aggregate climate over each crop's growing cycle and join it with the yield deviation (Theil-Sen).
Output: data/powerbi/clima_ciclo_x_rendimento.csv. Also prints correlations used in the README."""
from pathlib import Path
import pandas as pd
from scipy.stats import pearsonr, spearmanr

DATA = Path(__file__).resolve().parents[1] / "data"
c = pd.read_csv(DATA / "raw/clima_diario_rs.csv", parse_dates=["data"])
c["ano"] = c.data.dt.year
# Assumed growing cycles (year = harvest year in PAM): (start month, start-year offset, end month)
CICLO = {"Soja": (11, -1, 3), "Milho": (10, -1, 3), "Arroz": (10, -1, 3), "Trigo": (6, 0, 11)}

def window(crop, year):
    mi, off, mf = CICLO[crop]
    return pd.Timestamp(year + off, mi, 1), pd.Timestamp(year, mf, 1) + pd.offsets.MonthEnd(0)

rows = []
for meso, g in c.groupby("mesorregiao"):
    for crop in CICLO:
        for year in range(2001, 2026):
            a, b = window(crop, year)
            x = g[(g.data >= a) & (g.data <= b)]
            rows.append({"cultura": crop, "mesorregiao": meso, "ano": year, "chuva_ciclo_mm": x.chuva_mm.sum(),
                         "temp_media_ciclo_c": x.temp_media_c.mean(), "temp_max_media_ciclo_c": x.temp_max_c.mean(),
                         "dias_secos_ciclo": int((x.chuva_mm < 1).sum())})  # dry day = < 1 mm
cl = pd.DataFrame(rows)
# anomalies against the 2001-2025 mean of the same crop and mesoregion: rain in %, temperature in degrees C
for v, n in (("chuva_ciclo_mm", "chuva_anomalia_pct"), ("temp_media_ciclo_c", "temp_anomalia_c")):
    mean = cl.groupby(["cultura", "mesorregiao"])[v].transform("mean")
    cl[n] = (cl[v] / mean - 1) * 100 if v.startswith("chuva") else cl[v] - mean
s = pd.read_csv(DATA / "powerbi/serie_rendimento_regiao.csv")
m = cl.merge(s[["cultura", "mesorregiao", "ano", "rendimento_kg_ha", "desvio_pct"]], on=["cultura", "mesorregiao", "ano"], how="inner")
m.round(2).to_csv(DATA / "powerbi/clima_ciclo_x_rendimento.csv", index=False)
print("rows", len(m))
print("\nCorrelation (Pearson / Spearman) between yield deviation and climate, regions stacked:")
for crop, x in m.groupby("cultura"):
    out = [f"{v}: r={pearsonr(x[v], x.desvio_pct)[0]:+.2f} / rho={spearmanr(x[v], x.desvio_pct)[0]:+.2f}"
           for v in ["chuva_anomalia_pct", "temp_anomalia_c", "dias_secos_ciclo"]]
    print(crop, len(x), "|", " | ".join(out))
