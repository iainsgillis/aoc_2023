import argparse
from pathlib import Path
import re
import sys

import pytest

this_file = Path(__file__)
INPUT_TXT = this_file.stem + ".txt"


def find_symbols(s: str) -> list[list[int, int]]:
    ignore_set = set("0123456789.")
    grid = []
    for i, line in enumerate(s.splitlines()):
        for j, char in enumerate(line):
            if char in ignore_set:
                continue
            grid.append([i, j])
    return grid


def find_part_numbers(s: str) -> list[list[int, int]]:
    nums = []
    ignore_set = set("0123456789.")
    lines = s.splitlines()
    for i, line in enumerate(lines):
        for m in re.finditer("\\d+", line):
            for i_ in range(max(0, i - 1), min(len(lines) - 1, i + 1) + 1):
                for j_ in range(max(0, m.start() - 1), min(len(line) - 1, m.end() + 1)):
                    if lines[i_][j_] not in ignore_set:
                        nums.append(int(m.group()))
                        break
    return nums


def solve_aoc(s: str) -> int:
    parts = find_part_numbers(s)
    return sum(parts)


SAMPLE = """\
467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..
"""
EXPECTED = 4361


@pytest.mark.parametrize(
    ("sample", "expected"),
    ((SAMPLE, EXPECTED),),
)
def test_solve(sample: str, expected: int) -> None:
    assert solve_aoc(sample) == expected


def test_find_symbols() -> None:
    sample = """\
......#
617*...
.....+.
"""
    expected = [[0, 6], [1, 3], [2, 5]]
    output = find_symbols(sample)
    assert expected == output


@pytest.mark.parametrize(
    "sample, expected",
    [
        ("......#\n*...617\n.....+.", [617]),
        ("467..\n...*.\n..35.", [467, 35]),
        ("......#\n617.*..\n.....+.", []),
    ],
)
def test_find_part_numbers(sample, expected):
    output = find_part_numbers(sample)
    assert expected == output


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", nargs="?", default=INPUT_TXT)
    args = parser.parse_args()
    input_s = Path(args.input_file).read_text(encoding="utf-8")
    print(solve_aoc(input_s))
    return 0


if __name__ == "__main__":
    raise sys.exit(main())
