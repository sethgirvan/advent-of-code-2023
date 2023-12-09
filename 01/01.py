import fileinput
import re

sum: int = 0
for line in fileinput.input():
    digits = re.findall(r"\d", line)
    calibration_val = int(digits[0] + digits[-1])
    print(f"calibration value: {calibration_val}")
    sum += calibration_val

print(f"sum: {sum}")
