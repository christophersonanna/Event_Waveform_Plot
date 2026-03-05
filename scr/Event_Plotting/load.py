#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import awkward as ak
import numpy as np
import config
import matplotlib.pyplot as plt
from data_structure import Hit, Event

def load_and_transform(file_path: str) -> list[Event]:
    print(f"Reading TA Parquet: {file_path}")
    data = ak.from_parquet(file_path)
    events_list = []

    for row in data:
        # Access the specific TA branches
        sl = row.showlib     # Simulation truth (xmax, energy, particle)
        dr = row.rusdraw    # Raw SD data (fadc, xxyy)
        fp = row.rufptn     # Timing/Pattern (reltime, isgood)
        gm = row.rusdgeom   # Geometry (xcore, ycore)

        event_hits = []
        
        # In this schema, 'xxyy' is the reliable length for hits in the SD
        num_hits = len(dr.xxyy)
        
        for i in range(num_hits):
            # 1. Geometry - 
            x_c = gm.xcore[0] if hasattr(gm.xcore, "__len__") else gm.xcore
            y_c = gm.ycore[0] if hasattr(gm.ycore, "__len__") else gm.ycore
            
            xy = dr.xxyy[i]
            dx = (xy // 100) - x_c
            dy = (xy % 100) - y_c
            dist_km = np.sqrt(dx**2 + dy**2) * config.GRID_TO_KM

            # 2. FADC - Structure is var * var * var (Hit -> Pulse -> Bins)
            try:
                wave = np.array(dr.fadc[i][0]) 
                if len(wave) < 128:
                    # Pad with zeros if it's shorter than 128
                    padded = np.zeros(128)
                    padded[:len(wave)] = wave[:128]
                    wave = padded
                else:
                    wave = wave[:128] # Truncate if longer
            except (IndexError, ValueError):
                continue # Skip hit if no FADC pulse found

            # 3. Pattern/Timing - These are also nested var * var
            try:
                hit_is_good = fp.isgood[i] # This looks like var * int
                hit_sstart = fp.sstart[i][0]
                hit_reltime = fp.reltime[i][0]
                hit_timeerr = fp.timeerr[i][0]
            except (IndexError, ValueError):
                continue

            event_hits.append(Hit(
                fadc0=wave, fadc1=np.zeros(128),
                xxyy=int(xy), radius=float(dist_km),
                sstart=float(hit_sstart), isgood=int(hit_is_good),
                reltime=float(hit_reltime), timeerr=float(hit_timeerr)
            ))

        if len(event_hits) > 0:
            events_list.append(Event(
                event_id=int(dr.event_num),
                particle=int(sl.particle),
                energy=float(np.log10(sl.energy)) if sl.energy > 0 else 0.0,
                hits=event_hits,
                xcore=float(x_c), ycore=float(y_c),
                xmax=float(sl.xmax),
                phi=float(gm.phi[0]) if hasattr(gm.phi, "__len__") else float(gm.phi),
                theta=float(gm.theta[0]) if hasattr(gm.theta, "__len__") else float(gm.theta)
            ))

    print(f"Successfully Loaded {len(events_list)} events.")
    return events_list

import os
from glob import glob

def get_file_list(input_paths, n_step=1):
    """
    Gathers all .parquet files from a list of files or directories.
    n_step allows for skipping files to speed up testing.
    """
    all_files = []
    for path in input_paths:
        if os.path.isdir(path):
            all_files.extend(glob(os.path.join(path, "*.parquet")))
        elif os.path.isfile(path):
            all_files.append(path)
            
    # Sort for consistency and apply n_step skip
    all_files = sorted(all_files)[::n_step]
    
    if not all_files:
        print(f"Warning: No files found in paths: {input_paths}")
        
    return all_files

if __name__ == "__main__":
    main()
    plt.show(block=True)