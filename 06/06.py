# For part two just delete the spaces in the input

import math
import fileinput

with fileinput.input() as f:
    lines = iter(f)

    times_line = next(lines)
    dist_line = next(lines)

    times = [int(s) for s in times_line.split(":")[1].split()]
    dists = [int(s) for s in dist_line.split(":")[1].split()]

    product = 1

    # r = race time
    # t = button hold time
    # d = distance
    #
    # t(r - t) = d
    # -t^2 + rt - d = 0
    # t^2 - rt + d = 0
    #
    # quadratic formula:
    # t = [r +- sqrt(r^2 - 4d)]/2
    for time, dist in zip(times, dists):
        min_button_time = (time - math.sqrt(time**2 - 4*dist))/2
        max_button_time = (time + math.sqrt(time**2 - 4*dist))/2

        min_button_time_ceil = math.ceil(min_button_time)
        max_button_time_floor = math.floor(max_button_time)
        if min_button_time_ceil == min_button_time:
            min_button_time_ceil += 1
        if max_button_time_floor == max_button_time:
            max_button_time_floor -= 1

        time_range = max_button_time_floor - min_button_time_ceil + 1
        if time_range > 0:
            product *= time_range

print(product)
