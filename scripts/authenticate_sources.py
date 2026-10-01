"""Compare original public caches with authoritative CDC downloads observed now.

This is an explicit network provenance check, separate from the offline analysis.
It never replaces the original caches or changes their fingerprint manifest.
"""
from __future__ import annotations

import io
import json
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
import requests

from analyze import MEASURES, digest

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data/raw"
OUT = ROOT / "reports/generated"
SVI_URL = "https://svi.cdc.gov/Documents/Data/2022/csv/states/SVI_2022_US.csv"
FIELDS = ["year", "locationid", "measureid", "datavaluetypeid", "data_value",
          "low_confidence_limit", "high_confidence_limit"]


def fetch(url, destination, params=None):
    response = requests.get(url, params=params, timeout=60)
    response.raise_for_status()
    destination.write_bytes(response.content)
    return response


def main():
    observed = datetime.now(timezone.utc).isoformat()
    official = RAW / "svi_2022_official_download.csv"
    fetch(SVI_URL, official)
    original_hash, official_hash = digest(RAW / "svi_2022.csv"), digest(official)
    svi_columns = ["FIPS", "STATE", "STCNTY", "RPL_THEMES", "RPL_THEME1", "RPL_THEME2", "RPL_THEME3", "RPL_THEME4", "E_TOTPOP"]
    original_svi = pd.read_csv(RAW / "svi_2022.csv", usecols=svi_columns, dtype={"FIPS": str, "STCNTY": str}).sort_values("FIPS").reset_index(drop=True)
    official_svi = pd.read_csv(official, usecols=svi_columns, dtype={"FIPS": str, "STCNTY": str}).sort_values("FIPS").reset_index(drop=True)
    svi_values_equal = original_svi.equals(official_svi)
    metadata = {}
    for identifier, label in [("ai6z-tcin", "2024_archive"), ("cwsq-ngmh", "current")]:
        path = RAW / f"places_{label}_metadata.json"
        response = fetch(f"https://data.cdc.gov/api/views/{identifier}.json", path)
        source = response.json()
        metadata[label] = {"id": source["id"], "name": source["name"], "description": source["description"],
                           "metadata_url": response.url, "metadata_sha256": digest(path),
                           "observed_utc": observed}
    where = "measureid in (" + ",".join(f"'{m}'" for m in MEASURES) + ")"
    parts = []
    requests_receipt = []
    for offset in range(0, 600_000, 100_000):
        params = {"$select": ",".join(FIELDS), "$where": where,
                  "$order": "locationid,measureid", "$limit": 100_000, "$offset": offset}
        path = RAW / f"places_current_selected_{offset}.csv"
        response = fetch("https://data.cdc.gov/resource/cwsq-ngmh.csv", path, params=params)
        part = pd.read_csv(io.StringIO(response.text), dtype={"locationid": str})
        parts.append(part)
        requests_receipt.append({"url": response.url, "rows": len(part), "sha256": digest(path)})
        print(f"Downloaded selected CDC page: offset={offset}, rows={len(part):,}", flush=True)
        if len(part) < 100_000:
            break
    live = pd.concat(parts, ignore_index=True).sort_values(["locationid", "measureid"]).reset_index(drop=True)
    rename = {"Year": "year", "LocationID": "locationid", "MeasureId": "measureid", "DataValueTypeID": "datavaluetypeid",
              "Data_Value": "data_value", "Low_Confidence_Limit": "low_confidence_limit", "High_Confidence_Limit": "high_confidence_limit"}
    original = pd.read_csv(ROOT / "data/processed/selected_places_with_intervals.csv", dtype={"LocationID": str}).rename(columns=rename)
    original = original[FIELDS].sort_values(["locationid", "measureid"]).reset_index(drop=True)
    live = live[FIELDS]
    compared = []
    for column in FIELDS:
        compared.append({"field": column, "equal": original[column].equals(live[column])})
    receipt = {"observed_utc": observed,
               "svi": {"official_url": SVI_URL, "official_sha256": official_hash, "cache_sha256": original_hash,
                       "bytes_equal": original_hash == official_hash, "selected_values_equal": svi_values_equal,
                       "official_rows": len(official_svi), "cache_rows": len(original_svi),
                       "scope": "Official download configured by CDC download selector: 2022 / US / census / CSV; national ranks"},
               "places_metadata": metadata, "places_selected_comparison": {"cache_rows": len(original), "live_rows": len(live),
                   "original_full_file_sha256": digest(RAW / "places_2024.csv"),
                   "fields": compared, "all_fields_equal": all(item["equal"] for item in compared),
                   "requests": requests_receipt},
               "limits": "Authenticates current official content and selected records, not original acquisition time or all 40 cached PLACES measures. Matching tract IDs and documented vintage do not prove identical source polygons."}
    (OUT / "source_authentication.json").write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(receipt, indent=2), flush=True)


if __name__ == "__main__":
    main()
