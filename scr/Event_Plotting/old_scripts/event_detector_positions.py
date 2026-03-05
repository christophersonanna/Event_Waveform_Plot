#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def event_detector_positions(data, event):
    Detector_positions = []
    for i in range(0,len(data['DetectorXXYY'][event])):
        Detector_positions.append(data['DetectorXXYY'][event][i])
    return Detector_positions