#!/usr/bin/env python3
from typing import List, Dict, Any
from pathlib import Path
from parse_pathogen_map import parse_pathogen_map, PathogenSpecies, Strain
from parse_species_annotation import SpeciesAnnotation
import plotly.graph_objects as go
import plotly
from plotly.subplots import make_subplots


def visualize_pathogen_map(pathogens, species_data: List[SpeciesAnnotation]):
    """
    Visualize the pathogen map data using HTML <details> and <summary> tags.

    Args:
        pathogens: List of pathogen dictionaries
        file_path: Path to save the HTML file

    Returns:
        HTML string representation
    """
    # Convert dictionaries to PathogenSpecies objects if needed
    pathogen_objects = []
    for p in pathogens:
        # If the input is already in the right format, use it directly
        if isinstance(p, PathogenSpecies):
            pathogen_objects.append(p)
        else:
            # Otherwise, construct PathogenSpecies objects from dictionaries
            strains = []
            if "strains" in p:
                for s in p["strains"]:
                    strains.append(Strain(name=s["name"], reads=s["reads"]))

            pathogen_objects.append(
                PathogenSpecies(
                    name=p["name"], total_reads=p["total_reads"], strains=strains
                )
            )

    # Create an HTML representation using <details> and <summary> tags
    html_content = generate_pathogen_html(pathogen_objects, species_data)
    return {
        "Pathogen Species Distribution": html_content,
        "Strain Distribution": visualize_strain_distribution_per_species(
            pathogen_objects
        ),
    }


def generate_pathogen_html(
    pathogens: List[PathogenSpecies], species_data: List[SpeciesAnnotation]
) -> str:
    """
    Generate HTML content with <details> and <summary> tags for pathogen data.

    Args:
        pathogens: List of PathogenSpecies objects
        species_data: List of SpeciesAnnotation objects with confidence info

    Returns:
        HTML string representation
    """
    # Sort pathogens by total reads (descending)
    pathogens.sort(key=lambda p: p.total_reads, reverse=True)

    html = '<div class="pathogen-container">\n'

    # Add CSS for styling
    html += """
    <style>
        .pathogen-container {
            font-family: Arial, sans-serif;
            max-width: 100%;
        }
        .species-details {
            margin-bottom: 10px;
            border: 1px solid #ddd;
            border-radius: 5px;
        }
        .species-summary {
            display: flex;
            justify-content: space-between;
            padding: 8px 15px;
            background-color: #f0f6ff;
            cursor: pointer;
            font-weight: bold;
        }
        .strain-list {
            padding: 10px 15px 15px 30px;
        }
        .strain-item {
            display: flex;
            justify-content: space-between;
            margin: 5px 0;
            padding: 3px 0;
            border-bottom: 1px solid #eee;
        }
        .confidence-tag {
            font-size: 0.9em;
            font-style: italic;
            color: #555;
        }
        .reads-count {
            font-weight: bold;
            color: #333;
        }
    </style>
    """
    seen = set()
    # For each pathogen species
    for species in species_data:
        # Skip if the species has already been processed
        if species.get_lowest_taxonomy()[1] in seen:
            continue
        seen.add(species.get_lowest_taxonomy()[1])
        name = species.get_lowest_taxonomy()[1]
        pathogen = next((p for p in pathogens if p.name.lower() == name.lower()), None)
        if not pathogen:
            print(f"Species {name} not found in the pathogen data.")
            continue
        confidence = species.confidence_level
        name = pathogen.name
        # Create details element with summary
        html += f'<details class="species-details">\n'
        html += f'<summary class="species-summary">'
        html += f"▼ {name} (Confidence: {confidence})"
        html += f'<span class="reads-count">{pathogen.total_reads} reads</span>'
        html += f"</summary>\n"

        # Add strain information if available
        if pathogen.strains:
            html += f'<div class="strain-list">\n'
            html += f'<details class="species-details">\n'
            html += f'<summary class="species-summary">▼ Strains</summary>\n'
            html += f'<div class="strain-list">\n'

            # Sort strains by read count (descending)
            sorted_strains = sorted(
                pathogen.strains, key=lambda s: s.reads, reverse=True
            )

            # Add each strain as a list item
            for strain in sorted_strains:
                html += f'<div class="strain-item">'
                html += f"<span>• {strain.name}</span>"
                html += f'<span class="reads-count">{strain.reads} reads</span>'
                html += f"</div>\n"

            html += "</div>\n"  # Close strain-list
            html += "</details>\n"  # Close strains details
            html += "</div>\n"  # Close outer strain-list

        html += "</details>\n"  # Close species details

    html += "</div>\n"  # Close pathogen-container

    return html


def visualize_strain_distribution_per_species(pathogens: List[PathogenSpecies]) -> str:
    """
    Create a pie chart visualization of strain distribution within a species.

    Args:
        pathogens: List of PathogenSpecies objects
        file_path: Path to save the HTML file

    Returns:
        HTML string representation
    """
    # Create the parent directory if it doesn't exist

    # Sort pathogens by total reads (descending) to get the most significant first
    pathogens.sort(key=lambda p: p.total_reads, reverse=True)

    # Extract data for the visualization
    labels = []
    values = []

    # Process each strain from all species
    for pathogen in pathogens:
        if pathogen.strains:
            # Sort strains by read count (descending)
            sorted_strains = sorted(
                pathogen.strains, key=lambda s: s.reads, reverse=True
            )

            for strain in sorted_strains:
                # Clean up the strain name if needed
                strain_label = strain.name
                if len(strain_label) > 50:  # Truncate very long names
                    strain_label = strain_label[:47] + "..."

                labels.append(strain_label)
                values.append(strain.reads)

    # Create the pie chart
    fig = go.Figure(
        data=[
            go.Pie(
                labels=labels,
                values=values,
                textinfo="percent",
                textposition="inside",
                hoverinfo="label+percent+value",
                hovertemplate="Strain: %{label}<br>Reads: %{value}<br>Percentage: %{percent}<extra></extra>",
            )
        ]
    )

    # Update layout
    fig.update_layout(
        title_text="Strain Distribution per Species",
        showlegend=False,  # Hide legend for cleaner look with many strains
    )

    # Write to HTML file
    html_content = fig.to_html(full_html=False, include_plotlyjs="cdn")
    return html_content
