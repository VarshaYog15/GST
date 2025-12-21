import pandas as pd
import re
import ast

def clean_eq_data(
    input_path="C:/Users/VARSHA/Documents/Python/py_venv/eq_raw.csv",
    output_path="C:/Users/VARSHA/Documents/Python/py_venv/eq_clean.csv"
):

    print("🚀 Cleaning started")

    df = pd.read_csv(input_path)

    # DEBUG (you can remove later)
    print("📌 Columns found:", df.columns.tolist())

    # Convert timestamps FROM USGS column names
    df["time"] = pd.to_datetime(df["properties.time"], unit="ms", errors="coerce")
    df["updated"] = pd.to_datetime(df["properties.updated"], unit="ms", errors="coerce")

    # Extract coordinates
    df["geometry.coordinates"] = df["geometry.coordinates"].apply(
        lambda x: ast.literal_eval(x) if pd.notna(x) else [None, None, None]
    )

    df["longitude"] = df["geometry.coordinates"].apply(lambda x: x[0])
    df["latitude"] = df["geometry.coordinates"].apply(lambda x: x[1])
    df["depth_km"] = df["geometry.coordinates"].apply(lambda x: x[2])
    

    # Convert numeric columns
    numeric_cols = [
        "properties.mag", "properties.nst", "properties.dmin",
        "properties.rms", "properties.gap", "properties.magError",
        "properties.depthError", "properties.magNst", "properties.sig"
    ]

    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # Rename columns to clean names
    df.rename(columns = {"properties.mag": "mag",
        "properties.place": "place",
        "properties.sig": "sig",
        "properties.nst": "nst",
        "properties.dmin": "dmin",
        "properties.rms": "rms",
        "properties.gap": "gap",
        "properties.magType": "magType",
        "properties.type" : "type",
        "properties.status":"status",
        "properties.tsunami" : "tsunami",
        "properties.net" : "net",
        "properties.ids" : "ids",
        "properties.title" : "source",
        "properties.detail" : "magError",
        "properties.alert" : "alert"}, inplace=True)

    # Extract country
    def extract_country(place):
        if pd.isna(place):
            return None
        match = re.search(r",\s*(.*)$", place)
        return match.group(1) if match else place

    df["country"] = df["place"].apply(extract_country)

    df["year"] = df["time"].dt.year
    df["month"] = df["time"].dt.month
    df["day"] = df["time"].dt.day
    df["day_of_week"] = df["time"].dt.day_name()


    # Depth category
    df["depth_category"] = df["depth_km"].apply(
        lambda x: "Shallow (<50 km)" if x < 50 else
                  "Intermediate (50–300 km)" if x <= 300 else
                  "Deep (>300 km)"
    )

    # Magnitude category
    df["magnitude_type"] = df["mag"].apply(
        lambda x: "Strong (>6)" if x >= 6 else
                  "Moderate (4–6)" if x >= 4 else
                  "Light (<4)"
    )

    df.to_csv(output_path, index=False)

    print("Cleaned dataset saved to:", output_path)
    print("Rows:", df.shape[0], "Columns:", df.shape[1])

    return df


if __name__ == "__main__":
    clean_eq_data()
