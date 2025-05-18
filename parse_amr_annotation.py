from dataclasses import dataclass, field
from typing import List, Dict, Optional


@dataclass
class ResistanceMechanism:
    name: str
    count: int


@dataclass
class AMRAnnotation:
    name: str
    count: int
    mechanisms: List[ResistanceMechanism] = field(default_factory=list)


def parse_amr_annotation(file_path: str) -> List[AMRAnnotation]:
    """
    Parse an AMR summary report into structured data.

    Args:
        text: Multiline string of the report.

    Returns:
        Dictionary mapping bin names to lists of AMRAnnotation instances.
    """
    with open(file_path, "r") as f:
        text = f.read()

    bins: Dict[str, List[AMRAnnotation]] = {}
    current_bin: Optional[str] = None
    current_class: Optional[AMRAnnotation] = None

    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("[INFO]"):
            continue

        # Detect new bin
        if line.startswith("### Bin:"):
            bin_name = line[len("### Bin:") :].strip()
            bins[bin_name] = []
            current_bin = bin_name
            current_class = None
            continue

        # Detect mechanism lines (indented with dash)
        if line.startswith("- ") and current_bin and current_class:
            mech_text = line[2:]
            # Split name and count
            try:
                name_part, count_part = mech_text.rsplit("(", 1)
                name = name_part.strip()
                count = int(count_part.rstrip(")"))
            except ValueError:
                continue
            mechanism = ResistanceMechanism(name=name, count=count)
            bins[current_bin][-1].mechanisms.append(mechanism)
            continue

        # Otherwise, treat as antibiotic class line
        if current_bin:
            # Expect "<name> (<count>)"
            try:
                name_part, count_part = line.rsplit("(", 1)
                name = name_part.strip()
                count = int(count_part.rstrip(")"))
            except ValueError:
                continue
            ab_class = AMRAnnotation(name=name, count=count)
            bins[current_bin].append(ab_class)
            current_class = ab_class

    anns = list(bins.values())
    return anns[0]
