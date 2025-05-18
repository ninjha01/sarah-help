#!/usr/bin/env python3
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from pathlib import Path
from typing import List, Dict

from parse_amr_annotation import (
    AMRAnnotation,
    ResistanceMechanism,
)


def create_antibiotic_classes_bar_chart(
    annotations: List[AMRAnnotation],
    organism: str = "",
) -> str:
    """
    Create a grouped bar chart of antibiotic‐resistance counts for a single organism.

    Returns:
        HTML string representation of the chart
    """
    # build a DataFrame where every row has the same organism name
    df = pd.DataFrame(
        [{"Organism": organism, "Class": a.name, "Count": a.count} for a in annotations]
    )

    # grouped bar chart, one group (organism) with bars coloured by Class
    fig = px.bar(
        df,
        x="Organism",
        y="Count",
        color="Class",
        barmode="group",
        text="Count",
        title="Antibiotic Resistance Classes",
        labels={
            "Organism": "",
            "Count": "Number of Occurrences",
            "Class": "Antibiotic Class",
        },
        template="plotly",
    )

    # move the counts just above each bar
    fig.update_traces(textposition="outside")
    # remove any x‐tick rotation (we only have one tick)
    fig.update_layout(
        xaxis_tickangle=0,
        showlegend=True,
        plot_bgcolor="rgba(230, 236, 240, 1)",  # match the light grey panel
    )

    # return as embeddable HTML
    return fig.to_html(include_plotlyjs="cdn", full_html=False)


def create_resistance_mechanism_chart(annotations: List[AMRAnnotation]) -> str:
    """
    Create a stacked bar chart showing resistance mechanisms with antibiotic classes.
    Each bar represents a resistance mechanism, and each "slice" represents an antibiotic class.

    Returns:
        HTML string representation of the chart
    """
    # Prepare data for stacked bar chart
    data = []
    for ann in annotations:
        for mech in ann.mechanisms:
            data.append({
                "Class": ann.name,
                "Mechanism": mech.name,
                "Count": mech.count
            })
    
    df = pd.DataFrame(data)
    if df.empty:
        # No mechanism data
        fig = go.Figure()
        fig.add_annotation(
            text="No resistance mechanism data available",
            xref="paper",
            yref="paper",
            x=0.5,
            y=0.5,
            showarrow=False,
        )
        return fig.to_html(full_html=False, include_plotlyjs="cdn")
    
    # Group by Mechanism and Class to get counts
    df_grouped = df.groupby(["Mechanism", "Class"], as_index=False)["Count"].sum()
    
    # Create stacked bar chart
    fig = px.bar(
        df_grouped,
        x="Mechanism",
        y="Count",
        color="Class",
        title="Resistance Mechanisms by Antibiotic Class",
        template="plotly",
        barmode="stack",
    )
    
    fig.update_layout(
        xaxis_title="Resistance Mechanism",
        yaxis_title="Count",
        plot_bgcolor="#EBF0F8",
        height=600,
        width=900,
        xaxis=dict(tickangle=45),
    )

    return fig.to_html(full_html=False, include_plotlyjs="cdn")


def visualize_amr_annotation(annotations: List[AMRAnnotation]) -> Dict[str, str]:
    """
    Create visualizations for the AMR annotation data using the new data model.
    Returns a dict mapping chart titles to their HTML strings.

    Args:
        file_path: Path to the AMR annotation file
        output_dir: Optional directory to save HTML files

    Returns:
        Dict[str, str]: title → chart HTML
    """
    # Parse using the updated model
    # Prepare output dir

    visuals: Dict[str, str] = {}

    # Antibiotic classes chart
    html1 = create_antibiotic_classes_bar_chart(annotations)
    visuals["Antibiotic Classes Bar Chart"] = html1

    # Resistance mechanisms chart
    html2 = create_resistance_mechanism_chart(annotations)
    visuals["Resistance Mechanism Chart"] = html2

    return visuals
