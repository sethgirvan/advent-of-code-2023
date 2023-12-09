from typing import Tuple
import fileinput
import re

def subset_mins(subset: str) -> Tuple[int, int, int]:
    """
    Returns tuple of minimum number of (red, green blue) cubes
    """

    red_match = re.search(r"(\d+) red", subset)
    if red_match and red_match.group(1):
        red = int(red_match.group(1))
    else:
        red = 0

    green_match = re.search(r"(\d+) green", subset)
    if green_match and green_match.group(1):
        green = int(green_match.group(1))
    else:
        green = 0

    blue_match = re.search(r"(\d+) blue", subset)
    if blue_match and blue_match.group(1):
        blue = int(blue_match.group(1))
    else:
        blue = 0

    return (red, green, blue)

def game_power(game: str) -> int:
    subsets = re.match(r"^Game \d+: (.*)$", game)
    subset_list = subsets.group(1).split(";")
    rgb_min_lists = zip(*(subset_mins(subset) for subset in subset_list))
    maxes = [max(x) for x in rgb_min_lists]
    power = maxes[0] * maxes[1] * maxes[2]
    return power

sum = sum(game_power(line) for line in fileinput.input())

print(f"sum: {sum}")
