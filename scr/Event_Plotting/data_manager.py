import numpy as np
import os
from glob import glob
from load import load_and_transform
from aggregation import extract_event_features
from data_structure import Event, Hit

def save_to_npz(events, filename):
    if not events:
        print("Warning: No events to save.")
        return

    print(f"--- Packaging {len(events)} events into {filename} ---")
    
    # Identical to your previous project's extraction
    feats, meta = extract_event_features(events)
    
    # Event-level metadata (New for plotting)
    ev_ids = np.array([e.event_id for e in events])
    ev_phi = np.array([e.phi for e in events])
    ev_theta = np.array([e.theta for e in events])
    ev_xcore = np.array([e.xcore for e in events])
    ev_ycore = np.array([e.ycore for e in events])
    
    # Hit-level data (New for plotting)
    hit_counts = np.array([len(e.hits) for e in events])
    all_hits = [h for e in events for h in e.hits]
    
    h_fadc0 = np.array([h.fadc0 for h in all_hits])
    h_xxyy = np.array([h.xxyy for h in all_hits])
    h_h_radius = np.array([h.radius for h in all_hits]) # renamed to avoid conflict
    h_reltime = np.array([h.reltime for h in all_hits])

    # np.savez_compressed with identical keys from your processor.py
    np.savez_compressed(
        filename,
        # Keys for PCA Project Compatibility
        features=feats,
        xmax=np.array([m['xmax'] for m in meta]),
        energy=np.array([m['energy'] for m in meta]),
        particle=np.array([m['particle'] for m in meta]),
        radius=np.array([m['radius'] for m in meta]),
        # Keys for Plotting Project
        ev_ids=ev_ids,
        ev_phi=ev_phi, ev_theta=ev_theta,
        ev_xcore=ev_xcore, ev_ycore=ev_ycore,
        hit_counts=hit_counts,
        h_fadc0=h_fadc0, h_xxyy=h_xxyy,
        h_h_radius=h_h_radius, h_reltime=h_reltime
    )
    print(f"Done. File saved as {filename}")

def load_from_npz(filename):
    data = np.load(filename)
    if 'h_fadc0' not in data:
        raise KeyError("This NPZ doesn't contain hit data for plotting.")
    
    events = []
    h_idx = 0
    for i in range(len(data['ev_ids'])):
        num_hits = data['hit_counts'][i]
        hits = []
        for _ in range(num_hits):
            hits.append(Hit(
                fadc0=data['h_fadc0'][h_idx], fadc1=np.zeros(128),
                xxyy=int(data['h_xxyy'][h_idx]), radius=float(data['h_h_radius'][h_idx]),
                sstart=0.0, isgood=1, reltime=float(data['h_reltime'][h_idx]), timeerr=0.0
            ))
            h_idx += 1
        
        events.append(Event(
            event_id=int(data['ev_ids'][i]), particle=int(data['particle'][i]),
            energy=float(data['energy'][i]), hits=hits, xmax=float(data['xmax'][i]),
            xcore=float(data['ev_xcore'][i]), ycore=float(data['ev_ycore'][i]),
            phi=float(data['ev_phi'][i]), theta=float(data['ev_theta'][i])
        ))
    return events