import argparse
import functools
from pathlib import Path
import sys

import pytest

this_file = Path(__file__)
INPUT_TXT = this_file.parent / (this_file.stem + ".txt")


def parse_input(s: str) -> list[tuple[int]]:
    time, distance = s.splitlines()
    times = [int(n) for n in time.split()[1:]]
    distances = [int(n) for n in distance.split()[1:]]
    return list(zip(times, distances))


def solve_aoc(s: str) -> int:
    factors = []
    for race_duration, record_distance in parse_input(s):
        number_of_ways_to_beat_this_record = 0
        for hold_time in range(1, race_duration + 1):
            speed = hold_time
            distance = speed * (race_duration - hold_time)
            if record_distance < distance:
                number_of_ways_to_beat_this_record += 1
        factors.append(number_of_ways_to_beat_this_record)
    return functools.reduce(lambda x, y: x * y, factors)


SAMPLE = """\
Time:      7  15   30
Distance:  9  40  200
"""
EXPECTED = 288


@pytest.mark.parametrize(
    ("sample", "expected"),
    ((SAMPLE, EXPECTED),),
)
def test_solve(sample: str, expected: int) -> None:
    assert solve_aoc(sample) == expected


def test_parse_input() -> None:
    assert parse_input(SAMPLE) == [(7, 9), (15, 40), (30, 200)]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", nargs="?", default=INPUT_TXT)
    args = parser.parse_args()
    input_s = Path(args.input_file).read_text(encoding="utf-8")
    print(solve_aoc(input_s))
    return 0


if __name__ == "__main__":
    raise sys.exit(main())
