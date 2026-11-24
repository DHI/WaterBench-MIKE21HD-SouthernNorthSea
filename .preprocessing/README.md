# Preprocessing

Notebooks and scripts that produced the data in `input/`, `observations/` and `output_sample/` from the raw sources. This folder is part of the GitHub repository only, not the Zenodo archive.

- `preprocess_wl_stations.ipynb`, `preprocess_currents.ipynb`, `preprocess_altimetry.ipynb`: download/read raw observation data (in `raw_data/`), apply quality filtering, and write intermediate CSV files and station lists to `observations_csv/`.
- `convert_observations_to_dfs0.py`: converts the CSV files in `observations_csv/` to one `.dfs0` per station and per altimetry mission in `observations/`, writes the station manifest `observations/stations.csv`, and checks the result. Run with `python .preprocessing/convert_observations_to_dfs0.py`.
- `add_stations.ipynb`: adds the Dover, Cromer and Lowestoft stations to the model result `Points.dfs0`.
- `subset_modelresult.ipynb`: makes the one-week extract in `output_sample/` from the full model output.
