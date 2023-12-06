import argparse
from pathlib import Path
import sys

import pytest

this_file = Path(__file__)
INPUT_TXT = this_file.parent / (this_file.stem + ".txt")


def parse_input(s: str) -> dict[str, str]:
    (
        seeds,
        seed_to_soil,
        soil_to_fertilizer,
        fertilizer_to_water,
        water_to_light,
        light_to_temperature,
        temperature_to_humidity,
        humidity_to_location,
    ) = s.split("\n\n")
    return {
        "seeds": seeds,
        "seed_to_soil": seed_to_soil,
        "soil_to_fertilizer": soil_to_fertilizer,
        "fertilizer_to_water": fertilizer_to_water,
        "water_to_light": water_to_light,
        "light_to_temperature": light_to_temperature,
        "temperature_to_humidity": temperature_to_humidity,
        "humidity_to_location": humidity_to_location,
    }


def get_seeds(parsed: dict[str, str]) -> list[int]:
    line = parsed.get("seeds")
    _, txt = line.split(":")
    return [int(n) for n in txt.split()]


def get_mapping(key: str, parsed: dict[str, str]) -> list[tuple[int]]:
    mapping = []
    lines = parsed.get(key).splitlines()
    for line in lines[1:]:
        dst_start, src_start, rng_len = [int(n) for n in line.split()]
        mapping.append((src_start, dst_start, rng_len))
    return mapping


def calc_output(val: int, mapping: list[tuple[int]]) -> int:
    for src_start, dst_start, rng_len in mapping:
        if src_start <= val <= (src_start + rng_len):
            return dst_start - src_start + val
    return val


def solve_aoc(s: str) -> int:
    parsed = parse_input(s)
    seeds = get_seeds(parsed)
    maps = [get_mapping(k, parsed) for k in parsed if k != "seeds"]
    locations = []
    for seed in seeds:
        val = seed
        for m in maps:
            val = calc_output(val, m)
        locations.append(val)
    return min(locations)


SAMPLE = """\
seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4
"""
EXPECTED = 35


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
