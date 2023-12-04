import argparse
from pathlib import Path
import re
import sys

import pytest

this_file = Path(__file__)
INPUT_TXT = this_file.parent / (this_file.stem + ".txt")


def solve_aoc(s: str) -> int:
    total = 0
    for line in s.splitlines():
        _, nums = line.split(":")
        winning_s, mine_s = nums.split("|")
        winning = {int(x) for x in re.split("\\s+", winning_s.strip())}
        mine = {int(x) for x in re.split("\\s+", mine_s.strip())}
        in_common = winning & mine
        if len(in_common) == 0:
            continue
        score = 2 ** (len(in_common) - 1)
        total += score
    return total


SAMPLE = """\
Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11
"""
EXPECTED = 13


@pytest.mark.parametrize(
    ("sample", "expected"),
    ((SAMPLE, EXPECTED),),
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
