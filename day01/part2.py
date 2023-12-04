import argparse
from pathlib import Path
import re
import sys

import pytest

this_file = Path(__file__)
INPUT_TXT = this_file.parent / (this_file.stem + ".txt")


subs = {
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
}


def make_subs(raw: str) -> str:
    subbed = ""
    for i, char in enumerate(raw):
        if char.isdigit():
            subbed += char
            continue
        for k, v in subs.items():
            if raw[i:].startswith(k):
                subbed += v
                break
    return subbed


def solve_aoc(s: str) -> int:
    total = 0
    for line in map(make_subs, s.splitlines()):
        digits = re.findall(r"\d", line)
        num = int(digits[0] + digits[-1])
        total += num
    return total


SAMPLE = """\
two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen
"""
EXPECTED = 281


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
