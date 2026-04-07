import matplotlib.pyplot as plt
import numpy as np
import config
from data_structure import Event

def plot_event_display(event: Event):
    # 1. Apply the 'isgood' cut immediately
    # This filters out detectors that didn't pass the pattern/timing quality checks
    valid_hits = [h for h in event.hits if h.isgood >= 3]
    
    if not valid_hits:
        print(f"Skipping Event {event.event_id}: No 'isgood' hits found.")
        return

    num_hits = len(valid_hits)
    
    # 2. Timing and Signal Calculations using valid_hits
    times = np.array([h.reltime for h in valid_hits])
    t0 = np.min(times)
    rel_times = times - t0 
    
    # Sort hits by time (Earliest first) for the stack
    sorted_indices = np.argsort(rel_times)
    
    fig = plt.figure(figsize=(18, 10))
    
    # --- Left Plot: SD Array ---
    ax1 = fig.add_subplot(1, 2, 1)
    ew_hits = np.array([(h.xxyy // 100) for h in valid_hits])
    ns_hits = np.array([(h.xxyy % 100) for h in valid_hits])
    # Summing FADC bins to estimate total signal strength
    signals = np.array([np.sum(h.fadc0) for h in valid_hits])
    
    # Background Grid (Reference Dots)
    grid_x, grid_y = np.meshgrid(np.arange(1, 21), np.arange(1, 25))
    ax1.scatter(grid_x, grid_y, s=2, c='gray', alpha=0.2, marker='.')
    
    sc = ax1.scatter(ew_hits, ns_hits, s=signals/10, c=rel_times, cmap='turbo', edgecolors='k')
    ax1.set_title(f"Event {event.event_id} Map")
    plt.colorbar(sc, ax=ax1, label="Time [µs]")

    # --- Right Plot: Stacked Waveforms (First Hit on Top) ---
    ax2 = fig.add_subplot(1, 2, 2)
    # 128 bins per FADC waveform defined in config
    time_bins = np.linspace(0, 25, config.WAVEFORM_BINS) 
    
    v_space = 80 
    total_height = num_hits * v_space

    for i, idx in enumerate(sorted_indices):
        h = valid_hits[idx]
        
        # Chronological Offset: Early hits at high Y values
        offset = total_height - (i * v_space)
        
        # Color matching the time scale on the map
        color = plt.cm.turbo(rel_times[idx] / (np.max(rel_times) + 1e-9))
        
        # Normalize waveform peak to fit within its vertical slice
        peak = np.max(h.fadc0)
        norm_wf = (h.fadc0 / peak * (v_space * 0.8)) if peak > 0 else h.fadc0
        
        # Plotting the trace with the timing shift (rel_times)
        ax2.plot(time_bins + rel_times[idx], norm_wf + offset, color=color, lw=1.5)
        
        # Annotations: ID and Distance from core (calculated in load.py)
        label = f"SD{h.xxyy:04d}: {h.radius:.1f} km"
        ax2.text(rel_times[idx] + 26, offset + 5, label, fontsize=8)

    ax2.set_xlim(-2, np.max(rel_times) + 40)
    ax2.set_ylim(-10, total_height + v_space)
    ax2.set_xlabel("Relative time from earliest detector [µs]")
    ax2.get_yaxis().set_visible(False)
    
    plt.tight_layout()
    plt.show()
    #print(f"SD{h.xxyy:04d}: {h.isgood}")
    print(rel_times)