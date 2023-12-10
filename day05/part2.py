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


def seed_gen(parsed: dict[str, str]) -> list[tuple[int]]:
    line = parsed.get("seeds")
    _, txt = line.split(":")
    first_pass = [int(n) for n in txt.split()]
    return [
        (start, start + n - 1) for (start, n) in zip(first_pass[::2], first_pass[1::2])
    ]


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
    pairs = seed_gen(parsed)
    maps = [get_mapping(k, parsed) for k in parsed if k != "seeds"]
    locations = []
    for pair in pairs:
        to_process = [pair]
        candidates = []
        for m in maps:
            while to_process:
                current = to_process.pop()
                l_seed, r_seed = current
                overlap_in_at_least_one_part_of_the_map = False
                for l_src, l_dst, n in m:
                    src_r = l_src + n
                    if r_seed < l_src or src_r <= l_seed:
                        continue

                    overlapping = (max(l_seed, l_src), min(r_seed, src_r) - 1)
                    if overlapping[0] <= overlapping[1]:
                        offset = overlapping[0] - l_src
                        overlap_length = overlapping[1] - overlapping[0]
                        output_range = l_dst + offset
                        mapped = (output_range, output_range + overlap_length)
                        candidates.append(mapped)

                    left_of_lbound = (min(l_seed, l_src), min(r_seed, l_src) - 1)
                    if left_of_lbound[0] <= left_of_lbound[1]:
                        to_process.append(left_of_lbound)

                    right_of_rbound = (max(l_seed, src_r), max(r_seed, src_r) - 1)
                    if right_of_rbound[0] <= right_of_rbound[1]:
                        to_process.append(right_of_rbound)

                    overlap_in_at_least_one_part_of_the_map = True
                    break
                if not overlap_in_at_least_one_part_of_the_map:
                    candidates.append(current)
            to_process = candidates
            candidates = []
        locations.extend(to_process)

    return min(l for (l, _) in locations)


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
EXPECTED = 46


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
