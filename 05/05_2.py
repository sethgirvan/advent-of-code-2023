from functools import total_ordering
from typing import List, Dict, Tuple, Generator

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
        # if not self.containsSrc(src):
        #     raise Exception(f"src argument {src} not in RangeMap {srcStart} {length}")
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
            # print(f"src {src} less than min srcStart")
            return src
        r = self.range_maps[idx]
        if r.containsSrc(src):
            # print(f"Contains src {src}")
            # print(f"Select range {r.srcStart} {r.dstStart} {r.length}")
            calculated = src - r.srcStart + r.dstStart
            # print(f"calculated: {calculated}")
            return r.mapSrcToDst(src)
        else:
            # print(f"Does not contain src {src}")
            return src
    def mapInterval(self, src: tuple[int, int]) -> list[tuple[int, int]]:
        left = src[0]
        right = src[1]
        out: list[tuple[int, int]] = []
        while left < right:
            idx = bisect.bisect_right(self.range_maps, left) - 1
            if idx < 0:
                next_range = self.range_maps[0]
                seg_end = min(right, next_range.srcStart)
                out.append((left, seg_end))
                left = seg_end
                print("break1")
                continue

            r = self.range_maps[idx]
            if r.containsSrc(left):
                seg_end = min(right, r.srcStart + r.length)
                out.append((r.mapSrcToDst(left), r.mapSrcToDst(seg_end)))
                left = seg_end
                print("break2")
                continue
            elif idx == len(self.range_maps) - 1:
                out.append((left, right))
                left = right
                print("break3")
                continue
            else:
                next_range = self.range_maps[idx + 1]
                seg_end = min(right, next_range.srcStart)
                out.append((left, seg_end))
                left = seg_end
                print("break1")
                continue
        return out

    def mapIntervals(self, srcs: list[tuple[int, int]]) -> list[tuple[int, int]]:
        nested = [self.mapInterval(src) for src in srcs]
        return [item for sublist in nested for item in sublist]


maps: Dict[str, AToBMap] = {}
seeds: Generator[int, None, None]

# def merge_maps(src_map: AToBMap, dst_map: AToBMap) -> AToBMap:
#     src_ranges = sorted(src_map.range_maps, key=lambda x: x.dstStart)
#     dst_ranges = dst_map.range_maps
#     merged_map = AToBMap(src_map.src, dst_map.dst)
# 
#     src_idx = 0
#     dst_idx = 0
#     src_start = src_ranges[0].dstStart
#     dst_start = dst_ranges[0].srcStart
#     while src_idx < len(src_ranges) and dst_idx < len(dst_ranges):
#         if src_start < dst_start:
#             if src_idx >= len(src_ranges):
#                 src_start = dst_start
#                 break
#             elif src_ranges[src_idx].dstStart + src_ranges[src_idx].length <= dst_start:
#                 src = src_ranges[src_idx]
#                 offset = src_start - src.dstStart
#                 length = src.dstStart + src.length - src_start
#                 merged_map.insert(RangeMap(
#                     src.srcStart + offset,
#                     src_start,
#                     length,
#                     ))
#                 src_start += length
#                 src_idx += 1
#                 break
#             else:
#                 src = src_ranges[src_idx]
#                 offset = src_start - src.dstStart
#                 length = dst_start - src_start
#                 merged_map.insert(RangeMap(
#                     src.srcStart + offset,
#                     src_start,
#                     length,
#                     ))
#                 src_start = dst_start
#                 break;
#         elif src_start == dst_start:
#             if src_idx >= len(src_ranges):
#                 while dst_idx < len(dst_ranges):
#                     dst = dst_ranges[dst_idx]
#                     merged_map.insert(RangeMap(
#                         dst
#                         
#             src = src_ranges[src_idx]
#             src_len = src.dstStart + src.length - src_start
#             dst_len = 
#         elif src_start > dst_start:


def seed_to_loc(seed: int) -> int:
    val = seed
    src_dst_map = maps["seed"]
    # print(f"\n\nseed: {seed}")
    while True:
         # print(f"Mapping {src_dst_map.src} to {src_dst_map.dst}")
         val = src_dst_map.mapSrc(val)
         # print(f"val: {val}")
         if src_dst_map.dst == "location":
             break
         src_dst_map = maps[src_dst_map.dst]
    return val

def seed_intervals_to_loc_intervals(seed_intervals: list[tuple[int, int]]) -> list[tuple[int, int]]:
    intervals = seed_intervals
    src_dst_map = maps["seed"]
    # print(f"\n\nseed: {seed}")
    while True:
         print(f"Mapping {src_dst_map.src} to {src_dst_map.dst}")
         intervals = src_dst_map.mapIntervals(intervals)
         print(f"intervals: {intervals}")
         print(f"interval count: {len(intervals)}")
         if src_dst_map.dst == "location":
             break
         src_dst_map = maps[src_dst_map.dst]
    return intervals

def seed_range_to_tuple(seed_range: str) -> Tuple[int, int]:
    match = re.match(r"(\d+) +(\d+)", seed_range)
    if match is None:
        print(f"Failed to match seed range {seed_range}")
        raise Exception("Failed to seed_range")

    return (int(match.group(1)), int(match.group(2)))

def seed_range_to_interval(seed_range: tuple[int, int]) -> Tuple[int, int]:
    return (seed_range[0], seed_range[0] + seed_range[1])

def progress(l, func):
    ll = list(l)
    length = len(ll)
    for i, x in enumerate(ll):
        print("item {i}/{length}")
        yield func(x)

with fileinput.input() as f:
    lines = iter(f)

    seed_line = next(lines)
    seed_ranges = (seed_range for seed_range in re.findall(r"\d+ \d+", seed_line))
    seed_range_tuples = list(seed_range_to_tuple(s) for s in seed_ranges)
    seed_intervals = list(seed_range_to_interval(srt) for srt in seed_range_tuples)
    print(f"seed_range_tuples: {seed_range_tuples}")

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

location_intervals = seed_intervals_to_loc_intervals(seed_intervals)
print(f"location_intervals: {location_intervals}")
print(min(location_intervals, key=lambda x: x[0]))
