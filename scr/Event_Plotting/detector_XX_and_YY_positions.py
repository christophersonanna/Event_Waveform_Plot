#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def Detector_XX_and_YY_positions(positions):
    X_position = []
    Y_position = []
    for i in range(0, len(positions)):
        position = str(positions[i])
        if len(position) == 3:
            X = position[0]
            Y = position[1:2]
        else:
            X = position[0:1]
            Y = position[2:]
        X_position.append(int(X))
        Y_position.append(int(Y))
    return X_position, Y_position