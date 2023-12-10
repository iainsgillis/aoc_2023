import argparse
import collections
from pathlib import Path
import sys

import pytest

this_file = Path(__file__)
INPUT_TXT = this_file.parent / (this_file.stem + ".txt")


def hand_type(hand: str) -> tuple:
    return tuple(sorted(collections.Counter(hand).values(), reverse=True))


def hand_tiebreak(hand: str) -> int:
    return tuple("23456789TJQKA".index(c) for c in hand)


def solve_aoc(s: str) -> int:
    lst = [
        (hand, (hand_type(hand), hand_tiebreak(hand)), int(bid))
        for hand, bid in (line.split() for line in s.splitlines())
    ]
    return sum(
        item[-1] * i for i, item in enumerate(sorted(lst, key=lambda x: x[1]), start=1)
    )


SAMPLE = """\
32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483
"""
EXPECTED = 6440


@pytest.mark.parametrize(
    ("sample", "expected"),
    ((SAMPLE, EXPECTED),),
)
def test_solve(sample: str, expected: int) -> None:
    assert solve_aoc(sample) == expected


def test_hand_type() -> None:
    import random

    hands = "AAAAA AA8AA 23332 TTT98 23432 A23A4 23456".split()
    random.shuffle(hands)
    sort_asc = "23456 A23A4 23432 TTT98 23332 AA8AA AAAAA".split()
    assert sorted(hands, key=hand_type) == sort_asc


def test_hand_tiebreak() -> None:
    four_of_a_kind = "2AAAA 33332".split()
    full_house = "77788 77888".split()
    assert sorted(four_of_a_kind, key=hand_tiebreak) == four_of_a_kind
    assert sorted(full_house, key=hand_tiebreak) == full_house


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", nargs="?", default=INPUT_TXT)
    args = parser.parse_args()
    input_s = Path(args.input_file).read_text(encoding="utf-8")
    print(solve_aoc(input_s))
    return 0


if __name__ == "__main__":
    raise sys.exit(main())
