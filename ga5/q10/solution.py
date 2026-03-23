# /// script
# requires-python = ">=3.11"
# dependencies = ["pandas", "numpy"]
# ///

from __future__ import annotations

from collections import Counter
from pathlib import Path

import numpy as np
import pandas as pd

EARTH_RADIUS_KM = 6371.0
WAREHOUSES = {
    "Delhi": (28.6139, 77.209),
    "Mumbai": (19.076, 72.8777),
    "Chennai": (13.0827, 80.2707),
}


def haversine_vectorized(lat1: float, lon1: float, lat2: np.ndarray, lon2: np.ndarray) -> np.ndarray:
    lat1r = np.radians(lat1)
    lon1r = np.radians(lon1)
    lat2r = np.radians(lat2)
    lon2r = np.radians(lon2)

    dlat = lat2r - lat1r
    dlon = lon2r - lon1r

    a = np.sin(dlat / 2.0) ** 2 + np.cos(lat1r) * np.cos(lat2r) * np.sin(dlon / 2.0) ** 2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
    return EARTH_RADIUS_KM * c


def main() -> None:
    base_dir = Path(__file__).resolve().parent
    input_path = base_dir / "q-geospatial-nearest-warehouse.csv"
    df = pd.read_csv(input_path)

    lat = df["Latitude"].astype(float).to_numpy()
    lon = df["Longitude"].astype(float).to_numpy()

    for name, (wlat, wlon) in WAREHOUSES.items():
        df[f"Distance_{name}_Km"] = haversine_vectorized(wlat, wlon, lat, lon)

    distance_cols = [f"Distance_{name}_Km" for name in WAREHOUSES]
    df["Assigned_Warehouse"] = (
        df[distance_cols]
        .idxmin(axis=1)
        .str.replace("Distance_", "", regex=False)
        .str.replace("_Km", "", regex=False)
    )

    counts = Counter(df["Assigned_Warehouse"])
    busiest, count = max(counts.items(), key=lambda x: x[1])
    answer = f"{busiest}, {count}"

    df.to_csv(base_dir / "assigned_deliveries.csv", index=False)
    (base_dir / "answer.txt").write_text(f"{answer}\n", encoding="utf-8")
    print(answer)


if __name__ == "__main__":
    main()

