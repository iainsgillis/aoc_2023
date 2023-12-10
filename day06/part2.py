import argparse
import functools
from pathlib import Path
import sys

import pytest

this_file = Path(__file__)
INPUT_TXT = this_file.parent / (this_file.stem + ".txt")


def parse_input(s: str) -> tuple[int]:
    time, distance = s.splitlines()
    *_, time_parts = time.partition(":")
    *_, distance_parts = distance.partition(":")
    t = int("".join(time_parts.split()))
    d = int("".join(distance_parts.split()))
    return (t, d)


def solve_aoc(s: str) -> int:
    race_duration, record_distance = parse_input(s)
    number_of_ways_to_beat_this_record = 0
    for hold_time in range(race_duration):
        speed = hold_time
        distance = speed * (race_duration - hold_time)
        if record_distance < distance:
            number_of_ways_to_beat_this_record += 1
    return number_of_ways_to_beat_this_record


SAMPLE = """\
Time:      7  15   30
Distance:  9  40  200
"""
EXPECTED = 71503


@pytest.mark.parametrize(
    ("sample", "expected"),
    ((SAMPLE, EXPECTED),),
)
def test_solve(sample: str, expected: int) -> None:
    assert solve_aoc(sample) == expected


def test_parse_input() -> None:
    assert parse_input(SAMPLE) == (71530, 940200)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", nargs="?", default=INPUT_TXT)
    args = parser.parse_args()
    input_s = Path(args.input_file).read_text(encoding="utf-8")
    print(solve_aoc(input_s))
    return 0


if __name__ == "__main__":
    raise sys.exit(main())
