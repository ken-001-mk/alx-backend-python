#!/usr/bin/env python3

from typing import Iterable, List, Sequence, Tuple

def element_length(lst: Iterable[Sequence]) -> List[Tuple[Sequence, int]]:
    """Returns a list of tuples, where each tuple contains a string element
    and its corresponding length as an integer."""
    return [(i, len(i)) for i in lst]