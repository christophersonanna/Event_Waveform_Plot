import numpy as np
from data_structure import Event, Hit
from aggregation import extract_event_features

def save_to_npz(events, filename):
    if not events: return
    print(f"--- Packaging {len(events)} events into {filename} ---")
    
    feats, meta = extract_event_features(events)
    hit_counts = np.array([len(e.hits) for e in events])
    all_hits = [h for e in events for h in e.hits]
    
    # Use standard savez (not compressed) for much faster I/O
    np.savez(
        filename,
        features=feats,
        xmax=np.array([m['xmax'] for m in meta]),
        energy=np.array([m['energy'] for m in meta]),
        particle=np.array([m['particle'] for m in meta]),
        ev_ids=np.array([e.event_id for e in events]),
        ev_phi=np.array([e.phi for e in events]),
        ev_theta=np.array([e.theta for e in events]),
        ev_xcore=np.array([e.xcore for e in events]),
        ev_ycore=np.array([e.ycore for e in events]),
        hit_counts=hit_counts,
        h_fadc0=np.array([h.fadc0 for h in all_hits]),
        h_xxyy=np.array([h.xxyy for h in all_hits]),
        h_radius=np.array([h.radius for h in all_hits]),
        h_reltime=np.array([h.reltime for h in all_hits]),
        h_isgood=np.array([h.isgood for h in all_hits]) # Save the actual isgood value
    )

def load_from_npz(filename):
    # mmap_mode='r' allows reading the file without loading everything into RAM
    data = np.load(filename, mmap_mode='r')
    events = []
    h_idx = 0
    
    # Pre-access arrays to speed up the reconstruction loop
    h_fadc = data['h_fadc0']
    h_xxyy = data['h_xxyy']
    h_rad = data['h_radius']
    h_time = data['h_reltime']
    h_good = data['h_isgood']
    counts = data['hit_counts']

    for i in range(len(data['ev_ids'])):
        num_hits = counts[i]
        end_idx = h_idx + num_hits
        
        # Fast list comprehension for hit reconstruction
        hits = [Hit(
            fadc0=h_fadc[j], fadc1=np.zeros(128),
            xxyy=int(h_xxyy[j]), radius=float(h_rad[j]),
            sstart=0.0, isgood=int(h_good[j]), 
            reltime=float(h_time[j]), timeerr=0.0
        ) for j in range(h_idx, end_idx)]
        
        events.append(Event(
            event_id=int(data['ev_ids'][i]), particle=int(data['particle'][i]),
            energy=float(data['energy'][i]), hits=hits, xmax=float(data['xmax'][i]),
            xcore=float(data['ev_xcore'][i]), ycore=float(data['ev_ycore'][i]),
            phi=float(data['ev_phi'][i]), theta=float(data['ev_theta'][i])
        ))
        h_idx = end_idx
    return events