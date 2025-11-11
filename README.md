# Mapping Structural Disparities in NYC Policing

This repository contains the `data` and `scripts` for an investigation on demographic disparities in NYC Arrest data. More specifically, this repository and corresponding report aim at tackling our research question:

> “Given comparable offense types and time periods, do ZIP-code areas in New York City with different racial and socioeconomic compositions experience differing arrest intensities?"


Ethical Themes:

- Fairness: Are arrests proportionate to community demographics?
- Responsibility: How should analysts interpret open policing data without reproducing harm?
- Privacy: Why aggregate at ZIP level instead of individuals or officers?
- Bias Propagation: How biased data can affect predictive policing models.


Hypothesis:

ZIP codes with higher proportions of Black and LatinX residents will show higher arrest intensities, even when controlling for offense type, income, and borough.

## Methodology

This project examines how police arrest rates differ across New York City precincts with varying racial compositions, while controlling for offense type and time period.

We use public data from **NYC Open Data** and the **U.S. Census**, including NYPD Arrest Data, Complaint Data, and demographic information. 

Our analysis includes:
- **Exploratory data visualization** to identify disparities across precincts.  
- **Regression modeling** to test whether precincts with higher proportions of Black or Hispanic residents show higher arrest intensities after accounting for crime rates.  
- **Geospatial mapping** and an **interactive dashboard** (Streamlit) to display results clearly.

## Directory Structure

The directory structure follows the traditional data science prototyping structure. A file tree is shown below for your convenience.

```bash
├── data
│   └── arrests_2023.csv
├── README.md
├── requirements.txt
└── scripts
```

- `data`: all the relevant data in `csv` format 
- `scripts`: pertinent files for analysis
- `requirements.txt`: project dependencies


## Local Setup

**Note**: Make sure conda is installed on your machine.

Run the following commands to ensure all files work as expected, by replicated our own environment:

```bash
conda env create -f environment.yml
conda activate data-ethics
```