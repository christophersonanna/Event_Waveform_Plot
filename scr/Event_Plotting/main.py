import argparse
import os
from glob import glob
from datetime import datetime
from load import load_and_transform
from data_manager import save_to_npz, load_from_npz
from event_display import plot_event_display

def main():
    parser = argparse.ArgumentParser(description="TA Universal Loader & Plotter")
    
    # Input/Cache Args
    parser.add_argument("-i", "--input", nargs='+', help="Input directories or files")
    parser.add_argument("--cache", help="Path to save/load .npz file")
    parser.add_argument("--force", action="store_true", help="Overwrite existing cache")
    parser.add_argument("--isgood", type=int, default=3, help="Minimum isgood value (0-4)")
    parser.add_argument("--step", type=int, default=1, help="Load every nth file")
    
    # Plotting/Saving Args
    parser.add_argument("-n", "--index", type=int, nargs='+', default=[0], help="Index or range [start end]")
    parser.add_argument("--save", type=str, help="Folder to save plots instead of showing them")
    
    # Search Args
    parser.add_argument('--highest-energy', type=int, nargs='?', const=1, help='Plot top N energy events')
    parser.add_argument('--most-hits', type=int, nargs='?', const=1, help='Plot top N events with most hits')
    parser.add_argument('--find-time', type=str, help='Find event closest to time (YYYY-MM-DD HH:MM:SS)')

    args = parser.parse_args()
    events = []

    # 1. Loading
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
        print("No events loaded.")
        return

    # Create save directory if requested
    if args.save and not os.path.exists(args.save):
        os.makedirs(args.save)

    # 2. Selection
    target_list = []
    if args.highest_energy is not None:
        target_list = sorted(events, key=lambda e: e.energy, reverse=True)[:args.highest_energy]
    elif args.most_hits is not None:
        target_list = sorted(events, key=lambda e: len([h for h in e.hits if h.isgood >= args.isgood]), reverse=True)[:args.most_hits]
    elif args.find_time:
        try:
            search_ts = datetime.strptime(args.find_time, "%Y-%m-%d %H:%M:%S").timestamp()
            closest = min(events, key=lambda e: abs(getattr(e, 'time', 0) - search_ts))
            target_list = [closest]
        except ValueError:
            print("Time format: YYYY-MM-DD HH:MM:SS")
            return
    else:
        if len(args.index) == 1:
            idx = args.index[0]
            if idx < len(events): target_list = [events[idx]]
        else:
            start, end = args.index[0], args.index[1]
            target_list = events[start : end + 1]

    # 3. Plotting Loop
    for ev in target_list:
        save_path = None
        if args.save:
            save_path = os.path.join(args.save, f"event_{ev.event_id}.png")
            print(f"Saving Event {ev.event_id} to {save_path}...")
        else:
            print(f"Displaying Event {ev.event_id}...")
            
        plot_event_display(ev, min_isgood=args.isgood, save_to=save_path)

if __name__ == "__main__":
    main()