#!/usr/bin/env python3

import asyncio
from typing import List

wait_random = __import__("0-basic_async_syntax").wait_random 

async def wait_n(n: int, max_delay: int) -> List[float]:
  """return list of all delays"""
  wait = await asyncio.gather(
      *list(map(lambda _: wait_random(max_delay), range(n)))
  )
  return sorted(wait)