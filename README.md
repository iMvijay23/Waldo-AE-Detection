# AE Classification Tool

This tool allows users to classify whether a given text contains an adverse event (AE) using a fine-tuned RoBERTa model. It is designed to be easy to use and can be run directly from the command line.

## Features
- Takes a CSV file with text data as input
- Uses a pre-trained RoBERTa model to classify each text as having an adverse event or not
- Outputs the results in a CSV file with the predicted labels

## Installation
pip install .

### Prerequisites
- Python 3.6 or higher
- `pip` (Python package installer)


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