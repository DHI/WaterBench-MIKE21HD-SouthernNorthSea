import warnings
from pathlib import Path

import mikeio
import modelskill as ms
import pandas as pd

obs_fldr = Path("../observations")
# One row per station; station_id matches the observations/<station_id>.dfs0 file name.
df_stn = pd.read_csv(obs_fldr / "stations.csv", index_col="station_id")


def _point_obs(eum_type, item=None):
    """PointObservations for every station whose .dfs0 has an item of the given EUM type.

    If `item` is given, that item is used; otherwise all items of `eum_type` are
    returned. The quantity (name + unit) is taken from the EUM item info.
    """
    obs = []
    for sid, row in df_stn.iterrows():
        ds = mikeio.read(obs_fldr / f"{sid}.dfs0")
        names = [it.name for it in ds.items if it.type == eum_type]
        if item is not None:
            names = [n for n in names if n == item]
        for name in names:
            da = ds[name].dropna()
            obs.append(ms.PointObservation(da, x=row["lon"], y=row["lat"], name=sid))
    return obs


def get_wl_point_obs():
    """Get water level point observations as list of PointObservation objects"""
    return _point_obs(mikeio.EUMType.Surface_Elevation, item="water_level_filtered")


def get_u_v_point_obs():
    """Get current point observations as two lists of PointObservation objects"""
    ulist = _point_obs(mikeio.EUMType.u_velocity_component)
    vlist = _point_obs(mikeio.EUMType.v_velocity_component)
    return ulist, vlist


def get_altimetry_obs(quality=None):
    """Get altimetry observations as list of TrackObservation objects (one per satellite).

    quality: keep only points with this quality_water_level flag
             (0 = good, 1 = acceptable); None keeps all points.
    """
    q = ms.Quantity(name="Surface Elevation", unit="meter")
    altlist = []
    for fn in sorted(obs_fldr.glob("Altimetry_*.dfs0")):
        mission = fn.stem.split("_", 1)[1]
        df = mikeio.read(fn).to_dataframe()
        if quality is not None:
            df = df[df.quality_water_level == quality]

        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", message=".*duplicate timestamps.*")
            o = ms.TrackObservation(df, item="water_level", x_item="longitude", y_item="latitude", name=mission, quantity=q)
        altlist.append(o)
    return altlist
