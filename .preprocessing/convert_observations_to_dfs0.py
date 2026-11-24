"""Convert the observation CSV files to .dfs0 and build the station manifest.

Input  (written by the preprocess_*.ipynb notebooks in this folder):
    .preprocessing/observations_csv/<station_id>_wl.csv      water level
    .preprocessing/observations_csv/<station_id>_u_v.csv     current velocity
    .preprocessing/observations_csv/Altimetry_wl_<sat>.csv   altimetry track
    .preprocessing/observations_csv/stations.csv             water-level station positions
    .preprocessing/observations_csv/current_stations.csv     current station positions

Output (WaterBench STRUCTURE.md, section 8):
    observations/<station_id>.dfs0     one file per station
    observations/Altimetry_<sat>.dfs0  one track file per satellite mission
    observations/stations.csv          station manifest

Each station file holds every variable observed at that station as a separate
item tagged with its EUM item type and unit:

- water level -> items 'water_level_filtered', 'water_level_raw'
                 (EUM Surface Elevation [m]; the series are mean-subtracted,
                 so the type matches the model output item 'Surface elevation')
- currents    -> items 'u', 'v' (EUM u/v velocity component [m/s])

Altimetry track files hold the items 'longitude', 'latitude' (EUM
Latitude/longitude [degree]), 'water_level' (EUM Surface Elevation [m]) and
'quality_water_level' (quality flag: 0 = good, 1 = acceptable).

Values are written as float64, so the conversion is lossless. Missing values
(NaN) are stored as delete values. After writing, the script re-reads each file
and checks it against the source CSV, and checks that the manifest and the
station files match one to one.

Run from the repository root or from .preprocessing/:

    python .preprocessing/convert_observations_to_dfs0.py
"""

from __future__ import annotations

from pathlib import Path

import mikeio
import numpy as np
import pandas as pd
from mikeio import EUMType, EUMUnit, ItemInfo

REPO = Path(__file__).resolve().parent.parent
CSV_DIR = REPO / ".preprocessing" / "observations_csv"
OBS_DIR = REPO / "observations"
MANIFEST = OBS_DIR / "stations.csv"
SOURCE_MANIFESTS = [CSV_DIR / "stations.csv", CSV_DIR / "current_stations.csv"]

CRS = "EPSG:4326"
DATUM_WL = "Mean-subtracted zero reference (absolute vertical datum not retained)"
DATUM_NONE = "Not applicable (no water-level observations)"

# filename suffix -> {csv column: (EUM type, EUM unit)}
VARIABLES = {
    "_wl": {
        "water_level_filtered": (EUMType.Surface_Elevation, EUMUnit.meter),
        "water_level_raw": (EUMType.Surface_Elevation, EUMUnit.meter),
    },
    "_u_v": {
        "u": (EUMType.u_velocity_component, EUMUnit.meter_per_sec),
        "v": (EUMType.v_velocity_component, EUMUnit.meter_per_sec),
    },
}

ALTIMETRY_PREFIX = "Altimetry_wl_"
ALTIMETRY_ITEMS = {
    "longitude": (EUMType.Latitude_longitude, EUMUnit.degree),
    "latitude": (EUMType.Latitude_longitude, EUMUnit.degree),
    "water_level": (EUMType.Surface_Elevation, EUMUnit.meter),
    "quality_water_level": (EUMType.Undefined, EUMUnit.undefined),
}


def split_name(csv_path: Path) -> tuple[str, str]:
    """'Cromer_wl.csv' -> ('Cromer', '_wl'); 'MO_NN_u_v.csv' -> ('MO_NN', '_u_v')."""
    stem = csv_path.stem
    for suffix in VARIABLES:
        if stem.endswith(suffix):
            return stem[: -len(suffix)], suffix
    raise ValueError(f"Unrecognised observation file name: {csv_path.name}")


def read_csv(csv_path: Path, columns: list[str], unique_time: bool = True) -> pd.DataFrame:
    df = pd.read_csv(csv_path, index_col=0)
    df.index = pd.to_datetime(df.index, format="ISO8601")
    missing = set(columns) - set(df.columns)
    if missing:
        raise ValueError(f"{csv_path.name}: missing columns {sorted(missing)}")
    if not df.index.is_monotonic_increasing:
        raise ValueError(f"{csv_path.name}: time index not increasing")
    if unique_time and df.index.has_duplicates:
        raise ValueError(f"{csv_path.name}: duplicate time stamps")
    return df[columns].astype("float64")


def collect_station_sources() -> dict[str, list[tuple[Path, str]]]:
    """station_id -> list of (csv file, variable suffix)."""
    sources: dict[str, list[tuple[Path, str]]] = {}
    for csv_path in sorted(CSV_DIR.glob("*.csv")):
        if csv_path in SOURCE_MANIFESTS or csv_path.name.startswith(ALTIMETRY_PREFIX):
            continue
        sid, suffix = split_name(csv_path)
        sources.setdefault(sid, []).append((csv_path, suffix))
    if not sources:
        raise FileNotFoundError(f"No station CSV files found in {CSV_DIR}")
    return sources


def build_frame(files: list[tuple[Path, str]]) -> tuple[pd.DataFrame, list[ItemInfo]]:
    """Combine all variables of one station on a common (outer-joined) time axis."""
    frames, items = [], []
    for csv_path, suffix in files:
        spec = VARIABLES[suffix]
        frames.append(read_csv(csv_path, list(spec)))
        items += [ItemInfo(col, etype, eunit) for col, (etype, eunit) in spec.items()]
    df = pd.concat(frames, axis=1, join="outer").sort_index()
    if df.columns.has_duplicates:
        raise ValueError(f"Duplicate variables for one station: {list(df.columns)}")
    return df, items


def write_dfs0(df: pd.DataFrame, items: list[ItemInfo], fn: Path) -> None:
    """Write a non-equidistant calendar .dfs0 (float64 items).

    Written with mikecore rather than mikeio's Dataset.to_dfs, because the dfs
    header stores the start time to whole seconds only: mikeio anchors the
    time axis at the first time step, so sub-second tracks (altimetry) would
    be shifted by the fractional part of their first time stamp. Anchoring the
    axis at the whole second and storing every step as a float offset keeps
    the time stamps exact.
    """
    from mikecore.DfsFactory import DfsBuilder, DfsFactory
    from mikecore.DfsFile import DataValueType, DfsSimpleType, StatType
    from mikecore.eum import eumQuantity
    from mikeio.eum import TimeStepUnit

    start = df.index[0].floor("s")
    factory = DfsFactory()
    builder = DfsBuilder.Create(fn.stem, "convert_observations_to_dfs0.py", 1)
    builder.SetDataType(1)
    builder.SetGeographicalProjection(factory.CreateProjectionUndefined())
    builder.SetTemporalAxis(
        factory.CreateTemporalNonEqCalendarAxis(TimeStepUnit.SECOND, start.to_pydatetime())
    )
    builder.SetItemStatisticsType(StatType.RegularStat)
    for item in items:
        ib = builder.CreateDynamicItemBuilder()
        ib.Set(item.name, eumQuantity.Create(item.type, item.unit), DfsSimpleType.Double)
        ib.SetValueType(DataValueType.Instantaneous)
        ib.SetAxis(factory.CreateAxisEqD0())
        builder.AddDynamicItem(ib.GetDynamicItemInfo())
    builder.CreateFile(str(fn))
    dfs = builder.GetFile()

    data = df[[item.name for item in items]].to_numpy(dtype=np.float64, copy=True)
    data[np.isnan(data)] = dfs.FileInfo.DeleteValueDouble
    t_seconds = (df.index - start).total_seconds().to_numpy()
    dfs.WriteDfs0DataDouble(np.column_stack([t_seconds, data]))
    dfs.Close()


def verify(df: pd.DataFrame, items: list[ItemInfo], fn: Path) -> None:
    ds = mikeio.read(fn)
    assert ds.n_timesteps == len(df), f"{fn.name}: time step count differs"
    assert (ds.time == df.index).all(), f"{fn.name}: time axis differs"
    for item in items:
        got = ds[item.name]
        assert got.type == item.type, f"{fn.name}/{item.name}: EUM type {got.type}"
        assert got.unit == item.unit, f"{fn.name}/{item.name}: EUM unit {got.unit}"
        assert np.allclose(
            got.to_numpy(), df[item.name].to_numpy(), equal_nan=True, rtol=0, atol=0
        ), f"{fn.name}/{item.name}: values differ from CSV"


def build_manifest(sources: dict[str, list[tuple[Path, str]]]) -> pd.DataFrame:
    """One variable-agnostic row per station, from the per-variable source manifests."""
    positions = pd.concat(
        [pd.read_csv(fn, index_col=0) for fn in SOURCE_MANIFESTS if fn.exists()]
    )
    positions.index = positions.index.astype(str)
    if positions.index.has_duplicates:
        raise ValueError(
            f"Station listed twice in source manifests: "
            f"{sorted(set(positions.index[positions.index.duplicated()]))}"
        )
    manifest = pd.DataFrame(
        {
            "station_id": positions.index,
            "lon": positions["Longitude"].to_numpy(),
            "lat": positions["Latitude"].to_numpy(),
            "crs": CRS,
            "vertical_datum": [
                DATUM_WL if any(s == "_wl" for _, s in sources.get(sid, [])) else DATUM_NONE
                for sid in positions.index
            ],
        }
    )
    return manifest


def check_manifest(station_ids: set[str]) -> None:
    """Bidirectional referential integrity: manifest rows <-> .dfs0 files."""
    manifest_ids = set(pd.read_csv(MANIFEST)["station_id"].astype(str))
    dfs0_ids = {p.stem for p in OBS_DIR.glob("*.dfs0") if not p.name.startswith("Altimetry_")}
    problems = []
    if manifest_ids - dfs0_ids:
        problems.append(f"manifest rows without .dfs0: {sorted(manifest_ids - dfs0_ids)}")
    if dfs0_ids - manifest_ids:
        problems.append(f".dfs0 files without manifest row: {sorted(dfs0_ids - manifest_ids)}")
    if station_ids - manifest_ids:
        problems.append(f"converted stations not in manifest: {sorted(station_ids - manifest_ids)}")
    if problems:
        raise ValueError("stations.csv is out of sync: " + "; ".join(problems))


def convert_stations() -> set[str]:
    sources = collect_station_sources()
    for sid, files in sources.items():
        df, items = build_frame(files)
        fn = OBS_DIR / f"{sid}.dfs0"
        write_dfs0(df, items, fn)
        verify(df, items, fn)
        names = ", ".join(i.name for i in items)
        print(f"{fn.relative_to(REPO)}: {len(df)} time steps "
              f"({df.index[0]} - {df.index[-1]}), items [{names}]")
    build_manifest(sources).to_csv(MANIFEST, index=False)
    check_manifest(set(sources))
    return set(sources)


def convert_altimetry() -> int:
    """One track .dfs0 per satellite mission. Tracks may repeat a time stamp."""
    files = sorted(CSV_DIR.glob(f"{ALTIMETRY_PREFIX}*.csv"))
    items = [ItemInfo(c, t, u) for c, (t, u) in ALTIMETRY_ITEMS.items()]
    for csv_path in files:
        mission = csv_path.stem[len(ALTIMETRY_PREFIX):]
        df = read_csv(csv_path, list(ALTIMETRY_ITEMS), unique_time=False)
        fn = OBS_DIR / f"Altimetry_{mission}.dfs0"
        write_dfs0(df, items, fn)
        verify(df, items, fn)
        print(f"{fn.relative_to(REPO)}: {len(df)} points "
              f"({df.index[0]} - {df.index[-1]})")
    return len(files)


def main() -> None:
    OBS_DIR.mkdir(exist_ok=True)
    n_stations = len(convert_stations())
    n_tracks = convert_altimetry()
    print(f"OK: {n_stations} station files and {n_tracks} altimetry track files "
          "written and verified; stations.csv in sync.")


if __name__ == "__main__":
    main()
