#!/usr/bin/env python3

from typing import List, Union

def sum_mixed_list(mxd_lst: List[Union[int,float]]) -> float:
    """Takes list of floats and integers and return ths sum as a float"""
    return sum(mxd_lst)