# AE Classification Tool

This tool classifies whether a given text contains an adverse event (AE) using a fine-tuned RoBERTa model.

## Installation
pip install .

## Usage
ae-classifier --input path/to/input.csv --output path/to/output.csv

### Input File Format
The input file should be a CSV with the following columns:
- `id`: Unique identifier for each comment
- `comment`: The text to be classified

### Output File Format
The output file will contain:
- `id`: The original ID
- `comment`: The original comment
- `ae_label`: 'yes' or 'no' indicating the presence of an AE