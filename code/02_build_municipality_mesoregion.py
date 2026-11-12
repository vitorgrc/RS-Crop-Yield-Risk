"""Map each RS municipality to its IBGE mesoregion (codes 4301-4307) using SIDRA's territorial hierarchy.
Output: data/raw/municipio_meso.csv"""
import json, time, urllib.request
from pathlib import Path
import pandas as pd

OUT = Path(__file__).resolve().parents[1] / "data" / "raw"
OUT.mkdir(parents=True, exist_ok=True)
rows = []
for meso in range(4301, 4308):
    # n6 = municipalities contained in mesoregion n8 = <meso>; any table/variable works, we only need the territory codes
    url = f"https://apisidra.ibge.gov.br/values/t/5457/n6/in%20n8%20{meso}/v/214/p/2020/c782/40124"
    for attempt in range(4):
        try:
            data = json.load(urllib.request.urlopen(url, timeout=120))
            break
        except Exception as e:
            print("retry", meso, e)
            time.sleep(3 * (attempt + 1))
    else:
        raise SystemExit(f"failed: {meso}")
    rows += [(r["D1C"], meso) for r in data[1:]]
    print(meso, len(data) - 1)
m = pd.DataFrame(rows, columns=["cod_municipio", "cod_meso"]).drop_duplicates()
m.sort_values("cod_municipio").to_csv(OUT / "municipio_meso.csv", index=False)
print(len(m), "municipalities")
