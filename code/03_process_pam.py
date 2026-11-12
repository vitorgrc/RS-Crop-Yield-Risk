"""Clean the raw PAM data: wide table per municipality-crop-year, plus mesoregion.
Output: data/processed/pam_rs_fato.csv"""
from pathlib import Path
import pandas as pd

DATA = Path(__file__).resolve().parents[1] / "data"
(DATA / "processed").mkdir(exist_ok=True)
MESO = {4301: "Noroeste", 4302: "Nordeste", 4303: "Centro Ocidental", 4304: "Centro Oriental",
        4305: "Metropolitana de Porto Alegre", 4306: "Sudoeste", 4307: "Sudeste"}
df = pd.read_csv(DATA / "raw/pam_rs_raw.csv", dtype={"cod_municipio": str, "valor_bruto": str})
# IBGE conventions: '-' = zero (no production); '...' / 'X' = not available -> left empty
df["valor"] = df.valor_bruto.replace({"-": "0"}).pipe(pd.to_numeric, errors="coerce")
w = (df.pivot_table(index=["cod_municipio", "municipio", "ano", "cultura"], columns="variavel",
                    values="valor", aggfunc="first").reset_index())
w["municipio"] = w.municipio.str.replace(r" - RS$", "", regex=True)
mm = pd.read_csv(DATA / "raw/municipio_meso.csv", dtype={"cod_municipio": str})
mm["mesorregiao"] = mm.cod_meso.map(MESO)
w = w.merge(mm[["cod_municipio", "mesorregiao"]], on="cod_municipio", how="left")
# keep only rows with actual harvest (harvested area > 0)
w = w[w.area_colhida_ha.fillna(0) > 0].copy()
w["rendimento_kg_ha"] = w.producao_t * 1000 / w.area_colhida_ha  # yield recomputed from output and harvested area
cols = ["cod_municipio", "municipio", "mesorregiao", "ano", "cultura", "area_plantada_ha", "area_colhida_ha",
        "producao_t", "rendimento_kg_ha", "valor_mil_reais"]
w[cols].sort_values(["cultura", "ano", "municipio"]).to_csv(DATA / "processed/pam_rs_fato.csv", index=False)
print(w.shape, "rows without mesoregion:", w.mesorregiao.isna().sum())
