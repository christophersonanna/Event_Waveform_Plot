#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#importing
import matplotlib.pyplot as plt
import numpy as np

from parameter_cuts_and_organization import data_df
from whole_array_positions import SD_main_array
from event_detector_positions import event_detector_positions
from event_waveforms import detector_waveforms, detector_time
from detector_XX_and_YY_positions import Detector_XX_and_YY_positions

#Collecting Event data
Event = int(input("What is the event number?: "))

#basic information
positions = event_detector_positions(data_df, Event)
waveforms = detector_waveforms(data_df, Event)
time = detector_time(data_df, Event)
X_positions, Y_positions = Detector_XX_and_YY_positions(positions)

