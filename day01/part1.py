import argparse
from pathlib import Path
import re
import sys

import pytest

this_file = Path(__file__)
INPUT_TXT = this_file.stem + ".txt"


def solve_aoc(s: str) -> int:
    total = 0
    for line in s.splitlines():
        digits = re.findall(r"\d", line)
        num = int(digits[0] + digits[-1])
        total += num
    return total


SAMPLE = """\
1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet
"""
EXPECTED = 142


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
