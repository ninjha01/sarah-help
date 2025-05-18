#!/usr/bin/env python3
from dataclasses import dataclass
from typing import List
import re


@dataclass
class SpeciesAnnotation:
    id: str
    taxonomy: str
    similarity_threshold: float
    similarity: float
    proportion_threshold: float
    proportion_genome_aligned: float
    warnings: str
    impression: str
    confidence_level: str
    kingdom: str = ""
    phylum: str = ""
    class_name: str = ""
    order: str = ""
    family: str = ""
    genus: str = ""
    species: str = ""

    def __post_init__(self):
        # Parse the taxonomy string to extract individual taxonomy levels
        if self.taxonomy and self.taxonomy.startswith('"d__'):
            tax_parts = self.taxonomy.strip('"').split(";")
            for part in tax_parts:
                if part.startswith("d__"):
                    self.kingdom = part[3:]
                elif part.startswith("p__"):
                    self.phylum = part[3:]
                elif part.startswith("c__"):
                    self.class_name = part[3:]
                elif part.startswith("o__"):
                    self.order = part[3:]
                elif part.startswith("f__"):
                    self.family = part[3:]
                elif part.startswith("g__"):
                    self.genus = part[3:]
                elif part.startswith("s__"):
                    self.species = part[3:]

    def get_lowest_taxonomy(self):
        """
        Returns the lowest available taxonomy level for an annotation.

        Args:
            ann: A SpeciesAnnotation object

        Returns:
            A tuple of (taxonomy_level, taxonomy_name)
        """
        if self.species:
            return ("Species", self.species)
        elif self.genus:
            return ("Genus", self.genus)
        elif self.family:
            return ("Family", self.family)
        elif self.order:
            return ("Order", self.order)
        elif self.class_name:
            return ("Class", self.class_name)
        elif self.phylum:
            return ("Phylum", self.phylum)
        elif self.kingdom:
            return ("Kingdom", self.kingdom)
        else:
            return ("Unknown", self.impression if ann.impression else "Unknown")


def parse_species_annotation(file_path: str) -> List[SpeciesAnnotation]:
    """
    Parse the species annotation file and convert it to a structured format
    using dataclasses.
    """
    annotations = []
    current_id = None
    current_data = {}

    try:
        with open(file_path, "r") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue

                # Check if this is a new ID line
                if line.endswith(":"):
                    # If we have a previous annotation, save it
                    if current_id and current_data:
                        try:
                            annotations.append(
                                SpeciesAnnotation(id=current_id, **current_data)
                            )
                        except Exception as e:
                            print(f"Error creating annotation for {current_id}: {e}")

                    # Start a new annotation
                    current_id = line.rstrip(":")
                    current_data = {}

                # Parse key-value pairs
                elif ":" in line and current_id:
                    key, value = line.split(":", 1)
                    key = key.strip().lower().replace(" ", "_")
                    value = value.strip()

                    # Handle specific fields
                    if key == "taxonomy":
                        current_data["taxonomy"] = value
                    elif key == "similarity_threshold":
                        current_data["similarity_threshold"] = float(value)
                    elif key == "similarity":
                        current_data["similarity"] = float(value)
                    elif key == "proportion_threshold":
                        current_data["proportion_threshold"] = float(value)
                    elif key == "proportion_of_genome_aligned":
                        current_data["proportion_genome_aligned"] = float(value)
                    elif key == "warnings":
                        current_data["warnings"] = value
                    elif key == "impression":
                        current_data["impression"] = value
                    elif "confidence level" in line.lower():
                        # Extract confidence level from the last sentence
                        match = re.search(
                            r"Confidence level[^:]*:\s*(\w+)", line, re.IGNORECASE
                        )
                        if match:
                            current_data["confidence_level"] = match.group(1).lower()

        # Add the last annotation if it exists
        if current_id and current_data:
            try:
                annotations.append(SpeciesAnnotation(id=current_id, **current_data))
            except Exception as e:
                print(f"Error creating annotation for {current_id}: {e}")

        return annotations

    except Exception as e:
        print(f"Error parsing species annotation file {file_path}: {e}")
        return []
