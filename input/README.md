# Input

Input data for the MIKE 21 HD model setup in [`../model`](../model):

- `Mesh_8000_elems_HD_v2.mesh`: flexible mesh (about 8,000 triangular elements) with bathymetry interpolated to the mesh nodes.
- `IJV_BC_North_downsampled.dfs1`, `IJV_BC_South_downsampled.dfs1`: water level and current velocities on the North and South open boundaries.
- `wind.dfs2`: wind velocities and air pressure. The file is too large for GitHub and is not stored in this repository; download `MIKE21HD-SouthernNorthSea-input.zip` from [Zenodo](https://doi.org/10.5281/zenodo.14929387) and place `wind.dfs2` in this folder before running the model.
