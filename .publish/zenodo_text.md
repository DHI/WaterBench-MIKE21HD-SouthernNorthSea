# Hydrodynamic model of the Southern North Sea: MIKE21 model setup, outputs and observation data

## Description

**MIKE 21 Flow Model FM** is a hydrodynamic modeling system based on a flexible mesh approach, used for oceanographic, coastal, and estuarine applications. This repository includes a highly simplified model setup and 2-year simulation results for a region in the Southern North Sea, as well as observational data and code for model validation.

This dataset is part of the **WaterBench** series by DHI, supporting open research on water-related challenges. It is intended for **educational and research purposes only**, such as model validation, parameter calibration, and machine learning applications. The model mesh has been reduced from over 150,000 to ~8,000 elements compared to our operational model, and inputs are coarser in time and space, resulting in increased error (e.g., typical RMSE in water levels increases from ~8 cm to 15–20 cm). **Results must not be used for decision-making.**

Files:

* **README**. Description of dataset with details on citations, data processing, and background information. 
* **WaterBench-MIKE21HD-SouthernNorthSea.zip**: model setup, input data (e.g., boundary conditions, wind), observational data, and code for data exploration and model validation. 
* **MIKE21HD-SouthernNorthSea-output.zip**: 2-years model result files `Area.dfsu` and `Points.dfs0` (~4 GB).
* **MIKE21HD-SouthernNorthSea-input.zip**: wind input data for the model(~0.5 GB).


## DOI

10.5281/zenodo.14929387

## Contributors

* Freja Petersen
* Jesper Sandvig Mariegaard

## Publication date

2025-03-31

## Funding

Danish Ministry of Higher Education and Science

## Software

https://github.com/DHI/WaterBench-MIKE21HD-SouthernNorthSea