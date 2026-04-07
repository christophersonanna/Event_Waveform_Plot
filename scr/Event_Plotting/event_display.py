import matplotlib.pyplot as plt
import numpy as np
import config
from data_structure import Event

def plot_event_display(event: Event, min_isgood=3):
    # Filter hits by quality cut
    valid_hits = [h for h in event.hits if h.isgood >= min_isgood]
    if not valid_hits:
        print(f"No hits pass isgood >= {min_isgood}")
        return

    rel_times = np.array([h.reltime for h in valid_hits])
    rel_times -= np.min(rel_times)
    sorted_idx = np.argsort(rel_times)
    
    # Layout: Info (top-left), Array (bottom-left), Waveforms (right)
    fig = plt.figure(figsize=(22, 13))
    gs = fig.add_gridspec(2, 2, height_ratios=[1.2, 6], width_ratios=[1, 1.4], hspace=0.1)
    
    ax_info = fig.add_subplot(gs[0, 0])
    ax_array = fig.add_subplot(gs[1, 0])
    ax_wave = fig.add_subplot(gs[:, 1])

    # --- Top Left: Event Information (Clean floating text) ---
    ax_info.set_axis_off() # Removes the box and all axis labels/ticks
    
    # Fix Zenith: Convert from milliradians to degrees if value is > 180
    zenith_deg = np.degrees(event.theta)
    if zenith_deg > 180:
        zenith_deg = np.degrees(event.theta / 1000.0)

    info_text = (f"Event ID: {event.event_id}\n"
                 f"Energy: $10^{{{event.energy:.2f}}}$ eV\n"
                 f"Zenith: {zenith_deg:.1f}°")
    
    # Text placement at (0, 0.5) inside the invisible info subplot
    ax_info.text(0.0, 0.5, info_text, fontsize=14, weight='bold', 
                 va='center', ha='left', linespacing=1.6)

    # --- Bottom Left: Footprint & Shower Front ---
    gx, gy = np.meshgrid(np.arange(1, 21), np.arange(1, 25))
    ax_array.scatter(gx, gy, s=6, c='royalblue', alpha=0.3, marker='o') 
    
    ew = np.array([h.xxyy // 100 for h in valid_hits])
    ns = np.array([h.xxyy % 100 for h in valid_hits])
    sigs = np.array([np.sum(h.fadc0) for h in valid_hits])
    
    point_sizes = (np.log10(sigs + 1) * 35) 
    ax_array.scatter(ew, ns, s=point_sizes, c=rel_times, cmap='turbo', edgecolors='k', zorder=3)
    
    dx, dy = np.cos(event.phi), np.sin(event.phi)
    ax_array.arrow(event.xcore, event.ycore, dx*3.5, dy*3.5,
                   head_width=0.6, head_length=0.8, color='k', zorder=5)
    
    # Shower Front Line
    f_scale = 1.2
    ax_array.plot([event.xcore - dy*f_scale, event.xcore + dy*f_scale], 
                  [event.ycore + dx*f_scale, event.ycore - dx*f_scale], color='k', lw=2, zorder=4)

    for spine in ['top', 'right']:
        ax_array.spines[spine].set_visible(False)
    ax_array.set_aspect('equal')
    ax_array.set_xlabel("East-West [XX]")
    ax_array.set_ylabel("North-South [YY]")

    # --- Right Plot: Waveforms (Y-axis starts at 0) ---
    v_gap = 140 
    time_per_bin = 0.1 
    time_axis_base = np.arange(config.WAVEFORM_BINS) * time_per_bin

    for i, idx in enumerate(sorted_idx):
        h = valid_hits[idx]
        offset = (len(valid_hits) - i) * v_gap
        mip_val = np.max(h.fadc0) / 50.0 
        norm_wf = (h.fadc0 / (np.max(h.fadc0) + 1e-9)) * (v_gap * 0.7)
        
        color = plt.cm.turbo(rel_times[idx] / (np.max(rel_times) + 1e-9))
        ax_wave.plot(time_axis_base + rel_times[idx], norm_wf + offset, color=color, lw=1.2)
        
        label = f"SD{h.xxyy:04d}: {mip_val:.1f} MIP | {h.radius:.2f} km"
        ax_wave.text(time_axis_base[-1] + rel_times[idx] + 0.8, offset + 10, label, fontsize=9)

    for spine in ['top', 'right']:
        ax_wave.spines[spine].set_visible(False)
    
    ax_wave.set_yticks([]) 
    ax_wave.set_xlabel("Relative time from earliest detector [µs]")
    ax_wave.set_xlim(left=0) 
    
    plt.subplots_adjust(left=0.08, right=0.88, top=0.95, bottom=0.1, wspace=0.15)
    plt.show()