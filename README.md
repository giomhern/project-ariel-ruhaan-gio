# Investigating Demographic Disparities in NYC Arrest Data

This repository contains the `data` and `scripts` for an investigation on demographic disparities in NYC Arrest data. More specifically, this repository and corresponding report aim at tackling our research question:

> Controlling for offense type and time, how do arrest rates differ across NYC precincts with varying racial compositions?

in a lens of ethics, fairness, and bias. This research question is derived from the larger, broader question:

> Given similar offense types and time periods, do precincts and communities experience different arrest rates? 


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
