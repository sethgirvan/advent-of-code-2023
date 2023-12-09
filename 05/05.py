from functools import total_ordering
from typing import List, Dict

import bisect
import fileinput
import re

@total_ordering
class RangeMap:
    srcStart: int
    dstStart: int
    length: int

    def __init__(self, srcStart: int, dstStart: int, length: int):
        self.srcStart = srcStart
        self.dstStart = dstStart
        self.length = length

    def __eq__(self, other) -> bool:
        if hasattr(other, "srcStart"):
            return self.srcStart == other.srcStart
        else:
            return self.srcStart == other

    def __lt__(self, other) -> bool:
        if hasattr(other, "srcStart"):
            return self.srcStart < other.srcStart
        else:
            return self.srcStart < other

    def containsSrc(self, src: int) -> bool:
        return self.srcStart <= src and src < self.srcStart + self.length

    def mapSrcToDst(self, src: int) -> int:
        if not self.containsSrc(src):
            raise Exception(f"src argument {src} not in RangeMap {srcStart} {length}")
        return self.dstStart + (src - self.srcStart)

class AToBMap:
    src: str = ""
    dst: str = ""
    range_maps: List[RangeMap] = []

    def __init__(self, src: str, dst: str):
        self.src = src
        self.dst = dst
        self.range_maps = []

    def insert(self, r: RangeMap):
        idx = bisect.bisect_left(self.range_maps, r)
        self.range_maps.insert(idx, r)

    def mapSrc(self, src: int) -> int:
        idx = bisect.bisect_right(self.range_maps, src) - 1
        if idx < 0:
            print(f"src {src} less than min srcStart")
            return src
        r = self.range_maps[idx]
        if r.containsSrc(src):
            print(f"Contains src {src}")
            print(f"Select range {r.srcStart} {r.dstStart} {r.length}")
            calculated = src - r.srcStart + r.dstStart
            print(f"calculated: {calculated}")
            return r.mapSrcToDst(src)
        else:
            print(f"Does not contain src {src}")
            return src

maps: Dict[str, AToBMap] = {}
seeds: List[int] = []

def seedToLoc(seed: int) -> int:
    val = seed
    src_dst_map = maps["seed"]
    print(f"\n\nseed: {seed}")
    while True:
         print(f"Mapping {src_dst_map.src} to {src_dst_map.dst}")
         val = src_dst_map.mapSrc(val)
         print(f"val: {val}")
         if src_dst_map.dst == "location":
             break
         src_dst_map = maps[src_dst_map.dst]
    return val

with fileinput.input() as f:
    lines = iter(f)

    seed_line = next(lines)
    seeds = [int(seed) for seed in re.findall(r"\d+", seed_line)]

    # Build 'foo-to-bar' maps
    for line in lines:
        if not line.strip():
            continue

        match = re.match(r"(\w+)-to-(\w+)", line)
        if match is None:
            raise Exception("Failed to match 'foo-to-bar' line")
        src = str(match.group(1))
        dst = str(match.group(2))
        src_dst_map = AToBMap(src, dst)

        # Add ranges to current map
        for range_line in lines:
            if not range_line.strip():
                break

            range_match = re.match(r"(\d+) +(\d+) +(\d+)", range_line)
            if range_match is None:
                print(f"Failed to match range map line {range_line}")
                raise Exception("Failed to match range map line")
            dstStart = int(str(range_match.group(1)))
            srcStart = int(str(range_match.group(2)))
            length = int(str(range_match.group(3)))
            src_dst_map.insert(RangeMap(srcStart, dstStart, length))

        maps[src_dst_map.src] = src_dst_map

for k, src_dst_map in maps.items():
    print(f"key {k} Source {src_dst_map.src} Dest {src_dst_map.dst}")
    for r in src_dst_map.range_maps:
        print(f"{r.srcStart} {r.dstStart} {r.length}")
    print("\n\n")


locations = (seedToLoc(seed) for seed in seeds)
print(min(locations))
