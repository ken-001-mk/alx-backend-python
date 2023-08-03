#!/usr/bin/env python3

from typing import Any, Mapping, TypeVar, Union

K = TypeVar('K')
V = Union[Any, K]
F = Union[K, None]

def safely_get_value(dct: Mapping, key:Any, default: F = None) -> V:
    """Return value of key if it exists, otherwise return default"""
    if key in dct:
        return dct[key]
    else:
        return default
