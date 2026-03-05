#!/usr/bin/env python3
# -*- coding: utf-8 -*-

GRID_TO_KM = 1.2
PROTON_ID = 14
IRON_ID = 5626

WAVEFORM_BINS = 128
FEATURE_VECTOR_SIZE = 256
PCA_COMPONENTS = 25

# Window sizes for filtering
RADIUS_WINDOW = 1.5  # km
ENERGY_WINDOW = 0.25 # log10 eV
THETA_WINDOW = 5.0   # degrees
XMAX_WINDOW = 20.0   # g/cm^2

# Standard Zenith Bins for Sweeping
THETA_BINS = [15.0, 37.5, 52.5] 
ENERGY_BINS = [18.25, 18.75, 19.25, 19.75]
RADIUS_BINS = [3.0, 6.0, 9.0, 12.0]
XMAX_BINS = [650, 750, 850]