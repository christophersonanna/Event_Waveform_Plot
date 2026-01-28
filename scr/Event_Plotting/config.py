#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pathlib import Path

# Configuration Constants
PROCESSED_DATA_PATH = Path('/home/anna/Machine_Learning_Xmax/data/processed_tree_sample.parquet')
        #We're working with this data file for now since I know its structure
#OUTPUT_DATA_PATH = Path('/home/anna/Machine_Learning_Xmax/data/PCA_single_detector_25PC.parquet')
N_COMPONENTS_PCA = 128
WAVEFORM_LENGTH = 128