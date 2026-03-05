#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import config
from data_structure import Event

# aggregation.py
import numpy as np

def extract_event_features(events):
    features = []
    metadata = []
    
    for e in events:
        # 1. Gets all FADC waveforms for this event's hits
        # Shape: (num_hits, 128)
        waves = np.array([h.fadc0 for h in e.hits])
        
        if len(waves) == 0:
            continue
            
        # 2. Calculate the "Event Profile"
        # Takes the mean and std across the hits to see the 'average' shower shape
        mean_wf = np.mean(waves, axis=0)
        std_wf = np.std(waves, axis=0)
        
        # 3. Combines them into one feature vector (256 bins)
        f = np.concatenate([mean_wf, std_wf])
        
        features.append(f)
        
        # 4. Stores the metadata for coloring the plots later
        metadata.append({
            'xmax': e.xmax,
            'energy': e.energy,
            'particle': e.particle,
            'radius': np.mean([h.radius for h in e.hits]),
            'theta': e.theta,
            'event_id': e.event_id
        })
    
    return np.array(features), metadata

def extract_batch(file_list, args):
    """
    Loops through files, extracts waveforms and metadata, 
    and aggregates them into numpy arrays.
    """
    all_features = []
    all_metadata = []
    
    print(f"Starting extraction for {len(file_list)} files...")
    
    for i, f_path in enumerate(file_list):
        try:
            # 1. Load the raw data from parquet
            df = load_and_transform(f_path)
            
            # 2. Extract physics features (waveforms + labels)
            # This assumes extract_event_features returns (features, metadata_dict)
            feats, meta = extract_event_features(df)
            
            if feats is not None:
                all_features.append(feats)
                all_metadata.append(meta)
                
            if (i + 1) % 10 == 0:
                print(f"Processed {i + 1}/{len(file_list)} files")
                
        except Exception as e:
            print(f"Error processing {f_path}: {e}")
            continue

    if not all_features:
        print("No data extracted. Check your input files and extract_event_features logic.")
        return None, None

    # Convert lists to final analysis formats
    final_features = np.vstack(all_features)
    return final_features, all_metadata