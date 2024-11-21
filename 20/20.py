from abc import ABC, abstractmethod
from collections import deque
from typing import cast
import fileinput
import re

class Module(ABC):
    name = ""
    outputs: list[str] = []

    def __init__(self, name: str, outputs: list[str]) -> None:
        self.name = name
        self.outputs = outputs

    def pulse_out(self, level: bool) -> list[tuple[str, str, bool]]:
        return [(self.name, output, level) for output in self.outputs]

    @abstractmethod
    def pulse_in(self, inpt: str, level: bool) -> list[tuple[str, str, bool]]:
        raise NotImplementedError

class FlipFlop(Module):
    state = False

    def pulse_in(self, inpt: str, level: bool) -> list[tuple[str, str, bool]]:
        if not level:
            self.state = not self.state
            return self.pulse_out(self.state)
        return []

class Conjunction(Module):
    inpts: dict[str, bool] = {}

    def __init__(self, name: str, outputs: list[str]):
        super().__init__(name, outputs)
        self.inpts = {}

    def add_inpt(self, inpt: str) -> None:
        self.inpts[inpt] = False

    def pulse_in(self, inpt: str, level: bool) -> list[tuple[str, str, bool]]:
        self.inpts[inpt] = level
        if all(self.inpts.values()):
            return self.pulse_out(False)
        return self.pulse_out(True)

class Broadcaster(Module):
    def pulse_in(self, inpt: str, level: bool) -> list[tuple[str, str, bool]]:
        return self.pulse_out(level)

def parse_module(line: str) -> tuple[type[Module], str, list[str]]:
    if line[0] == "%":
        module_type = FlipFlop
        name = line.split(maxsplit=1)[0][1:]
    elif line[0] == "&":
        module_type = Conjunction
        name = line.split(maxsplit=1)[0][1:]
    elif line.startswith("broadcaster"):
        module_type = Broadcaster
        name = "broadcaster"
    else:
        raise Exception("Unknown module type")

    outputs = "".join(re.sub(r"^[^>]*>", "", line).split()).split(",")

    return (module_type, name, outputs)


lines = [line.rstrip() for line in fileinput.input()]
# Create modules pointing to their respective outputs. We will tell Conjunction
# modules which modules are connected to them as inputs in the next pass.
modules: dict[str, Module] = {}
for line in lines:
    module_type, name, outputs = parse_module(line)
    modules[name] = module_type(name, outputs)

# Now tell Conjunction modules about their inputs.
for line in lines:
    _, name, outputs = parse_module(line)
    for output in outputs:
        if output in modules and isinstance(modules[output], Conjunction):
            cast(Conjunction, modules[output]).add_inpt(name)

high_pulse_count = 0
low_pulse_count = 0

def push_button() -> None:
    pulses: deque[tuple[str, str, bool]] = deque([("button", "broadcaster", False)])
    while len(pulses) > 0:
        inpt, name, level = pulses.popleft()

        global high_pulse_count
        global low_pulse_count
        if level:
            high_pulse_count += 1
        else:
            low_pulse_count += 1

        if name in modules:
            module = modules[name]
            pulses.extend(module.pulse_in(inpt, level))

for i in range(0, 1000):
    push_button()

p1_answer = high_pulse_count * low_pulse_count

print(f"high pulse count: {high_pulse_count}, low pulse count: {low_pulse_count}")
print(f"p1 answer: {p1_answer}")
