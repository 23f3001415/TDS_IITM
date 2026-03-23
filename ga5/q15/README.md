# Q15: QGIS - Largest Voronoi Service Area

## ELI15 Step-by-Step (Complete Beginner)

1. Load the school points GeoJSON in QGIS.
2. Reproject points to a projected CRS (`EPSG:27700`) so area units are in metres.
3. Run `Voronoi Polygons` with buffer region set to at least `10%`.
4. Add area field in km² using:
   `$area / 1000000`
5. Sort area descending.
6. Largest polygon area is the answer (round to 2 decimals).

## Equivalent Python Solver

- `solution.py` reproduces the same logic:
  - Reproject to `EPSG:27700`
  - Voronoi polygons
  - Clip using 10% buffered extent
  - Compute area in km² and pick max

## Files in This Folder

- `q-geospatial-qgis-gap.geojson`: input points
- `solution.py`: Voronoi largest-area calculator
- `areas_km2.txt`: all polygon areas in km²
- `answer.txt`: final largest area

## Run

```powershell
cd C:\Users\sriva\OneDrive\Documents\TDS\ga5\q15
uv run solution.py
```

## Final Answer

`77.70`
