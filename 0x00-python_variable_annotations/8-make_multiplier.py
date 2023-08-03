#!/usr/bin/env python3

from typing import Callable

def make_multiplier(multiplier: float) -> Callable[[float], float]:
    """Returns a function that multiplies float by mutiplier"""
    def multiplier_function(i: float) -> float:
        return i * multiplier
    return multiplier_function