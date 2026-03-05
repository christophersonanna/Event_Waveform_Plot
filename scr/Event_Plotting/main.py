#!/usr/bin/env python3
import argparse
import os
from glob import glob
from load import load_and_transform
from data_manager import save_to_npz, load_from_npz
from event_display import plot_event_display 

def main():
    parser = argparse.ArgumentParser(description="TA Universal Loader & Plotter")
    parser.add_argument("-i", "--input", nargs='+', help="Input directories")
    parser.add_argument("--cache", help="Path to .npz file")
    parser.add_argument("--step", type=int, default=1, help="Load every nth file")
    parser.add_argument("-n", "--index", type=int, default=0, help="Event index to plot")

    args = parser.parse_args()
    events = []

    if args.input:
        all_files = []
        for path in args.input:
            if os.path.isdir(path):
                # Apply the step logic here
                found = sorted(glob(os.path.join(path, "*.parquet")))[::args.step]
                print(f"Path {path}: Found {len(found)} files (step={args.step})")
                all_files.extend(found)
            else:
                all_files.append(path)
        
        for f in all_files:
            events.extend(load_and_transform(f))
        
        if args.cache:
            save_to_npz(events, args.cache)

    elif args.cache:
        events = load_from_npz(args.cache)

    if events:
        print(f"Total Events: {len(events)}")
        plot_event_display(events[args.index])

if __name__ == "__main__":
    main()