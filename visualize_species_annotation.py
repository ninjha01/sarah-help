#!/usr/bin/env python3
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from pathlib import Path
from typing import List, Dict, Counter, Tuple
from collections import Counter

from parse_species_annotation import parse_species_annotation, SpeciesAnnotation


def visualize_species_annotation(
    annotations: List[SpeciesAnnotation],
) -> Dict[str, go.Figure]:
    # Extract the lowest taxonomy names for each annotation
    taxonomy_data = [ann.get_lowest_taxonomy() for ann in annotations]

    # Count occurrences of each taxonomy name (not just the level)
    name_counts = Counter([name for _, name in taxonomy_data])

    # Sort the data by count (descending)
    sorted_data = sorted(name_counts.items(), key=lambda x: x[1], reverse=True)

    # Get labels and values
    labels = [item[0] for item in sorted_data]
    values = [item[1] for item in sorted_data]

    # Create pie chart
    fig = go.Figure(
        data=[
            go.Pie(
                labels=labels,
                values=values,
                hole=0.3,
                textinfo="label+percent",
                marker=dict(colors=px.colors.qualitative.Plotly),
            )
        ]
    )

    fig.update_layout(
        title_text="Distribution of Lowest Taxonomy Classifications", showlegend=True
    )

    return {
        "Species Annotation Distribution": fig.to_html(
            full_html=False, include_plotlyjs="cdn"
        )
    }
