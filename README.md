# Mapping Structural Disparities in NYC Policing

This repository contains the data and code for an empirical investigation of racial and socioeconomic disparities in NYPD arrest patterns in 2023.

We focus on the question:

> How do racial composition, income, and poverty predict arrest intensity across New York City ZIP Code Tabulation Areas (ZCTAs), after accounting for population size?

The project situates this empirical question within broader concerns in data ethics, algorithmic fairness, and the risks of bias propagation in data-driven policing.

---

## Ethical Themes

- **Fairness**  
  Are arrests proportional to the demographic composition of communities, or are some racial groups and neighborhoods systematically subject to higher enforcement intensity?

- **Responsibility**  
  How should researchers and practitioners interpret “open” policing data without naturalizing, sanitizing, or amplifying existing harms?

- **Privacy**  
  Why use aggregated, area-level data (ZIP/ZCTA) instead of identifying individuals, officers, or exact addresses, and how does this choice balance analytic value with protection against re-identification?

- **Bias Propagation**  
  How can biased or uneven arrest data, if used uncritically as training data for predictive systems, reproduce and legitimize structural inequalities in policing? How do such systems participate in feedback loops where past enforcement shapes future patrol allocation?

---

## Hypothesis

We hypothesize that, even after normalizing by population and controlling for basic contextual factors, ZIP codes with higher proportions of Black and Hispanic residents and greater socioeconomic disadvantage will exhibit higher arrest intensities than whiter, wealthier ZIP codes. We further expect these disparities to be large enough to raise concerns about disparate impact and about the use of arrest data as “objective” inputs in predictive policing tools.

---

## Methodology (High-Level)

1. **Data sources**
   - **NYPD Arrest Data (Historic)** from NYC Open Data, restricted to **calendar year 2023**.
   - **American Community Survey (ACS) 2019–2023 5-year estimates**, at the ZIP Code Tabulation Area (ZCTA) level, including:
     - Total population  
     - Racial/ethnic composition (White, Black, Hispanic/Latino, Asian, American Indian/Alaska Native)  
     - Median household income  
     - Poverty counts and rates
   - **Census ZCTA shapefiles** for New York City to enable mapping and spatial analysis.

2. **Geospatial linkage**
   - Each arrest is geocoded using NYPD-provided latitude/longitude.
   - Arrest locations are spatially joined to NYC ZIP/ZCTA polygons (GeoJSON).
   - We retain ZCTAs with sufficient residential population and valid ACS coverage to obtain stable per-capita rates.

3. **Construction of arrest intensity measures**
   - For each ZCTA we compute:
     - **Arrest intensity**: total arrests per 1,000 residents.
     - Counts of felonies, misdemeanors, and violations.
   - We merge these with ACS demographics to obtain a single 2023 ZIP-level analysis dataset (`data/merged/merged_arrests_acs_2023.csv`).

4. **Exploratory & descriptive analysis**
   - Citywide descriptive statistics for arrests and population, disaggregated by race.
   - Identification of **highest- and lowest-intensity ZIP codes** and their demographic profiles.
   - Correlation matrix relating arrest intensity, racial composition, and socioeconomic indicators.
   - Scatterplots (e.g., arrest intensity vs. median income, % Black, % Hispanic).

5. **Regression modeling (OLS)**
   - Three cross-sectional OLS models with **arrests per 1,000 residents** as the outcome:
     1. **Race-only model**: percent Black, percent Hispanic.
     2. **Race + SES model**: adds median income and poverty rate.
     3. **Full model**: adds log population to capture differences in ZIP-code size.
   - Models are used to assess whether racial disparities in arrest intensity persist after adjusting for income, poverty, and population size, and to quantify effect sizes.

6. **Unsupervised clustering of “neighborhood types”**
   - Standardize selected variables (arrest intensity, % Black, % Hispanic, median income, poverty).
   - Fit k-means models for varying values of k; choose **k = 4** based on the elbow plot.
   - Interpret resulting clusters as **neighborhood profiles** (e.g., Hispanic-Majority / High Arrest, White-Affluent / Low Arrest) and map their spatial distribution.

7. **Geospatial analysis**
   - Choropleth maps of:
     - Arrest intensity (per 1,000 residents).
     - Key demographic and socioeconomic indicators (e.g., poverty).
   - **Spatial smoothing** using queen contiguity weights and spatial lags to highlight regional clustering.
   - **Z-score standardization** of arrest intensity to identify ZIP codes with exceptionally high or low enforcement relative to the citywide mean.

8. **Normative / fairness interpretation**
   - Synthesis of descriptive, regression, clustering, and spatial results.
   - Interpretation in terms of **structural bias**, feedback loops in predictive policing, and the ethical risks of treating arrest data as neutral evidence of crime.

---

## Repository Contents

```bash
├── data
│   ├── acs
│   ├── arrests
│   ├── geo
│   ├── merged
│   └── prev
├── docs
├── environment.yml
├── exploration
├── notebooks
├── outputs
├── README.md
└── scripts
```

## Local Setup 

### Prerequisites

- Conda (Anaconda or Miniconda)
- Git (optional but recommended)

```bash
# Clone this repository
git clone git@github.com:giomhern/project-ariel-ruhaan-gio.git
cd project-ariel-ruhaan-gio

# Create and activate the environment
conda env create -f environment.yml
conda activate data-ethics
```

## Reproducing the Analysis

1. Run exploratory and modeling notebooks. Launch Jupyter:

```bash
jupyter lab
```

2. Then open and run:
  
- notebooks/01_exploratory_modeling_analysis.ipynb
- notebooks/02_spatial_analysis.ipynb
- notebooks/03_spatial_analysis.ipynb
- 
These notebooks regenerate the summary statistics, OLS models, clustering results, and spatial figures saved under outputs/.

## Citation / Acknowledgment

If you use or adapt this repository, please acknowledge:

- NYPD Arrest Data (NYC Open Data)
- U.S. Census Bureau ACS 5-year estimates and ZCTA shapefiles
- The course DATA 259: Ethics, Fairness, Responsibility, and Privacy in Data Science (University of Chicago)

and credit the project authors:

- Giovanni Maya
- Ariel Alleyne
- Ruhaan Chopra