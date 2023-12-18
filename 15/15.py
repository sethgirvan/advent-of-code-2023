import fileinput

line = next(fileinput.input()).rstrip()

def hash_str(input: str) -> int:
    hash = 0
    for c in input:
        hash = 17 * (hash + ord(c)) % 256
    return hash

p1 = sum(hash_str(step) for step in line.split(","))
print(f"p1 answer: {p1}")
