# /// script
# requires-python = ">=3.11"
# dependencies = ["numpy", "scipy", "pyproj", "shapely"]
# ///

from __future__ import annotations

import json
from pathlib import Path

import numpy as np
from pyproj import Transformer
from scipy.spatial import Voronoi
from shapely.geometry import Polygon, box


def voronoi_finite_polygons_2d(vor: Voronoi, radius: float | None = None) -> tuple[list[list[int]], np.ndarray]:
    if vor.points.shape[1] != 2:
        raise ValueError("Requires 2D input points.")

    new_regions: list[list[int]] = []
    new_vertices = vor.vertices.tolist()

    center = vor.points.mean(axis=0)
    if radius is None:
        radius = np.ptp(vor.points, axis=0).max() * 2

    all_ridges: dict[int, list[tuple[int, int, int]]] = {}
    for (p1, p2), (v1, v2) in zip(vor.ridge_points, vor.ridge_vertices):
        all_ridges.setdefault(p1, []).append((p2, v1, v2))
        all_ridges.setdefault(p2, []).append((p1, v1, v2))

    for p1, region_idx in enumerate(vor.point_region):
        region = vor.regions[region_idx]
        if all(v >= 0 for v in region):
            new_regions.append(region)
            continue

        ridges = all_ridges[p1]
        new_region = [v for v in region if v >= 0]

        for p2, v1, v2 in ridges:
            if v2 < 0:
                v1, v2 = v2, v1
            if v1 >= 0:
                continue

            tangent = vor.points[p2] - vor.points[p1]
            tangent /= np.linalg.norm(tangent)
            normal = np.array([-tangent[1], tangent[0]])

            midpoint = vor.points[[p1, p2]].mean(axis=0)
            direction = np.sign(np.dot(midpoint - center, normal)) * normal
            far_point = vor.vertices[v2] + direction * radius

            new_region.append(len(new_vertices))
            new_vertices.append(far_point.tolist())

        verts = np.asarray([new_vertices[v] for v in new_region])
        centroid = verts.mean(axis=0)
        angles = np.arctan2(verts[:, 1] - centroid[1], verts[:, 0] - centroid[0])
        new_region = np.asarray(new_region)[np.argsort(angles)].tolist()
        new_regions.append(new_region)

    return new_regions, np.asarray(new_vertices)


def main() -> None:
    base_dir = Path(__file__).resolve().parent
    input_path = base_dir / "q-geospatial-qgis-gap.geojson"

    geojson = json.loads(input_path.read_text(encoding="utf-8"))
    coords = [
        tuple(feature["geometry"]["coordinates"])
        for feature in geojson.get("features", [])
        if feature.get("geometry", {}).get("type") == "Point"
    ]
    if not coords:
        raise RuntimeError("No point features found in input GeoJSON.")

    lon = np.array([c[0] for c in coords], dtype=float)
    lat = np.array([c[1] for c in coords], dtype=float)

    transformer = Transformer.from_crs("EPSG:4326", "EPSG:27700", always_xy=True)
    x, y = transformer.transform(lon, lat)
    points = np.column_stack([x, y])

    vor = Voronoi(points)
    regions, vertices = voronoi_finite_polygons_2d(vor)

    minx, miny = points.min(axis=0)
    maxx, maxy = points.max(axis=0)
    width = maxx - minx
    height = maxy - miny

    # Match QGIS Voronoi "buffer region" = 10%.
    buffer_pct = 0.10
    clipping_extent = box(
        minx - width * buffer_pct,
        miny - height * buffer_pct,
        maxx + width * buffer_pct,
        maxy + height * buffer_pct,
    )

    areas_km2 = []
    for region in regions:
        polygon = Polygon(vertices[region]).intersection(clipping_extent)
        areas_km2.append(polygon.area / 1_000_000.0)

    largest_area_km2 = max(areas_km2)
    answer = f"{largest_area_km2:.2f}"

    (base_dir / "areas_km2.txt").write_text(
        "\n".join(f"{i+1}: {a:.6f}" for i, a in enumerate(areas_km2)) + "\n",
        encoding="utf-8",
    )
    (base_dir / "answer.txt").write_text(f"{answer}\n", encoding="utf-8")
    print(answer)


if __name__ == "__main__":
    main()

