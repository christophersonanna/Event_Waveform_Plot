#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def detector_waveforms(data, event):
    Detector_waveforms = []
    for i in range(0,len(data['FADC0'][event])):
        Detector_waveforms.append(data['FADC0'][event][i])
    return Detector_waveforms

def detector_time(data, event):
    Detector_time = []
    for i in range(0,len(data['ClockCount'][event])):
        Detector_time.append(data['ClockCount'][event][i])
    return Detector_time