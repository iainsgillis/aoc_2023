import argparse
from pathlib import Path
import sys

import pytest

this_file = Path(__file__)
INPUT_TXT = this_file.parent / (this_file.stem + ".txt")


def solve_aoc(s: str) -> int:
    d = {"L": 0, "R": 1}
    pattern, rest = s.split("\n\n")
    network = {l[:3]: (l[7:10], l[12:15]) for l in rest.splitlines()}
    current = "AAA"
    total = 0
    while current != "ZZZ":
        idx = d[pattern[total % len(pattern)]]
        total += 1
        current = network[current][idx]
    return total


SAMPLE1 = """\
RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)
"""
EXPECTED1 = 2


SAMPLE2 = """\
LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)
"""

EXPECTED2 = 6


@pytest.mark.parametrize(
    ("sample", "expected"), ((SAMPLE1, EXPECTED1), (SAMPLE2, EXPECTED2))
)
def test_solve(sample: str, expected: int) -> None:
    assert solve_aoc(sample) == expected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", nargs="?", default=INPUT_TXT)
    args = parser.parse_args()
    input_s = Path(args.input_file).read_text(encoding="utf-8")
    print(solve_aoc(input_s))
    return 0


if __name__ == "__main__":
    raise sys.exit(main())
