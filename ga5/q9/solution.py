# /// script
# requires-python = ">=3.11"
# dependencies = ["pandas", "numpy"]
# ///

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

HQ_LAT = 28.6139
HQ_LON = 77.209
EARTH_RADIUS_KM = 6371.0


def haversine_km(lat: np.ndarray, lon: np.ndarray) -> np.ndarray:
    lat1 = np.radians(HQ_LAT)
    lon1 = np.radians(HQ_LON)
    lat2 = np.radians(lat)
    lon2 = np.radians(lon)

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = np.sin(dlat / 2.0) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2.0) ** 2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
    return EARTH_RADIUS_KM * c


def main() -> None:
    base_dir = Path(__file__).resolve().parent
    input_path = base_dir / "q-geospatial-haversine-correlation.csv"

    df = pd.read_csv(input_path)
    df["Distance_Km"] = haversine_km(
        df["Latitude"].astype(float).to_numpy(),
        df["Longitude"].astype(float).to_numpy(),
    )

    corr = float(df["Distance_Km"].corr(df["Monthly_Revenue"].astype(float), method="pearson"))
    answer = f"{corr:.4f}"

    df.to_csv(base_dir / "with_distance.csv", index=False)
    (base_dir / "answer.txt").write_text(f"{answer}\n", encoding="utf-8")
    print(answer)


if __name__ == "__main__":
    main()

