from collections.abc import Callable

import fileinput
import functools
import operator
import re

class PartRange:
    categories: dict[str, tuple[int, int]]

    def __init__(self):
        self.categories = {}

    def from_new_range(self, category: str, range: tuple[int, int]):
        ret = type(self)()
        ret.categories = self.categories.copy()
        ret.categories[category] = range
        return ret

    @classmethod
    def from_ranges(
            cls,
            x: tuple[int, int],
            m: tuple[int, int],
            a: tuple[int, int],
            s: tuple[int, int],
    ) :
        ret = cls()
        ret.categories = {
                "x": x,
                "m": m,
                "a": a,
                "s": s,
        }
        return ret

    def __getitem__(self, indices) -> tuple[int, int]:
        return self.categories[indices]

    def combinations(self) -> int:
        return functools.reduce(operator.mul, (end - start for _, (start, end) in self.categories.items()))

    def split(self, category: str, op: str, comp: int, name: str):
        range = self.categories[category]
        if op == "<":
            if range[1] <= comp:
                return [(name, self)]
            elif range[0] < comp:
                return [
                        (name, self.from_new_range(category, (range[0], comp))),
                        (None, self.from_new_range(category, (comp, range[1])))
                ]
            else:
                return (None, self)
        else:
            if range[0] > comp:
                return [(name, self)]
            elif range[1] > comp:
                return [
                        (None, self.from_new_range(category, (range[0], comp + 1))),
                        (name, self.from_new_range(category, (comp + 1, range[1])))
                ]
            else:
                return [(None, self)]

class Rule:
    category: str
    op: str
    comp: int
    output: str
    unconditional: bool

    def __init__(self, rulestr: str):
        match = re.match(r"^[a-zA-Z]+$", rulestr)
        if match:
            # This is the last rule in the workflow and is unconditional
            self.output = rulestr
            self.unconditional = True
            return

        match = re.match(r"([xmas])([<>])(\d+):([a-zA-Z]+)", rulestr)
        if not match:
            raise Exception("Failed to match rule string")
        self.unconditional = False
        self.category = match.group(1)
        self.op = match.group(2)
        self.comp = int(match.group(3))
        self.output = match.group(4)

    def apply(self, partrange: PartRange) -> list[tuple[str | None, PartRange]]:
        if self.unconditional:
            return [(self.output, partrange)]
        return partrange.split(self.category, self.op, self.comp, self.output)

    def __str__(self) -> str:
        if self.unconditional:
            return self.output
        else:
            return self.category + self.op + str(self.comp) + ":" + self.output

class Workflow:
    name: str
    rules: list[Rule]

    def __init__(self, workflowstr: str) -> None:
        match = re.match(r"([a-zA-Z]+){([^}]*)}", workflowstr)
        if not match:
            raise Exception("Failed to match workflow string")
        self.name = match.group(1)
        rules_str = match.group(2)
        rule_strs = rules_str.split(",")
        self.rules = [Rule(rs) for rs in rule_strs]

    def apply(self, partrange: PartRange) -> list[tuple[str, PartRange]]:
        to_apply = [partrange]
        ret: list[tuple[str, PartRange]] = []
        for rule in self.rules:
            print(f"Applying rule: {rule}")
            next_apply: list[PartRange] = []
            for partrange in to_apply:
                out = rule.apply(partrange)
                for o in out:
                    if o[0] is not None:
                        ret.append(o)
                    else:
                        next_apply.append(o[1])
            to_apply = next_apply
            if len(to_apply) == 0:
                return ret

        raise Exception("No rule applied to part")

workflows: dict[str, Workflow] = {}

def num_combinations(partrange: PartRange) -> int:
    combinations = 0
    to_apply: list[tuple[str, PartRange]] = [("in", partrange)]
    while len(to_apply) > 0:
        pr = to_apply.pop()
        out = workflows[pr[0]].apply(pr[1])
        for o in out:
            if o[0] == "A":
                combinations += o[1].combinations()
            elif o[0] != "R":
                to_apply.append(o)

    return combinations

with fileinput.input() as f:
    lines = iter(f)
    for line in lines:
        l = line.rstrip()
        if l == "":
            break

        wf = Workflow(l)
        workflows[wf.name] = wf

    start = PartRange.from_ranges(
            (1, 4001),
            (1, 4001),
            (1, 4001),
            (1, 4001),
    )
    p2 = num_combinations(start)
    print(f"part 2 answer: {p2}")
