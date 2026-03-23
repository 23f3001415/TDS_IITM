# /// script
# requires-python = ">=3.11"
# dependencies = ["pandas", "numpy"]
# ///

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

EARTH_RADIUS_KM = 6371.0


def main() -> None:
    base_dir = Path(__file__).resolve().parent
    input_path = base_dir / "rideshare_trips.csv"

    df = pd.read_csv(input_path)
    df["start_time"] = pd.to_datetime(df["start_time"], format="ISO8601", utc=True)
    df["hour"] = df["start_time"].dt.hour

    # Step A: peak hours 17:00-20:59 UTC
    peak = df[(df["hour"] >= 17) & (df["hour"] < 21)].copy()

    # Step B: Haversine distance > 7 km
    lat1 = np.radians(peak["pickup_lat"].astype(float).to_numpy())
    lon1 = np.radians(peak["pickup_lon"].astype(float).to_numpy())
    lat2 = np.radians(peak["dropoff_lat"].astype(float).to_numpy())
    lon2 = np.radians(peak["dropoff_lon"].astype(float).to_numpy())

    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = np.sin(dlat / 2.0) ** 2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2.0) ** 2
    peak["dist_km"] = EARTH_RADIUS_KM * 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))

    long_trips = peak[peak["dist_km"] > 7].copy()

    # Step C: top driver by summed fare
    revenue_by_driver = (
        long_trips.groupby("driver_id", as_index=True)["fare_amount"].sum().sort_values(ascending=False)
    )
    top_driver = str(revenue_by_driver.index[0])
    top_fare = float(revenue_by_driver.iloc[0])

    answer = f"{top_driver}, {top_fare:.2f}"
    long_trips.to_csv(base_dir / "qualifying_trips.csv", index=False)
    (base_dir / "answer.txt").write_text(f"{answer}\n", encoding="utf-8")
    print(answer)


if __name__ == "__main__":
    main()

