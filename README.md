# Mapping Structural Disparities in NYC Policing

This repository contains the data and code for an empirical investigation of racial and socioeconomic disparities in NYPD arrest patterns.

We focus on the question:

> Given comparable time periods, do ZIP Code Tabulation Areas (ZCTAs) in New York City with different racial and socioeconomic compositions experience differing arrest intensities?

The project situates this empirical question within broader concerns in data ethics, algorithmic fairness, and the risks of bias propagation in data-driven policing.

## Ethical Themes

- Fairness  
  Are arrests proportional to the demographic composition of communities, or are some groups and neighborhoods systematically subject to higher enforcement intensity?

- Responsibility  
  How should researchers and practitioners interpret open policing data without naturalizing or amplifying existing harms?

- Privacy  
  Why use aggregated, area-level data (ZIP/ZCTA) instead of identifying individuals, officers, or exact locations, and how does this choice balance analytic value with protection against re-identification?

- Bias Propagation  
  How can biased or uneven arrest data, if used uncritically as training data for predictive systems, reproduce and legitimize structural inequalities in policing?

## Hypothesis

We hypothesize that, even after normalizing by population and controlling for basic contextual factors, ZIP codes with higher proportions of Black and Hispanic residents and greater socioeconomic disadvantage will exhibit higher arrest intensities than whiter, wealthier ZIP codes. We further expect these disparities to be large enough to raise concerns about disparate impact and the use of arrest data in predictive policing tools.

## Methodology

1. Data sources
   - NYPD Arrests Data (NYC Open Data), restricted to 2023.
   - U.S. Census Bureau ACS 2023 5-year estimates at the ZIP Code Tabulation Area (ZCTA) level for:
     - Total population
     - Racial and ethnic composition (White, Black, Hispanic/Latino, Asian, American Indian/Alaska Native)
     - Median household income
     - Poverty measures

2. Geospatial linkage
   - Each arrest record is geocoded using its latitude and longitude.
   - Arrest locations are spatially joined to NYC ZIP/ZCTA polygons (GeoJSON).
   - We retain ZCTAs with sufficient residential population to obtain stable rates.

3. Construction of arrest intensity measures
   - For each ZCTA, we compute:
     - Total arrests per 1,000 residents.
     - Offense severity breakdowns (felony, misdemeanor, violation).
     - Group-specific arrest intensities where both ACS population counts and arrest counts are available.
   - We merge these with ACS demographics to obtain a ZIP-level analysis dataset.

4. Exploratory analysis
   - Descriptive statistics and visualization of arrest intensity across ZIP codes.
   - Correlation analysis between arrest intensity, racial composition, and socioeconomic indicators.
   - Examination of how high- and low-intensity ZIP codes differ in demographic and economic profiles.

5. Regression modeling
   - Ordinary Least Squares (OLS) models with arrest intensity as the outcome and:
     - Racial composition (percent Black, Hispanic, etc.)
     - Socioeconomic context (income, poverty)
     - Population size (log population) as controls.
   - Poisson regression with total arrests as a count outcome and population as an offset, to model arrest rates directly.
   - These models assess whether racial and economic disparities in arrest intensity persist after adjusting for basic contextual factors.

6. Fairness analysis
   - Citywide group-specific arrest rates (e.g., Black vs White vs Hispanic) and corresponding rate ratios.
   - ZIP-level Black-to-White and Hispanic-to-White arrest intensity ratios where denominators are reliable.
   - Interpretation of these disparities using fairness concepts such as disparate impact and structural bias.

## Repository Contents

```bash 
├── data
│   ├── acs
│   ├── arrests
│   ├── geo
│   ├── merged
│   └── prev
├── environment.yml
├── exploration
│   ├── chloro.ipynb
│   ├── explo.ipynb
│   ├── exploration.ipynb
│   └── Project_DATA259 (1).ipynb
├── notebooks
│   └── analysis_2023.ipynb
├── README.md
└── scripts
    ├── acs_data_loader.py
    └── merge_arrests_acs.py
```

- `data/`  
  Processed CSV files, including:
  - Raw NYPD 2023 arrests extract
  - ACS 2023 ZIP-level demographic data
  - Merged and cleaned ZIP-level analysis dataset

- `scripts/`  
  Reproducible steps for:
  - Downloading and preparing ACS data
  - Spatially joining arrests to ZCTAs
  - Constructing arrest intensity and merged datasets

- `notebooks/` 
  Jupyter notebooks containing:
  - Exploratory analysis
  - Regression modeling
  - Fairness and disparity analysis

- `environment.yml`  
  Conda environment specification for reproducing the analysis.

## Local Setup

Prerequisites:
- Conda (Anaconda or Miniconda)

Setup:

```bash
conda env create -f environment.yml
conda activate data-ethics
```