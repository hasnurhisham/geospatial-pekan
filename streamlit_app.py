import streamlit as st
import pandas as pd
import folium
from folium.plugins import MarkerCluster
import streamlit.components.v1 as components

# 1. Page Configuration
st.set_page_config(page_title="Pekan Hotspots Dashboard", layout="wide")

st.title("📍 Pekan District Geospatial Dashboard")
st.caption("Uzma Geospatial AI Technical Assessment")


# 2. Load Dataset
@st.cache_data
def load_data():
    return pd.read_excel("Data_PekanPahang.xlsx")


df = load_data()

# 3. Sidebar Filters
st.sidebar.header("Filter Hotspots")
severity_filter = st.sidebar.multiselect(
    "Select Severity Level:",
    options=df["Severity"].unique(),
    default=df["Severity"].unique()
)

search_query = st.sidebar.text_input("Search Location or Factor:")

# Apply Filters
filtered_df = df[df["Severity"].isin(severity_filter)]
if search_query:
    filtered_df = filtered_df[
        filtered_df["Location Name"].str.contains(search_query, case=False, na=False) |
        filtered_df["Contributing_Factor"].str.contains(search_query, case=False, na=False)
        ]

# 4. Key Metrics Summary
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Hotspots", len(filtered_df))
col2.metric("High Severity", len(filtered_df[filtered_df["Severity"] == "High"]))
col3.metric("Medium Severity", len(filtered_df[filtered_df["Severity"] == "Medium"]))
col4.metric("Total Affected Pop.", f"{filtered_df['Affected_Population'].sum():,}")

st.markdown("---")

# 5. Dashboard Layout: Map + Table
col_map, col_table = st.columns([6, 5])

color_map = {
    "High": "red",
    "Medium": "orange",
    "Low": "green"
}

with col_map:
    st.subheader("Interactive Map")

    m = folium.Map(location=[3.485, 103.380], zoom_start=11, tiles="OpenStreetMap")
    marker_cluster = MarkerCluster().add_to(m)

    for _, row in filtered_df.iterrows():
        popup_html = f"""
        <div style="font-family: Arial; font-size: 12px; width: 180px;">
            <b>{row['Location Name']}</b><br>
            <b>ID:</b> {row['Hotspot_ID']}<br>
            <b>Severity:</b> <span style="color:{color_map.get(row['Severity'])}; font-weight:bold;">{row['Severity']}</span><br>
            <b>Affected Pop:</b> {row['Affected_Population']:,}<br>
            <b>Factor:</b> {row['Contributing_Factor']}
        </div>
        """
        folium.CircleMarker(
            location=[row["Latitude"], row["Longitude"]],
            radius=7,
            color=color_map.get(row["Severity"], "blue"),
            fill=True,
            fill_color=color_map.get(row["Severity"], "blue"),
            fill_opacity=0.85,
            popup=popup_html
        ).add_to(marker_cluster)

    # Render via core HTML component (No JSON errors)
    map_html = m._repr_html_()
    components.html(map_html, height=520, scrolling=False)

with col_table:
    st.subheader("Hotspot Data List")
    st.dataframe(
        filtered_df[["Hotspot_ID", "Location Name", "Severity", "Affected_Population", "Contributing_Factor"]],
        hide_index=True,
        use_container_width=True,
        height=520
    )
