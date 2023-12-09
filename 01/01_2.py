import fileinput
import re

word_to_digit_map = {
        "zero": "0",
        "one": "1",
        "two": "2",
        "three": "3",
        "four": "4",
        "five": "5",
        "six": "6",
        "seven": "7",
        "eight": "8",
        "nine": "9",
}
pattern = "|".join(sorted(re.escape(k) for k in word_to_digit_map))

rev_word_to_digit_map = {word[::-1]: digit for word, digit in word_to_digit_map.items()}
pattern_rev = "|".join(sorted(re.escape(k) for k in rev_word_to_digit_map))

sum: int = 0
for line in fileinput.input():
    reversed = line[::-1]

    all_digits = re.sub(pattern, lambda match: word_to_digit_map[match.group(0)], line)
    all_digits_rev = re.sub(pattern_rev, lambda match: rev_word_to_digit_map[match.group(0)], reversed)


    # for word, digit in word_to_digit_map.items():
    #     line = line.replace(word, digit)
    first = re.search(r"\d", all_digits).group(0)

    # for word, digit in rev_word_to_digit_map.items():
    #     reversed = reversed.replace(word, digit)
    last = re.search(r"\d", all_digits_rev).group(0)
    calibration_val = int(first + last)

    # digits = re.findall(r"\d", all_digits)
    # calibration_val = int(digits[0] + digits[-1])

    print(f"calibration value: {calibration_val}")
    sum += calibration_val

print(f"sum: {sum}")
