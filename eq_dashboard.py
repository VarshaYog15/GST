import streamlit as st
import pandas as pd

# =====================================================
# Load Data
# =====================================================
@st.cache_data
def load_data():
    return pd.read_csv("C:/Users/VARSHA/Documents/Python/py_venv/eq_clean.csv")

df = load_data()

# =====================================================
# Column Detection (Safe)
# =====================================================
# Magnitude
if "properties.mag" in df.columns:
    MAG_COL = "properties.mag"
elif "mag" in df.columns:
    MAG_COL = "mag"
else:
    st.error("❌ Magnitude column not found")
    st.stop()

# Latitude / Longitude
LAT_COL = "latitude" if "latitude" in df.columns else None
LON_COL = "longitude" if "longitude" in df.columns else None

# =====================================================
# Sidebar Navigation
# =====================================================
st.sidebar.title("📂 Analysis Menu")

menu = st.sidebar.radio(
    "Choose Analysis",
    [
        "Overview",
        "Alerts",
        "Geography",
        "Time Analysis",
        "Advanced Insights",
        "Raw Data"
    ]
)

# =====================================================
# Global Filters
# =====================================================
st.sidebar.subheader("🔍 Filters")
min_mag = st.sidebar.slider("Minimum Magnitude", 0.0, 9.0, 4.0)

filtered_df = df[df[MAG_COL] >= min_mag]

# =====================================================
# Title
# =====================================================
st.title("🌍 Global Seismic Trends Dashboard")
st.write("Interactive analysis of global earthquake activity")

# =====================================================
# QUERY FUNCTIONS (≈30)
# =====================================================
# ---------- Overview ----------
def total_earthquakes(df): return len(df)
def avg_magnitude(df): return round(df[MAG_COL].mean(), 2)
def max_magnitude(df): return df[MAG_COL].max()
def earthquakes_by_year(df): return df["year"].value_counts().sort_index()
def top_countries(df): return df["country"].value_counts().head(10)

# ---------- Alerts ----------
def strong_eq(df): return df[df[MAG_COL] >= 6]
def shallow_eq(df): return df[df["depth_km"] < 50]
def high_sig_eq(df): return df[df.get("properties.sig", 0) >= 600]
def critical_eq(df): return df[(df[MAG_COL] >= 6) & (df["depth_km"] < 50)]
def recent_eq(df): return df.sort_values("time", ascending=False).head(20)
def alert_by_country(df): return critical_eq(df)["country"].value_counts()

# ---------- Geography ----------
def eq_by_country(df): return df["country"].value_counts()
def top_active_regions(df): return df.groupby("country").size().sort_values(ascending=False).head(10)
def depth_vs_mag(df): return df[[MAG_COL, "depth_km"]]

# ---------- Time ----------
def yearly_trend(df): return df.groupby("year").size()
def monthly_trend(df): return df.groupby("month").size()
def weekday_trend(df): return df["day_of_week"].value_counts()
def recent_30_days(df):
    cutoff = pd.Timestamp.now() - pd.Timedelta(days=30)
    return df[df["time"] >= cutoff]

# ---------- Advanced ----------
def depth_category_dist(df): return df["depth_category"].value_counts()
def magnitude_type_dist(df): return df["magnitude_type"].value_counts()
def strongest_countries(df): return df.groupby("country")[MAG_COL].max().sort_values(ascending=False).head(5)
def alert_levels(df): return df.get("alert_level", pd.Series()).value_counts()
def rare_locations(df):
    counts = df["country"].value_counts()
    return counts[counts == 1]

# =====================================================
# PAGE RENDERING
# =====================================================
# ---------- Overview ----------
if menu == "Overview":
    st.header("Overview")

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Earthquakes", total_earthquakes(filtered_df))
    col2.metric("Average Magnitude", avg_magnitude(filtered_df))
    col3.metric("Maximum Magnitude", max_magnitude(filtered_df))

    st.subheader("Earthquakes per Year")
    st.bar_chart(earthquakes_by_year(filtered_df))

    st.subheader("Top 10 Countries")
    st.dataframe(top_countries(filtered_df))

# ---------- Alerts ----------
elif menu == "Alerts":
    st.header("Seismic Alerts")

    col1, col2, col3 = st.columns(3)
    col1.metric("Strong (≥6)", len(strong_eq(filtered_df)))
    col2.metric("Shallow (<50km)", len(shallow_eq(filtered_df)))
    col3.metric("Critical", len(critical_eq(filtered_df)))

    st.subheader("Critical Earthquakes")
    st.dataframe(critical_eq(filtered_df)[
        ["time", "country", MAG_COL, "depth_km"]
    ])

# ---------- Geography ----------
elif menu == "Geography":
    st.header("Geographic Analysis")

    st.subheader("Top Active Regions")
    st.bar_chart(top_active_regions(filtered_df))

    if LAT_COL and LON_COL:
        st.subheader("Earthquake Map")
        st.map(
            filtered_df[[LAT_COL, LON_COL]]
            .rename(columns={LAT_COL: "lat", LON_COL: "lon"})
            .dropna()
        )

# ---------- Time Analysis ----------
elif menu == "Time Analysis":
    st.header("Time Analysis")

    st.subheader("Yearly Trend")
    st.line_chart(yearly_trend(filtered_df))

    st.subheader("Day of Week Distribution")
    st.bar_chart(weekday_trend(filtered_df))

    st.subheader("Last 30 Days Activity")
    st.dataframe(recent_30_days(filtered_df)[
        ["time", "country", MAG_COL, "depth_km"]
    ])

# ---------- Advanced Insights ----------
elif menu == "Advanced Insights":
    st.header("Advanced Insights")

    st.subheader("Depth Categories")
    st.bar_chart(depth_category_dist(filtered_df))

    st.subheader("Magnitude Types")
    st.bar_chart(magnitude_type_dist(filtered_df))

    st.subheader("Strongest Countries")
    st.dataframe(strongest_countries(filtered_df))

# ---------- Raw Data ----------
elif menu == "Raw Data":
    st.header("Raw Data")
    st.dataframe(filtered_df)
