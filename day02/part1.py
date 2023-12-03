import argparse
from pathlib import Path
import sys

import pytest

this_file = Path(__file__)
INPUT_TXT = this_file.parent / (this_file.stem + ".txt")


# The Elf would first like to know which games would have been possible if the
# bag contained only 12 red cubes, 13 green cubes, and 14 blue cubes?
INVENTORY = {"red": 12, "green": 13, "blue": 14}


def turn_dict(
    s: str,
) -> dict[str, int]:
    dct = {}
    for lst in s.split(", "):
        n, color = lst.split(" ")
        dct.update({color: int(n)})
    return dct


def rest_to_game(
    s: str,
) -> list[dict[str, int]]:
    return [turn_dict(draw) for draw in s.strip().split("; ")]


def parse_line(
    s: str,
) -> tuple[int, str]:
    game_x, _, rest = s.partition(":")
    _, _, num = game_x.partition(" ")
    game_num = int(num)
    return game_num, rest


def is_possible(
    game: list[dict[str, int]],
) -> bool:
    for dct in game:
        for k, v in dct.items():
            if INVENTORY.get(k) < v:
                return False
    return True


def solve_aoc(s: str) -> int:
    total = 0
    for line in s.splitlines():
        n, rest = parse_line(line)
        game = rest_to_game(rest)
        if is_possible(game):
            total += n
    return total


SAMPLE = """\
Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green
"""
EXPECTED = 8


@pytest.mark.parametrize(
    ("sample", "expected"),
    ((SAMPLE, EXPECTED),),
)
def test_solve(sample: str, expected: int) -> None:
    assert solve_aoc(sample) == expected


def test_turn_dict():
    expected = {"blue": 3, "red": 4}
    output = turn_dict("3 blue, 4 red")
    assert expected == output


def test_rest_to_game():
    expected = [{"blue": 3, "red": 4}, {"red": 1, "green": 2, "blue": 6}, {"green": 2}]
    output = rest_to_game("3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green")
    assert expected == output


def test_parse_line():
    expected = (1, " 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green")
    output = parse_line("Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green")
    assert expected == output


def test_is_possible():
    expected = True
    example_game = [
        {"blue": 3, "red": 4},
        {"red": 1, "green": 2, "blue": 6},
        {"green": 2},
    ]
    output = is_possible(example_game)
    assert expected is output


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", nargs="?", default=INPUT_TXT)
    args = parser.parse_args()
    input_s = Path(args.input_file).read_text(encoding="utf-8")
    print(solve_aoc(input_s))
    return 0


if __name__ == "__main__":
    raise sys.exit(main())
