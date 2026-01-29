#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from parameter_cuts_and_organization import data_df
from event_waveforms import detector_waveforms, detector_time

def combining_waveform_and_time(waveforms, times):
    #Making t=0 at first triggered
    min_time = min(times)
    new_times = []
    for i in range(0,len(times)):
        new_times.append(times[i] - min_time)
    
    #timed_waveforms = []
    #for i in range(0,len(waveforms)):
    return new_times
    #return timed_waveform
    
Event = 66
waveforms = detector_waveforms(data_df, Event)
times = detector_time(data_df, Event)

test = combining_waveform_and_time(waveforms, times)
print(test)
