#!/usr/bin/env python3
from dataclasses import dataclass, field
from typing import List
import re


@dataclass
class Genus:
    name: str
    count: int


@dataclass
class Family:
    name: str
    confidence: str
    count: int
    genera: List[Genus] = field(default_factory=list)


def parse_viral_summary(file_path: str) -> List[Family]:
    """
    Parse the viral summary TSV file and convert it to a structured format
    using dataclasses.
    """
    with open(file_path, "r") as file:
        text = file.read()

    return parse_data(text)


def parse_data(data_string):
    families = []
    current_family = None

    # Split by lines
    lines = data_string.strip().split("\n")

    for line in lines:
        # Check if it's a family line
        family_match = re.match(r"(\d+) (\w+) \[Family\] — (\w+) confidence", line)
        if family_match:
            count = int(family_match.group(1))
            name = family_match.group(2)
            confidence = family_match.group(3)
            current_family = Family(name=name, confidence=confidence, count=count)
            families.append(current_family)
            continue

        # Check if it's a genus line (should be indented)
        genus_match = re.match(r"\s+(\d+) (\w+) \[Genus\]", line)
        if genus_match and current_family:
            count = int(genus_match.group(1))
            name = genus_match.group(2)
            current_family.genera.append(Genus(name=name, count=count))

    return families
