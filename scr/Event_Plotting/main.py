import argparse
import os
from glob import glob
from datetime import datetime
from load import load_and_transform
from data_manager import save_to_npz, load_from_npz
from event_display import plot_event_display

def main():
    parser = argparse.ArgumentParser(description="TA Universal Loader & Plotter")
    parser.add_argument("-i", "--input", nargs='+', help="Input directories or files")
    parser.add_argument("--cache", help="Path to save/load .npz file")
    parser.add_argument("--force", action="store_true", help="Overwrite existing cache")
    parser.add_argument("--isgood", type=int, default=3, help="Minimum isgood value")
    parser.add_argument("--step", type=int, default=1, help="Load every nth file")
    
    # Updated index to take 1 or 2 values (e.g., -n 5 or -n 5 12)
    parser.add_argument("-n", "--index", type=int, nargs='+', default=[0], help="Event index or range (start end)")
    
    # Updated search arguments to take an optional count
    parser.add_argument('--highest-energy', type=int, nargs='?', const=1, help='Plot top N energy events')
    parser.add_argument('--most-hits', type=int, nargs='?', const=1, help='Plot top N events with most hits')
    parser.add_argument('--find-time', type=str, help='Find event closest to time (YYYY-MM-DD HH:MM:SS)')

    args = parser.parse_args()
    events = []

    # Loading Logic
    if args.input:
        if args.cache and os.path.exists(args.cache) and not args.force:
            events = load_from_npz(args.cache)
        else:
            all_files = []
            for path in args.input:
                if os.path.isdir(path):
                    found = sorted(glob(os.path.join(path, "*.parquet")))[::args.step]
                    all_files.extend(found)
                else:
                    all_files.append(path)
            for f in all_files:
                events.extend(load_and_transform(f))
            if args.cache:
                save_to_npz(events, args.cache)
    elif args.cache:
        events = load_from_npz(args.cache)

    if not events:
        print("No events found.")
        return

    target_events = []

    # Selection Logic for Multiple Plots
    if args.highest_energy is not None:
        # Sort by energy descending and take N
        target_events = sorted(events, key=lambda e: e.energy, reverse=True)[:args.highest_energy]
        print(f"Plotting top {len(target_events)} highest energy events.")

    elif args.most_hits is not None:
        # Sort by hit count passing isgood filter
        target_events = sorted(events, key=lambda e: len([h for h in e.hits if h.isgood >= args.isgood]), reverse=True)[:args.most_hits]
        print(f"Plotting top {len(target_events)} events with most hits.")

    elif args.find_time:
        search_ts = datetime.strptime(args.find_time, "%Y-%m-%d %H:%M:%S").timestamp()
        closest = min(events, key=lambda e: abs(getattr(e, 'time', 0) - search_ts))
        target_events = [closest]

    else:
        # Handle index or range
        if len(args.index) == 1:
            idx = args.index[0]
            target_events = [events[idx]] if idx < len(events) else []
        else:
            start, end = args.index[0], args.index[1]
            target_events = events[start:end+1]
            print(f"Plotting range {start} to {end}.")

    # Loop through and plot
    for ev in target_events:
        print(f"Displaying Event ID: {ev.event_id}")
        plot_event_display(ev, min_isgood=args.isgood)

if __name__ == "__main__":
    main()