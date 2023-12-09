import fileinput

def prev_item(curr: list[int]) -> int:
    # print(curr)
    if all((x == 0 for x in curr)):
        return 0
    differences = [x - curr[i] for i, x in enumerate(curr[1:])]
    return curr[0] - prev_item(differences)

sequences = list((int(x) for x in line.split()) for line in fileinput.input())
# print(prev_item(list(sequences[0])))

prev_values = list(prev_item(list(seq)) for seq in sequences)
print(prev_values)
print(len(prev_values))
print(sum(prev_values))
