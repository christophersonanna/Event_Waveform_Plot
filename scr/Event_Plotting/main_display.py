#!/usr/bin/env python3
import argparse
import sys
from load import load_and_transform
# Assuming the plotting function above is in event_display.py
from event_display import plot_event_display

def main():
    parser = argparse.ArgumentParser(description="TA Event Display CLI")
    parser.add_argument("-i", "--input", required=True, help="Path to .parquet file")
    parser.add_argument("-n", "--index", type=int, default=0, help="Event index to display")
    
    # Placeholder for future cuts
    parser.add_argument("--min-energy", type=float, help="Minimum log10(Energy)")
    parser.add_argument("--max-hits", type=int, help="Filter by number of hits")

    args = parser.parse_args()

    # Load data using your existing base
    events = load_and_transform(args.input)
    
    if not events:
        print("No events found.")
        return

    # Apply cuts (Logic can be expanded here)
    filtered_events = events
    if args.min_energy:
        filtered_events = [e for e in filtered_events if e.energy >= args.min_energy]
    
    if args.index >= len(filtered_events):
        print(f"Index {args.index} out of range (Found {len(filtered_events)} events).")
        return

    print(f"Displaying event {filtered_events[args.index].event_id}...")
    plot_event_display(filtered_events[args.index])

if __name__ == "__main__":
    main()