# Model

- `DWF_HD_Setup.m21fm`: the MIKE 21 Flow Model FM (HD) setup file. It refers to the mesh, boundary conditions and wind forcing in [`../input`](../input) by relative paths, so the setup can be run directly from this folder once `input/wind.dfs2` has been downloaded.
- `DWF_HD_Setup.log`: log file from the benchmark simulation, with the parameter settings and run time.

The simulation writes `Area.dfsu` and `Points.dfs0`; the full results are on [Zenodo](https://doi.org/10.5281/zenodo.14929387) and a one-week extract is in [`../output_sample`](../output_sample).
