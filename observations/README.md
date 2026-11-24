# Observations

Observation data for validation of the model (see the `code/model_validation_*.ipynb` notebooks).

- One `.dfs0` file per station, named `<station_id>.dfs0`. Each variable observed at a station is an item in its file, tagged with its EUM item type and unit:
  - Water level stations: items `water_level_filtered` and `water_level_raw` (Surface Elevation, m). The series are mean-subtracted, i.e. relative to a zero mean rather than an absolute vertical datum.
  - `MO_NN` (currents): items `u` and `v` (u/v velocity component, m/s), depth-averaged.
- `stations.csv` is the station manifest, with one row per station: `station_id` (matches the `.dfs0` file name), `lon`, `lat`, `crs` (`EPSG:4326`) and `vertical_datum`.
- One altimetry track file per satellite mission, named `Altimetry_<mission>.dfs0` (`3a`, `3b`, `6a`, `c2`, `j3`, `sa`). Items: `longitude`, `latitude` (degrees, EPSG:4326), `water_level` (Surface Elevation, m) and `quality_water_level` (0 = good, 1 = acceptable). Altimetry tracks are not listed in `stations.csv`.

The `.dfs0` files and `stations.csv` are produced from the CSV files in `.preprocessing/observations_csv/` by `.preprocessing/convert_observations_to_dfs0.py`.
