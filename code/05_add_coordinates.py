"""Add municipality centroid coordinates (latitude/longitude) to dim_municipio.csv.
Source: kelvins/municipios-brasileiros (MIT), downloaded at run time; joined by 7-digit IBGE code."""
import urllib.request
from pathlib import Path
import pandas as pd

DATA = Path(__file__).resolve().parents[1] / "data"
URL = "https://raw.githubusercontent.com/kelvins/municipios-brasileiros/main/csv/municipios.csv"
k = pd.read_csv(urllib.request.urlopen(URL, timeout=120), dtype={"codigo_ibge": str})
d = pd.read_csv(DATA / "powerbi/dim_municipio.csv", dtype={"cod_municipio": str}).drop(columns=["latitude", "longitude"], errors="ignore")
d = d.merge(k[["codigo_ibge", "latitude", "longitude"]], left_on="cod_municipio", right_on="codigo_ibge", how="left").drop(columns="codigo_ibge")
print("municipalities without coordinates:", d.latitude.isna().sum())
d.to_csv(DATA / "powerbi/dim_municipio.csv", index=False)
