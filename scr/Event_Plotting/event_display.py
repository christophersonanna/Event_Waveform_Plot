import matplotlib.pyplot as plt
import numpy as np
import config
from data_structure import Event

def plot_event_display(event: Event):
    hits = event.hits
    num_hits = len(hits)
    
    # 1. Timing and Signal Calculations
    times = np.array([h.reltime for h in hits])
    t0 = np.min(times)
    rel_times = times - t0 
    
    # 2. Sort hits by time (Earliest first)
    # This ensures the first hit (index 0 of sorted) is handled first
    sorted_indices = np.argsort(rel_times)
    
    fig = plt.figure(figsize=(18, 10))
    
    # --- Left Plot: SD Array ---
    ax1 = fig.add_subplot(1, 2, 1)
    ew_hits = np.array([(h.xxyy // 100) for h in hits])
    ns_hits = np.array([(h.xxyy % 100) for h in hits])
    signals = np.array([np.sum(h.fadc0) for h in hits])
    
    # Background Grid (Standard TA 20x24 approx)
    grid_x, grid_y = np.meshgrid(np.arange(1, 21), np.arange(1, 25))
    ax1.scatter(grid_x, grid_y, s=2, c='gray', alpha=0.2, marker='.')
    
    sc = ax1.scatter(ew_hits, ns_hits, s=signals/10, c=rel_times, cmap='turbo', edgecolors='k')
    ax1.set_title(f"Event {event.event_id} Map")
    plt.colorbar(sc, ax=ax1, label="Time [µs]")

    # --- Right Plot: Stacked Waveforms ---
    ax2 = fig.add_subplot(1, 2, 2)
    time_bins = np.linspace(0, 25, 128) 
    
    # Define vertical spacing
    v_space = 80 
    # Total height of the stack
    total_height = num_hits * v_space

    for i, idx in enumerate(sorted_indices):
        h = hits[idx]
        
        # To put the FIRST hit on TOP:
        # i=0 (earliest) gets the maximum offset
        # i=num_hits (latest) gets the minimum offset
        offset = total_height - (i * v_space)
        
        # Color matching the time scale
        color = plt.cm.turbo(rel_times[idx] / (np.max(rel_times) + 1e-9))
        
        # Normalize waveform peak to fit within its vertical slice
        peak = np.max(h.fadc0)
        norm_wf = (h.fadc0 / peak * (v_space * 0.8)) if peak > 0 else h.fadc0
        
        # Plot: Shift X by rel_time, Shift Y by calculated offset
        ax2.plot(time_bins + rel_times[idx], norm_wf + offset, color=color, lw=1.5)
        
        # Labels: ID, MIP (Sum/10), and Distance
        mip = np.sum(h.fadc0) / 10.0
        label = f"SD{h.xxyy:04d}: {mip:.1f} MIP @ {h.radius:.1f}km"
        ax2.text(rel_times[idx] + 26, offset + 5, label, fontsize=8)

    ax2.set_xlim(-2, np.max(rel_times) + 45)
    ax2.set_ylim(-10, total_height + v_space)
    ax2.set_xlabel("Relative time [µs]")
    ax2.set_title(f"Date: {event.event_id}")
    ax2.get_yaxis().set_visible(False) # Hide arbitrary Y scale
    
    plt.tight_layout()
    plt.show()