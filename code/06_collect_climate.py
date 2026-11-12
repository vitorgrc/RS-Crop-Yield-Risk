"""Daily climate (ERA5 reanalysis via Open-Meteo) at ONE reference municipality per mesoregion, 2000-2025.
Points are hand-picked representative municipalities (approximate coordinates); the data is modeled, not station-measured.
Output: data/raw/clima_diario_rs.csv"""
import json, time, urllib.request
from pathlib import Path
import pandas as pd

OUT = Path(__file__).resolve().parents[1] / "data" / "raw"
OUT.mkdir(parents=True, exist_ok=True)
POINTS = {  # mesoregion: (reference municipality, lat, lon)
    "Noroeste": ("Palmeira das Missões", -27.90, -53.31),
    "Nordeste": ("Vacaria", -28.51, -50.93),
    "Centro Ocidental": ("Santa Maria", -29.69, -53.81),
    "Centro Oriental": ("Santa Cruz do Sul", -29.72, -52.43),
    "Metropolitana de Porto Alegre": ("Camaquã", -30.85, -51.81),
    "Sudoeste": ("Alegrete", -29.78, -55.79),
    "Sudeste": ("Pelotas", -31.77, -52.34),
}
rows = []
for meso, (mun, lat, lon) in POINTS.items():
    url = ("https://archive-api.open-meteo.com/v1/archive?latitude=%s&longitude=%s&start_date=2000-01-01&end_date=2025-12-31"
           "&daily=precipitation_sum,temperature_2m_mean,temperature_2m_max&timezone=America%%2FSao_Paulo" % (lat, lon))
    d = None
    for t in range(4):
        try:
            d = json.load(urllib.request.urlopen(url, timeout=120))["daily"]
            break
        except Exception as e:  # Open-Meteo has daily request limits; retry later if it keeps failing
            print("retry", meso, e)
            time.sleep(5 * (t + 1))
    if d is None:
        raise SystemExit("failed: " + meso)
    df = pd.DataFrame(d).rename(columns={"time": "data", "precipitation_sum": "chuva_mm",
                                         "temperature_2m_mean": "temp_media_c", "temperature_2m_max": "temp_max_c"})
    df.insert(0, "mesorregiao", meso)
    df.insert(1, "ponto_referencia", mun)
    rows.append(df)
    print(meso, len(df), flush=True)
pd.concat(rows).to_csv(OUT / "clima_diario_rs.csv", index=False)
