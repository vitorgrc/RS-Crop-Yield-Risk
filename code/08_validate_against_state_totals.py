"""Sanity check: the sum of municipal values must match IBGE's published state (RS) totals, per crop and year.
Output: data/validation_sum_of_municipalities_vs_ibge_rs.csv"""
import json, urllib.request
from pathlib import Path
import pandas as pd

DATA = Path(__file__).resolve().parents[1] / "data"
PRODUCTS = {40124: "Soja", 40122: "Milho", 40102: "Arroz", 40127: "Trigo"}
VARS = {216: "area_colhida_ha", 214: "producao_t", 215: "valor_mil_reais"}
rows = []
for pc, pn in PRODUCTS.items():
    for vc, vn in VARS.items():
        url = f"https://apisidra.ibge.gov.br/values/t/5457/n3/43/v/{vc}/p/all/c782/{pc}"  # n3 43 = RS as a whole
        for r in json.load(urllib.request.urlopen(url, timeout=120))[1:]:
            rows.append({"cultura": pn, "ano": int(r["D3C"]), "variavel": vn, "ibge": pd.to_numeric(r["V"].replace("-", "0"), errors="coerce")})
ibge = pd.DataFrame(rows).pivot_table(index=["cultura", "ano"], columns="variavel", values="ibge").add_suffix("_ibge")
f = pd.read_csv(DATA / "powerbi/fato_pam.csv")
soma = f.groupby(["cultura", "ano"])[["area_colhida_ha", "producao_t", "valor_mil_reais"]].sum().add_suffix("_soma")
v = ibge.join(soma, how="inner")
for c in ["area_colhida_ha", "producao_t", "valor_mil_reais"]:
    v["d_" + c] = v[c + "_soma"] - v[c + "_ibge"]
v.round(2).to_csv(DATA / "validation_sum_of_municipalities_vs_ibge_rs.csv")
print(len(v), "crop-years; largest absolute difference:", v[[c for c in v.columns if c.startswith("d_")]].abs().max().to_dict())
