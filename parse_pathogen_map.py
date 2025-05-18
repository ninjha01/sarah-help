#!/usr/bin/env python3
from dataclasses import dataclass, field
from typing import List
import re


@dataclass
class Strain:
    name: str
    reads: int


@dataclass
class PathogenSpecies:
    name: str
    total_reads: int
    strains: List[Strain] = field(default_factory=list)


def parse_pathogen_map(file_path: str) -> List[PathogenSpecies]:
    pathogens = []
    current_species = None

    try:
        with open(file_path, "r") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue

                # Check if this is a species line
                species_match = re.match(
                    r"Species:\s+(.+)\s+Total_Reads:\s+(\d+)", line
                )

                # Check if this is a strain line
                strain_match = re.match(r"\s*Strain:\s+(.*?)\s+Reads:\s+(\d+)", line)

                if species_match:
                    species_name = species_match.group(1).strip()
                    total_reads = int(species_match.group(2))

                    current_species = PathogenSpecies(
                        name=species_name, total_reads=total_reads
                    )
                    pathogens.append(current_species)
                elif strain_match and current_species:
                    strain_name = strain_match.group(1).strip()
                    reads = int(strain_match.group(2))
                    current_species.strains.append(
                        Strain(name=strain_name, reads=reads)
                    )
                else:
                    print(f"Unrecognized line format: {line}")
                    continue
        return pathogens

    except Exception as e:
        print(f"Error parsing pathogen map file {file_path}: {e}")
        return []
