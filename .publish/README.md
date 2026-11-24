# Publish

Material for publishing the case on [Zenodo](https://doi.org/10.5281/zenodo.14929387). This folder is part of the GitHub repository only, not the Zenodo archive.

- `zip_repo.py`: zips the repository for Zenodo, excluding hidden folders and `output/`.
- `zip_output_input.py`: zips the full model output and the wind input into separate archives, with `README_output.md` / `README_input.md` as their README files.
- `zenodo_text.md`: description text for the Zenodo record.
- `README.pdf`: rendered version of the main README.
- `checklist.md`: checklist for preparing a case for publishing.

The zip files are build outputs and are not committed (`*.zip` is in `.gitignore`). Run the scripts from the repository root.
