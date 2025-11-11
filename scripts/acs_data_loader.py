from dotenv import load_dotenv
import requests 
import pandas as pd
import os 

load_dotenv()

CENSUS_API_KEY = os.getenv("CENSUS_API_KEY")

if not CENSUS_API_KEY:
    raise ValueError("CENSUS_API_KEY not found in environment variables.")

api = "https://api.census.gov/data/2023/acs/acs5"

variables = [
    # Population + Race/Ethnicity
    "B03002_001E",  # Total population
    "B03002_003E",  # White alone
    "B03002_004E",  # Black or African American alone
    "B03002_005E",  # American Indian and Alaska Native alone
    "B03002_006E",  # Asian alone
    "B03002_012E",  # Hispanic or Latino (any race)
    # Socioeconomic variables
    "B19013_001E",  # Median household income
    "B17001_002E"   # Below poverty level
]

url = (
    f"{api}?get=NAME,{','.join(variables)}"
    f"&for=zip%20code%20tabulation%20area:*"
    f"&key={CENSUS_API_KEY}"
)
print("Fetching ACS 2023 ZIP-level demographics for NY only (selected demographic variables):")
response = requests.get(url)
response.raise_for_status()

acs = response.json()
acs = pd.DataFrame(acs[1:], columns=acs[0])

for col in variables:
    acs[col] = pd.to_numeric(acs[col], errors="coerce")

acs.rename(columns={
    "B03002_001E": "total_pop",
    "B03002_003E": "white_count",
    "B03002_004E": "black_count",
    "B03002_005E": "native_count",
    "B03002_006E": "asian_count",
    "B03002_012E": "hispanic_count",
    "B19013_001E": "median_income",
    "B17001_002E": "below_poverty",
    "zip code tabulation area": "ZCTA"
}, inplace=True)

acs["pct_white"] = acs["white_count"] / acs["total_pop"]
acs["pct_black"] = acs["black_count"] / acs["total_pop"]
acs["pct_native"] = acs["native_count"] / acs["total_pop"]
acs["pct_asian"] = acs["asian_count"] / acs["total_pop"]
acs["pct_hispanic"] = acs["hispanic_count"] / acs["total_pop"]


acs_clean = acs[[
    "ZCTA",
    # Population counts
    "total_pop", "white_count", "black_count",
    "native_count", "asian_count", "hispanic_count",
    # SES metrics
    "median_income", "below_poverty",
    # Computed proportions
    "pct_white", "pct_black", "pct_native",
    "pct_asian", "pct_hispanic"
]]

os.makedirs("../data/acs/2023", exist_ok=True)
save_path = "../data/acs/2023/acs_zip_2023_full.csv"
acs_clean.to_csv(save_path, index=False)

print(f"Saved ACS 2023 ZIP-level data (with raw counts) → {save_path}")