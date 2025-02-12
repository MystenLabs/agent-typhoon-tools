# Sui Agent Hackathon Judging Tools

This repository contains tools for processing and analyzing judge scoring data from the Sui Agent Typhoon Hackathon.

## Overview

The tools in this repository help process judge scoring data and analyze project rankings across multiple judges. It includes:

- Score processing scripts to extract top 40 projects from each judge
- Project frequency analysis across all judges' top 40 lists
- Repository validation and cloning tools for project submissions

## Components

### Score Processing (`process_submission_screening_scores.py`)

Python script that:
- Parses judge scoring CSV files from `data-judges` directory
- Extracts top 40 ranked projects for each judge
- Generates individual judge top 40 lists
- Creates a consolidated frequency report showing how often each project appears across judges' lists

### Public GitHub Check (`check_and_download_repos.sh`)

Bash script that:
- Validates project repository URLs from `repos.txt`
- Identifies and logs private repositories
- Clones public repositories for review

## Utilities

### Project Frequency Report

1. Place judge scoring CSV files in `data-judges` directory
2. Run score processing:

```bash
python process_submission_screening_scores.py
```

### Repository Validation and Cloning

1. Place project repository URLs in `repos.txt`
2. Run repository validation and cloning:

```bash
bash check_and_download_repos.sh
```

