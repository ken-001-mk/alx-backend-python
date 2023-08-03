#!/usr/bin/env python3

from typing import Sequence, Any, Union

def safe_first_element(lst: Sequence[Any]) -> Union[Any, None]:
    """Returns first element of list or None if list is empty"""
    if lst:
        return lst[0]
    else:
        return None