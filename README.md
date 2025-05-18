# Pathogen Analysis Dashboard

A script to visualizing pathogen data from raw text files:

- Antimicrobial resistance (AMR) annotations: AMR_annotation.txt
- Pathogen mapping data: Pathogen_map.txt
- Species annotations: Species_annotation.txt
- Viral taxonomic classifications: structured_viral_summary.tsv

The script generates interactive visualizations to provide insights into the pathogen composition and characteristics of samples.

## Features

- **Data Parsing**: Process raw output files from bioinformatics pipelines
- **Interactive Visualizations**: Generate Plotly-based charts, graphs, and tables
- **Consolidated Report**: Combine all visualizations into a comprehensive HTML report


## Visualizations

The dashboard includes multiple visualization types:
- Bar charts for pathogen species and AMR classes
- Sunburst diagrams for taxonomic relationships
- Scatter plots for similarity metrics
- Pie charts for confidence distributions
- Tree maps for viral taxonomy

## Installation

This project requires Python 3 and the following packages:
```
pip install plotly pandas
```

## Usage

To generate a complete report with all visualizations:

```python
python main.py
open report.html
```

The script will process the following data files from the `data/` directory:
- `Pathogen_map.txt` via `parse_pathogen_map.py` and `visualize_pathogen_map.py`
- `Species_annotation.txt` via `parse_species_annotation.py` and `visualize_species_annotation.py`
- `AMR_annotation.txt` via `parse_amr_annotation.py` and `visualize_pathogen_map.py`
- `structured_viral_summary.tsv` via `parse_structured_viral_summary.py` and `visualize_structured_viral_summary.py`

Output will be saved as:
- `report.html` - Main consolidated report

