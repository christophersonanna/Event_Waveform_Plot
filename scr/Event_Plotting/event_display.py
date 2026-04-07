import matplotlib.pyplot as plt
import numpy as np
import config
from data_structure import Event

def plot_event_display(event: Event, min_isgood=3, save_to=None):
    # --- 1. Deduplicate & Filter ---
    sd_map = {}
    for h in event.hits:
        if h.isgood >= min_isgood:
            if h.xxyy not in sd_map or np.max(h.fadc0) > np.max(sd_map[h.xxyy].fadc0):
                sd_map[h.xxyy] = h
    valid_hits = list(sd_map.values())
    if not valid_hits: return

    # --- 2. Time Alignment ---
    sorted_by_sig = sorted(valid_hits, key=lambda h: np.max(h.fadc0), reverse=True)
    t0 = min([h.reltime for h in sorted_by_sig[:3]])
    
    processed_hits = []
    for h in valid_hits:
        dt = h.reltime - t0
        if -5.0 < dt < 20.0:
            h.norm_time = dt
            processed_hits.append(h)
    
    if not processed_hits: return
    processed_hits.sort(key=lambda h: h.norm_time)
    
    # --- 3. UI Setup ---
    fig = plt.figure(figsize=(22, 13))
    gs = fig.add_gridspec(2, 2, height_ratios=[1.2, 6], width_ratios=[1, 1.4], hspace=0.1)
    ax_info = fig.add_subplot(gs[0, 0]); ax_array = fig.add_subplot(gs[1, 0]); ax_wave = fig.add_subplot(gs[:, 1])

    # --- Info Section ---
    ax_info.set_axis_off()
    theta_rad = event.theta / 1000.0 if np.degrees(event.theta) > 180 else event.theta
    info_text = (f"Event ID: {event.event_id}\n"
                 f"Energy: $10^{{{event.energy:.2f}}}$ eV\n"
                 f"Zenith: {np.degrees(theta_rad):.1f}°")
    ax_info.text(0.0, 0.5, info_text, fontsize=15, weight='bold', va='center', linespacing=1.6)

    # --- Array Map ---
    gx, gy = np.meshgrid(np.arange(1, 21), np.arange(1, 25))
    ax_array.scatter(gx, gy, s=6, c='royalblue', alpha=0.2, marker='o') 
    
    ew = np.array([h.xxyy // 100 for h in processed_hits])
    ns = np.array([h.xxyy % 100 for h in processed_hits])
    sigs = np.array([np.sum(h.fadc0) for h in processed_hits])
    times = np.array([h.norm_time for h in processed_hits])
    ax_array.scatter(ew, ns, s=(np.log10(sigs + 1) * 45), c=times, cmap='turbo', edgecolors='none', zorder=3)

    # --- DYNAMIC BALANCED GEOMETRY ---
    idx_first = np.argmin(times); idx_last = np.argmax(times)
    x_s, y_s = ew[idx_first], ns[idx_first]; x_e, y_e = ew[idx_last], ns[idx_last]
    dx = x_e - x_s; dy = y_e - y_s; dist = np.sqrt(dx**2 + dy**2) + 1e-9
    
    # Arrow
    arrow_scale = 1.15; head_size = 0.45 
    ax_array.arrow(x_s, y_s, dx * arrow_scale, dy * arrow_scale, 
                   head_width=head_size, head_length=head_size * 1.2, 
                   color='black', lw=1.5, zorder=5)
    
    # Shower Front (Corrected scaling)
    px, py = -dy/dist, dx/dist
    f_half_width = max(1.2, dist * 0.4) 
    ax_array.plot([event.xcore - px * f_half_width, event.xcore + px * f_half_width], 
                  [event.ycore - py * f_half_width, event.ycore + py * f_half_width], 
                  color='black', lw=2.0, zorder=4, alpha=0.6)

    # Formatting
    for spine in ['top', 'right']: ax_array.spines[spine].set_visible(False)
    ax_array.set_aspect('equal'); ax_array.set_xlabel("East-West [XX]"); ax_array.set_ylabel("North-South [YY]")

    # --- Waveforms ---
    v_gap = 140; time_per_bin = 0.1 
    time_axis_base = np.arange(config.WAVEFORM_BINS) * time_per_bin

    for i, h in enumerate(processed_hits):
        offset = (len(processed_hits) - i) * v_gap
        norm_wf = (h.fadc0 / (np.max(h.fadc0) + 1e-9)) * (v_gap * 0.7)
        color = plt.cm.turbo(h.norm_time / (max(times) + 1e-9))
        ax_wave.plot(time_axis_base + h.norm_time, norm_wf + offset, color=color, lw=1.2)
        label = f"SD{h.xxyy:04d}: {np.max(h.fadc0)/50.0:.1f} MIP | {h.radius:.2f} km"
        ax_wave.text(time_axis_base[-1] + h.norm_time + 0.8, offset + 10, label, fontsize=9)

    for spine in ['top', 'right']: ax_wave.spines[spine].set_visible(False)
    ax_wave.set_yticks([]); ax_wave.set_xlabel("Relative time from core [µs]"); ax_wave.set_xlim(left=0) 
    
    plt.subplots_adjust(left=0.08, right=0.88, top=0.95, bottom=0.1, wspace=0.15)
    
    # --- OUTPUT LOGIC ---
    if save_to:
        plt.savefig(save_to, dpi=150)
        plt.close(fig) # Critical: close the figure to free up RAM
    else:
        plt.show()