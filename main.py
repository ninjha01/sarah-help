#!/usr/bin/env python3
import datetime
from pathlib import Path

# Import all parsing modules
from parse_structured_viral_summary import parse_viral_summary
from parse_species_annotation import parse_species_annotation
from parse_pathogen_map import parse_pathogen_map
from parse_amr_annotation import parse_amr_annotation

# Import all visualization modules
from visualize_structured_viral_summary import visualize_viral_summary
from visualize_species_annotation import visualize_species_annotation
from visualize_pathogen_map import (
    visualize_pathogen_map,
)
from visualize_amr_annotation import visualize_amr_annotation


def generate_report(
    viral_summary_path: str,
    species_annotation_path: str,
    pathogen_map_path: str,
    amr_annotation_path: str,
    output_path: str = "report.html",
):
    """
    Generate a comprehensive HTML report that combines all visualizations.
    """
    # Parse all data first and verify we have results
    print("Parsing data files...")

    # Parse and verify viral summary data
    viral_data = parse_viral_summary(viral_summary_path)
    assert (
        viral_data
    ), f"No data returned from parsing viral summary file: {viral_summary_path}"

    # Parse and verify species annotation data
    species_data = parse_species_annotation(species_annotation_path)
    assert (
        species_data
    ), f"No data returned from parsing species annotation file: {species_annotation_path}"

    # Parse and verify pathogen map data
    pathogen_data = parse_pathogen_map(pathogen_map_path)
    assert (
        pathogen_data
    ), f"No data returned from parsing pathogen map file: {pathogen_map_path}"

    # Parse and verify AMR annotation data
    amr_data = parse_amr_annotation(amr_annotation_path)
    assert (
        amr_data
    ), f"No data returned from parsing AMR annotation file: {amr_annotation_path}"

    # Generate all visualizations
    print("Generating visualizations...")

    identified_species_vis = visualize_pathogen_map(pathogen_data, species_data)
    species_annotation_vis = visualize_species_annotation(species_data)
    viral_summary_vis = visualize_viral_summary(viral_data)

    amr_annotation_vis = visualize_amr_annotation(amr_data)

    # Create the HTML report
    print("Generating final report...")

    # Current date and time
    current_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Collect all visualizations as HTML strings
    all_visualizations = {
        "Pathogen Map": identified_species_vis,
        "Species Annotation": species_annotation_vis,
        "AMR Annotation": amr_annotation_vis,
        "Viral Summary": viral_summary_vis,
    }

    # Create the HTML report with improved styling
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Pathogen Analysis Report</title>
        <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
        <style>
            /* Base styles */
            :root {{
                --primary-color: #2c3e50;
                --secondary-color: #3498db;
                --accent-color: #e74c3c;
                --background-color: #f8f9fa;
                --text-color: #333;
                --border-color: #ddd;
                --section-bg: #fff;
                --header-bg: #f1f8ff;
            }}
            
            * {{
                box-sizing: border-box;
                margin: 0;
                padding: 0;
            }}
            
            body {{
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Oxygen, Ubuntu, Cantarell, "Open Sans", "Helvetica Neue", sans-serif;
                line-height: 1.6;
                color: var(--text-color);
                background-color: var(--background-color);
                padding: 0;
                margin: 0;
            }}
            
            /* Header styles */
            header {{
                background-color: var(--header-bg);
                padding: 2rem;
                border-bottom: 1px solid var(--border-color);
                text-align: center;
                margin-bottom: 2rem;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
            }}
            
            header h1 {{
                color: var(--primary-color);
                font-size: 2.5rem;
                margin-bottom: 0.5rem;
            }}
            
            .date {{
                color: #666;
                font-size: 0.9rem;
                font-style: italic;
            }}
            
            /* Main content */
            main {{
                max-width: 1200px;
                margin: 0 auto;
                padding: 0 2rem 3rem;
            }}
            
            h2 {{
                color: var(--primary-color);
                margin: 2.5rem 0 1rem;
                padding-bottom: 0.5rem;
                border-bottom: 2px solid var(--secondary-color);
                font-size: 1.8rem;
            }}
            
            h3 {{
                color: var(--secondary-color);
                margin: 1.5rem 0 1rem;
                font-size: 1.4rem;
            }}
            
            p {{
                margin-bottom: 1.5rem;
                color: #555;
            }}
            
            /* Visualization containers */
            .visualization {{
                background-color: var(--section-bg);
                border-radius: 8px;
                box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
                padding: 1.5rem;
                margin-bottom: 2rem;
                overflow: hidden;
                border: 1px solid var(--border-color);
            }}
            
            /* Footer styles */
            footer {{
                text-align: center;
                padding: 2rem;
                background-color: var(--primary-color);
                color: white;
                font-size: 0.9rem;
                margin-top: 3rem;
            }}
            
            /* Responsive adjustments */
            @media (max-width: 768px) {{
                header {{
                    padding: 1.5rem;
                }}
                
                main {{
                    padding: 0 1rem 2rem;
                }}
                
                h2 {{
                    font-size: 1.5rem;
                }}
                
                .visualization {{
                    padding: 1rem;
                }}
            }}
        </style>
    </head>
    <body>
        <header>
            <h1>Pathogen Analysis Report</h1>
            <div class="date">Generated on {current_date}</div>
        </header>
        
        <main>
    """

    # Add section for each category
    for category, vis_content in all_visualizations.items():
        html_content += f"""
            <h2>{category}</h2>
            <p>Analysis results from {category.lower()} data.</p>
        """

        # Add the HTML content directly
        for title, content in vis_content.items():
            html_content += f"""
            <div class="visualization">
                <h3>{title}</h3>
                {content}
            </div>
            """

    # Close the HTML document
    html_content += """
        </main>
        <footer>
        </footer>
    </body>
    </html>
    """

    # Write the report to a file
    with open(output_path, "w") as f:
        f.write(html_content)

    print(f"Report successfully generated: {output_path}")
    return output_path


if __name__ == "__main__":
    # File paths to read
    viral_summary_path = (
        "/Users/nishantjha/Desktop/sarah/data/structured_viral_summary.tsv"
    )
    species_annotation_path = (
        "/Users/nishantjha/Desktop/sarah/data/Species_annotation.txt"
    )
    pathogen_map_path = "/Users/nishantjha/Desktop/sarah/data/Pathogen_map.txt"
    amr_annotation_path = "/Users/nishantjha/Desktop/sarah/data/AMR_annotation.txt"

    # Generate the report
    report_path = generate_report(
        viral_summary_path,
        species_annotation_path,
        pathogen_map_path,
        amr_annotation_path,
        "report.html",
    )
