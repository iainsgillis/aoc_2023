import argparse
from collections import namedtuple
from pathlib import Path
import re
import sys

import pytest

this_file = Path(__file__)
INPUT_TXT = this_file.parent / (this_file.stem + ".txt")


def find_gear_candidates(s: str) -> list[list[int, int]]:
    candidates = []
    for i, line in enumerate(s.splitlines()):
        for j, char in enumerate(line):
            if char != "*":
                continue
            candidates.append([i, j])
    return candidates


PartNumber = namedtuple("PartNumber", ["value", "row", "start", "end"])


def find_part_numbers(s: str) -> list[PartNumber]:
    nums = []
    ignore_set = set("0123456789.")
    lines = s.splitlines()
    for i, line in enumerate(lines):
        for m in re.finditer("\\d+", line):
            for i_ in range(max(0, i - 1), min(len(lines) - 1, i + 1) + 1):
                for j_ in range(max(0, m.start() - 1), min(len(line) - 1, m.end() + 1)):
                    if lines[i_][j_] not in ignore_set:
                        part_number = PartNumber(int(m.group()), i, m.start(), m.end())
                        nums.append(part_number)
                        break
    return nums


def filter_candidates(
    gear_candidates: list[list[int, int]], parts: list[PartNumber]
) -> list[int]:
    ratios = []
    for gc in gear_candidates:
        row, col = gc
        # adjacent = [
        #     part
        #     for part in parts
        #     if (abs(part.row - row) == 1 and (part.start - 1 <= col <= part.end + 1))
        # ]
        adjacent = [part for part in parts if abs(part.row - row) <= 1 and col in range(part.start - 1, part.end + 1)]


        if len(adjacent) != 2:
            continue
        gear_ratio = adjacent[0].value * adjacent[-1].value
        ratios.append(gear_ratio)
    return ratios


def solve_aoc(s: str) -> int:
    parts = find_part_numbers(s)
    gear_candidates = find_gear_candidates(s)
    gear_ratios = filter_candidates(gear_candidates, parts)
    return sum(gear_ratios)


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
EXPECTED = 467835


@pytest.mark.parametrize(
    ("sample", "expected"),
    ((SAMPLE, EXPECTED),),
)
def test_solve(sample: str, expected: int) -> None:
    assert solve_aoc(sample) == expected


def test_find_gear_candidates() -> None:
    sample = """\
467..
...*.
..35.
.....
617*.
.....
"""
    expected = [[1, 3], [4, 3]]
    output = find_gear_candidates(sample)
    assert expected == output


@pytest.mark.parametrize(
    "sample, expected",
    [
        ("......#\n*...617\n.....+.", [PartNumber(617, 1, 4, 7)]),
        (
            "467..\n...*.\n..35.",
            [PartNumber(467, 0, 0, 3), PartNumber(35, 2, 2, 4)],
        ),
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
