import os 
import pandas as pd 
import geopandas as gpd

ARRESTS_PATH = "./data/arrests/arrests_2023.csv"
ACS_PATH = "./data/acs/2023/acs_zip_2023_full.csv"
ZCTA_GEOJSON_PATH = "./data/geo/nyc-zip-code-tabulation-areas.geojson"
OUTPUT_PATH = "./data/merged/merged_arrests_acs_2023.csv"


def merge_arrests_acs(
    arrests_path: str = ARRESTS_PATH,
    acs_path: str = ACS_PATH,
    geojson_path: str = ZCTA_GEOJSON_PATH,
    output_path: str = OUTPUT_PATH,
) -> pd.DataFrame:
    
    print("Loading NYPD arrests data...")
    arrests = pd.read_csv(arrests_path)

    required_cols = {"ARREST_KEY", "Latitude", "Longitude", "LAW_CAT_CD", "PERP_RACE"}
    missing = required_cols - set(arrests.columns)
    if missing:
        raise ValueError(f"Missing required columns in arrests data: {missing}")

    if "JURISDICTION_CODE" in arrests.columns:
        arrests = arrests[arrests["JURISDICTION_CODE"] == 0]

    arrests["Latitude"] = pd.to_numeric(arrests["Latitude"], errors="coerce")
    arrests["Longitude"] = pd.to_numeric(arrests["Longitude"], errors="coerce")
    arrests = arrests.dropna(subset=["Latitude", "Longitude"])
    arrests = arrests[
        (arrests["Latitude"] != 0) & (arrests["Longitude"] != 0)
    ]

    print(f"Remaining arrests with valid coords: {len(arrests):,}")

    print("Converting arrests to GeoDataFrame...")
    arrests_gdf = gpd.GeoDataFrame(
        arrests,
        geometry=gpd.points_from_xy(arrests["Longitude"], arrests["Latitude"]),
        crs="EPSG:4326",
    )

    print("Loading NYC ZCTA GeoJSON...")
    zcta = gpd.read_file(geojson_path)

    if zcta.crs is None:
        zcta.set_crs(epsg=4326, inplace=True)
    else:
        zcta = zcta.to_crs(epsg=4326)

    # Detect ZIP/ZCTA field
    zip_field_candidates = ["ZCTA5CE10", "ZCTA5CE20", "ZCTA", "ZIPCODE", "postalCode", "zipcode"]
    zip_field = next((c for c in zip_field_candidates if c in zcta.columns), None)
    if not zip_field:
        raise ValueError(
            f"Could not find a ZIP/ZCTA column in GeoJSON. "
            f"Looked for: {zip_field_candidates}. Found: {list(zcta.columns)}"
        )

    print("📍 Assigning ZIP (ZCTA) to each arrest via spatial join...")
    arrests_with_zcta = gpd.sjoin(
        arrests_gdf,
        zcta[[zip_field, "geometry"]],
        how="left",
        predicate="within",
    )

    arrests_with_zcta.rename(columns={zip_field: "ZCTA"}, inplace=True)
    arrests_with_zcta = arrests_with_zcta.dropna(subset=["ZCTA"])
    arrests_with_zcta["ZCTA"] = arrests_with_zcta["ZCTA"].astype(str).str.zfill(5)

    print(f"Arrests with ZCTA assigned: {len(arrests_with_zcta):,}")

    print("Aggregating arrests by ZCTA...")

    def count_if(series, value):
        return (series == value).sum()

    agg = (
        arrests_with_zcta.groupby("ZCTA")
        .agg(
            total_arrests=("ARREST_KEY", "count"),
            felonies=("LAW_CAT_CD", lambda x: count_if(x, "F")),
            misdemeanors=("LAW_CAT_CD", lambda x: count_if(x, "M")),
            violations=("LAW_CAT_CD", lambda x: count_if(x, "V")),
        )
        .reset_index()
    )

    race_counts = (
        arrests_with_zcta.groupby(["ZCTA", "PERP_RACE"])
        .size()
        .unstack(fill_value=0)
        .reset_index()
    )

    agg = agg.merge(race_counts, on="ZCTA", how="left")

    print("Loading ACS 2023 ZIP-level demographics...")
    acs = pd.read_csv(acs_path)
    if "ZCTA" not in acs.columns:
        raise ValueError("ACS file must contain 'ZCTA' column.")

    acs["ZCTA"] = acs["ZCTA"].astype(str).str.zfill(5)

    print("Merging arrests and ACS on ZCTA...")
    merged = agg.merge(acs, on="ZCTA", how="left")

    merged["arrest_rate_per_1000"] = (
        merged["total_arrests"] / merged["total_pop"]
    ) * 1000

    race_pop_map = {
        "BLACK": "black_count",
        "WHITE": "white_count",
        "ASIAN / PACIFIC ISLANDER": "asian_count",
        "AMERICAN INDIAN/ALASKAN NATIVE": "native_count",
    }

    if "WHITE HISPANIC" in merged.columns or "BLACK HISPANIC" in merged.columns:
        merged["HISPANIC_ARRESTS"] = (
            merged.get("WHITE HISPANIC", 0) + merged.get("BLACK HISPANIC", 0)
        )

    for perp_col, pop_col in race_pop_map.items():
        if perp_col in merged.columns and pop_col in merged.columns:
            rate_col = (
                perp_col.lower()
                .replace(" / ", "_")
                .replace(" ", "_")
                .replace("__", "_")
                + "_arrest_rate_per_1000"
            )
            merged[rate_col] = (merged[perp_col] / merged[pop_col].replace({0: pd.NA})) * 1000

    if "HISPANIC_ARRESTS" in merged.columns and "hispanic_count" in merged.columns:
        merged["hispanic_arrest_rate_per_1000"] = (
            merged["HISPANIC_ARRESTS"]
            / merged["hispanic_count"].replace({0: pd.NA})
        ) * 1000


    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    merged.to_csv(output_path, index=False)
    print(f"Merged dataset saved to: {output_path}")

    return merged

if __name__ == "__main__":
    df = merge_arrests_acs()
    print("Preview of the merged, clean dataset:")
    print(df.head())