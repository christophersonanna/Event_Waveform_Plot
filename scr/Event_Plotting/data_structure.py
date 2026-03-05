# -*- coding: utf-8 -*-

from dataclasses import dataclass
import numpy as np
from typing import List

@dataclass
class Hit:
    fadc0: np.ndarray
    fadc1: np.ndarray
    xxyy: int
    radius: float
    sstart: float
    isgood: int
    reltime: float
    timeerr: float

@dataclass
class Event:
    event_id: int
    particle: int
    energy: float
    hits: List[Hit]
    xcore: float
    ycore: float
    xmax: float
    phi: float
    theta: float