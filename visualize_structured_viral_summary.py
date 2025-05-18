#!/usr/bin/env python3
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from pathlib import Path
from typing import List, Dict

from parse_structured_viral_summary import parse_viral_summary, Family


def create_family_bar_chart(families: List[Family]) -> str:
    """
    Create a bar chart of viral families.

    Returns:
        HTML string representation of the chart
    """
    # Create a DataFrame for the plot
    df = pd.DataFrame(
        [
            {
                "Family": family.name,
                "Count": family.count,
                "Confidence": family.confidence,
            }
            for family in families
        ]
    )

    # Sort by count in descending order
    df = df.sort_values("Count", ascending=False)

    # Create a bar chart with colors based on confidence
    fig = px.bar(
        df,
        x="Family",
        y="Count",
        color="Confidence",
        color_discrete_map={"High": "green", "Moderate": "orange", "Low": "red"},
        title="Viral Families Distribution",
        template="plotly",
    )

    fig.update_layout(
        xaxis_title="Viral Family", yaxis_title="Count", legend_title="Confidence Level"
    )

    # Convert to HTML
    return fig.to_html(full_html=False, include_plotlyjs="cdn")


def generate_viral_summary_html(families: List[Family]) -> str:
    """
    Generate HTML content that mimics the nested structure of the source file.

    Args:
        families: List of Family objects with genera

    Returns:
        HTML string representation
    """
    # Sort families by count (descending)
    families.sort(key=lambda f: f.count, reverse=True)

    # Add CSS for styling
    html = """
    <style>
        .viral-container {
            font-family: monospace;
            max-width: 100%;
            white-space: pre-wrap;
            line-height: 1.5;
            padding: 15px;
            background-color: #f5f5f5;
            border-radius: 5px;
            border: 1px solid #ddd;
        }
        .family-line {
            font-weight: bold;
        }
        .genus-line {
            margin-left: 20px;
            color: #444;
        }
        .confidence-high {
            color: green;
        }
        .confidence-moderate {
            color: orange;
        }
        .confidence-low {
            color: red;
        }
    </style>
    """
    html += '<div class="viral-container">\n'

    # For each viral family
    for family in families:
        # Add confidence color class based on level
        confidence_class = ""
        if family.confidence.lower() == "high":
            confidence_class = "confidence-high"
        elif family.confidence.lower() == "moderate":
            confidence_class = "confidence-moderate"
        elif family.confidence.lower() == "low":
            confidence_class = "confidence-low"

        # Create family line mimicking the source format
        html += f'<details class="family-line"><summary class="{confidence_class}">{family.count} {family.name} [Family] — {family.confidence} confidence</summary>\n'

        # Add genera information if available
        if family.genera:
            # Sort genera by read count (descending)
            sorted_genera = sorted(family.genera, key=lambda g: g.count, reverse=True)

            # Add each genus as indented line
            for genus in sorted_genera:
                html += f'<div class="genus-line">{genus.count} {genus.name} [Genus]</div>\n'
        html += "</details>\n"  # Close details for family
    html += "</div>\n"  # Close viral-container

    return html


def visualize_viral_summary(families: List[Family]):
    """
    Create visualizations for the viral summary data.
    Returns a dictionary of visualization titles and their HTML string representations.

    Args:
        families: List of Family objects

    Returns:
        Dictionary of visualization titles and their HTML content
    """
    # Create the visualizations
    visualizations = {}

    # Family distribution bar chart
    bar_chart_html = create_family_bar_chart(families)
    visualizations["Viral Families Distribution"] = bar_chart_html

    # Generate formatted viral taxonomy list
    viral_summary_html = generate_viral_summary_html(families)
    visualizations["Viral Taxonomy List"] = viral_summary_html

    return visualizations
