import math
import fileinput
import re

def cycle_len(node: str, map_all_ix_dict: dict[str, str]) -> int:
    step = 0
    while not check_node_finished(node):
        node = map_all_ix_dict[node]
        step += 1
    return step

def map_node(node: str, ix: str, map_dict: dict[str, tuple[str, str]]) -> str:
    return map_dict[node][0 if ix == "L" else 1]

def map_node_all_ix(node: str, ixs: str, map_dict: dict[str, tuple[str, str]]) -> str:
    for ix in ixs:
        node = map_node(node, ix, map_dict)
    return node

def check_node_finished(node: str) -> bool:
    return node[2] == "Z"

def check_nodes_finished(nodes: list[str]) -> bool:
    return all(check_node_finished(n) for n in nodes)

def map_line_to_tuple(line: str) -> tuple[str, str, str]:
    nodes = re.findall(r"\w+", line)
    return (nodes[0], nodes[1], nodes[2])

with fileinput.input() as f:
    lines = iter(f)

    rl_ixs = next(lines).strip()

    next(lines) # Remove empty line
    tups = list(map_line_to_tuple(l) for l in lines)
    # All nodes starting with A
    nodes = [t[0] for t in tups if t[0][2] == "A"]
    map_dict = {t[0]: (t[1], t[2]) for t in tups}
    map_all_ix_dict = {k: map_node_all_ix(k, rl_ixs, map_dict) for k in map_dict}

    cycle_lens = [cycle_len(n, map_all_ix_dict) for n in nodes]
    nodes_lcm = math.lcm(*cycle_lens)
    print(281 * nodes_lcm)


#     step = 0
#     while not check_nodes_finished(nodes):
#         for i in range(0, 1000000):
#             if check_nodes_finished(nodes):
#                 break
#             for i, _ in enumerate(nodes):
#                 nodes[i] = map_all_ix_dict[nodes[i]]
#             step += 281
#         print(step)
#         print(nodes)
#
# print(step)
