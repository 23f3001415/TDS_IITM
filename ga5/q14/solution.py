# /// script
# requires-python = ">=3.11"
# dependencies = ["pandas", "numpy"]
# ///

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

EARTH_RADIUS_KM = 6371.0


def haversine_matrix(order_lat: np.ndarray, order_lon: np.ndarray, wh_lat: np.ndarray, wh_lon: np.ndarray) -> np.ndarray:
    dlat = order_lat[:, None] - wh_lat[None, :]
    dlon = order_lon[:, None] - wh_lon[None, :]
    a = (
        np.sin(dlat / 2.0) ** 2
        + np.cos(order_lat)[:, None] * np.cos(wh_lat)[None, :] * np.sin(dlon / 2.0) ** 2
    )
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
    return EARTH_RADIUS_KM * c


def pick_warehouse_label_column(warehouses: pd.DataFrame) -> str:
    preferred = [
        "warehouse_name",
        "Warehouse_Name",
        "name",
        "warehouse",
        "Warehouse",
        "warehouse_id",
        "Warehouse_ID",
    ]
    for col in preferred:
        if col in warehouses.columns:
            return col
    return warehouses.columns[0]


def main() -> None:
    base_dir = Path(__file__).resolve().parent
    orders_path = base_dir / "q-geospatial-python-closest-orders.csv"
    warehouses_path = base_dir / "q-geospatial-python-closest-warehouses.csv"

    orders = pd.read_csv(orders_path)
    warehouses = pd.read_csv(warehouses_path)

    order_lat = np.radians(orders["latitude"].astype(float).to_numpy())
    order_lon = np.radians(orders["longitude"].astype(float).to_numpy())
    wh_lat = np.radians(warehouses["latitude"].astype(float).to_numpy())
    wh_lon = np.radians(warehouses["longitude"].astype(float).to_numpy())

    distances = haversine_matrix(order_lat, order_lon, wh_lat, wh_lon)
    nearest_idx = np.argmin(distances, axis=1)

    label_col = pick_warehouse_label_column(warehouses)
    assigned = warehouses.iloc[nearest_idx][label_col].to_numpy()
    counts = pd.Series(assigned).value_counts()

    busiest_warehouse = str(counts.index[0])
    busiest_count = int(counts.iloc[0])
    answer = f"{busiest_warehouse}, {busiest_count}"

    output = orders.copy()
    output["assigned_warehouse"] = assigned
    output.to_csv(base_dir / "assigned_orders.csv", index=False)
    (base_dir / "answer.txt").write_text(f"{answer}\n", encoding="utf-8")
    print(answer)


if __name__ == "__main__":
    main()

