import fileinput
import re

RED_MAX = 12
GREEN_MAX = 13
BLUE_MAX = 14

def subset_is_possible(subset: str) -> bool:
    red = re.search(r"(\d+) red", subset)
    if red and red.group(1) and int(red.group(1)) > RED_MAX:
        return False

    green = re.search(r"(\d+) green", subset)
    if green and green.group(1) and int(green.group(1)) > GREEN_MAX:
        return False

    blue = re.search(r"(\d+) blue", subset)
    if blue and blue.group(1) and int(blue.group(1)) > BLUE_MAX:
        return False

    return True

def game_is_possible(game: str) -> bool:
    subsets = re.match(r"^Game \d+: (.*)$", game)
    subset_list = subsets.group(1).split(";")
    return all(subset_is_possible(subset) for subset in subset_list)

sum = 0
for line in fileinput.input():
    if game_is_possible(line):
        game = int(re.match(r"^Game (\d+):", line).group(1))
        sum += game

print(f"sum: {sum}")
