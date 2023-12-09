import fileinput

def next_item(curr: list[int]) -> int:
    # print(curr)
    if all((x == 0 for x in curr)):
        return 0
    differences = [x - curr[i] for i, x in enumerate(curr[1:])]
    return curr[-1] + next_item(differences)

sequences = list((int(x) for x in line.split()) for line in fileinput.input())
# print(next_item(list(sequences[0])))

next_values = list(next_item(list(seq)) for seq in sequences)
print(next_values)
print(len(next_values))
print(sum(next_values))
