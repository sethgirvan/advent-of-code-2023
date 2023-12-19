from collections.abc import Callable

import fileinput
import operator
import re

class Part:
    categories: dict[str, int]

    def __init__(self, partstr: str) -> None:
        match = re.match(r"{x=(\d+),m=(\d+),a=(\d+),s=(\d+)}", partstr)
        if not match:
            raise Exception("Failed to match part string")
        self.categories = {
                "x": int(match.group(1)),
                "m": int(match.group(2)),
                "a": int(match.group(3)),
                "s": int(match.group(4)),
        }

    def __getitem__(self, indices) -> int:
        return self.categories[indices]

    def sum(self) -> int:
        return sum(v for _, v in self.categories.items())

class Rule:
    category: str
    op: Callable
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
        self.op = operator.lt if match.group(2) == "<" else operator.gt
        self.comp = int(match.group(3))
        self.output = match.group(4)

    def apply(self, part: Part) -> str | None:
        if self.unconditional:
            return self.output
        val = part[self.category]
        if self.op(val, self.comp):
            return self.output
        return None

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

    def apply(self, part: Part) -> str:
        for rule in self.rules:
            out = rule.apply(part)
            if out is not None:
                return out
        raise Exception("No rule applied to part")

workflows: dict[str, Workflow] = {}

def part_is_accepted(part: Part) -> bool:
    name = "in"
    while True:
        name = workflows[name].apply(part)

        if name == "A":
            return True
        if name == "R":
            return False

with fileinput.input() as f:
    lines = iter(f)
    for line in lines:
        l = line.rstrip()
        if l == "":
            break

        wf = Workflow(l)
        workflows[wf.name] = wf

    parts = (Part(line.rstrip()) for line in lines)
    p1 = sum(part.sum() for part in parts if part_is_accepted(part))
    print(f"part 1 answer: {p1}")
