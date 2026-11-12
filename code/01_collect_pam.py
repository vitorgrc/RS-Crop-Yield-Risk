"""Download IBGE's PAM (Municipal Agricultural Production, SIDRA table 5457) for every RS municipality.
Output: data/raw/pam_rs_raw.csv (long format, one row per municipality-year-crop-variable)."""
import json, time, urllib.request
from pathlib import Path
import pandas as pd

OUT = Path(__file__).resolve().parents[1] / "data" / "raw"
OUT.mkdir(parents=True, exist_ok=True)
PRODUCTS = {40124: "Soja", 40122: "Milho", 40102: "Arroz", 40127: "Trigo"}  # soy, maize, rice, wheat
VARS = {8331: "area_plantada_ha", 216: "area_colhida_ha", 214: "producao_t",
        112: "rendimento_kg_ha", 215: "valor_mil_reais"}  # planted area, harvested area, output, yield, value
rows = []
for pc, pn in PRODUCTS.items():
    for vc, vn in VARS.items():
        # n6 = municipalities, n3 43 = Rio Grande do Sul, c782 = crop classification
        url = f"https://apisidra.ibge.gov.br/values/t/5457/n6/in%20n3%2043/v/{vc}/p/all/c782/{pc}"
        data = None
        for attempt in range(4):
            try:
                data = json.load(urllib.request.urlopen(url, timeout=120))
                break
            except Exception as e:
                print("retry", pn, vn, e)
                time.sleep(3 * (attempt + 1))
        if data is None:
            raise SystemExit(f"failed: {pn} {vn}")
        for r in data[1:]:  # first element is the header
            rows.append({"cod_municipio": r["D1C"], "municipio": r["D1N"], "ano": int(r["D3C"]), "cultura": pn,
                         "variavel": vn, "unidade": r["MN"], "valor_bruto": r["V"]})
        print(pn, vn, len(data) - 1, flush=True)
pd.DataFrame(rows).to_csv(OUT / "pam_rs_raw.csv", index=False)
print("total rows", len(rows))
