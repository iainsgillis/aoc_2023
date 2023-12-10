import argparse
from pathlib import Path
import sys
import time

import pytest

this_file = Path(__file__)
INPUT_TXT = this_file.parent / (this_file.stem + ".txt")


def lcm(a, b):
    def gcd(a, b):
        while b:
            a, b = b, a % b
        return a

    return abs(a * b) // gcd(a, b)


def solve_aoc(s: str) -> int:
    d = {"L": 0, "R": 1}
    pattern, rest = s.split("\n\n")
    network = {l[:3]: (l[7:10], l[12:15]) for l in rest.splitlines()}

    # using LCM -- snappy
    starters = [k for k in network if k.endswith("A")]
    N = 1
    while starters:
        current = starters.pop()
        path = [current]
        total = 0
        while not current.endswith("Z"):
            idx = d[pattern[total % len(pattern)]]
            total += 1
            next = network[current][idx]
            path.append(next)
            current = next
        N = lcm(N, total)
    return N

    # brute force -- infeasible. Maybe in a compiled language?
    # start = time.perf_counter()
    # current = [k for k in network if k.endswith("A")]
    # total = 0
    # while not all(k.endswith("Z") for k in current):
    #     idx = d[pattern[total % len(pattern)]]
    #     total += 1
    #     current = [network[k][idx] for k in current]
    # print(f"{round(time.perf_counter() - start):_}")
    # return total


SAMPLE1 = """\
LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)
"""
EXPECTED1 = 6


@pytest.mark.parametrize(("sample", "expected"), ((SAMPLE1, EXPECTED1),))
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
