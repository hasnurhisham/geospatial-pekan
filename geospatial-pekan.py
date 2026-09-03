import streamlit as st
import pandas as pd
import folium
import streamlit.components.v1 as components
import plotly.express as px


# ---------------------------------------------------------
# 1. Page Configuration & Modern CSS Theme
# ---------------------------------------------------------
st.set_page_config(
    page_title="Pekan District Geospatial Vulnerability & Risk Atlas",
    page_icon="🗺️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,600;0,700;1,400&family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
        background-color: #f7f6f2;
        color: #111111;
    }
    .stApp {
        background-color: #f7f6f2;
    }
    .hero-tag {
        font-size: 11px;
        letter-spacing: 2px;
        font-weight: 800;
        color: #1b382b;
        text-transform: uppercase;
        margin-bottom: 2px;
    }
    .hero-title {
        font-family: 'Playfair Display', serif;
        font-size: 46px;
        font-weight: 700;
        line-height: 1.1;
        color: #050505;
        margin-bottom: 8px;
    }
    .hero-sub {
        font-size: 14px;
        font-weight: 500;
        color: #222222;
        margin-bottom: 25px;
    }
    .card-box {
        background-color: #ffffff;
        border-radius: 16px;
        padding: 20px;
        border: 1.5px solid #dcd8cd;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    }
    .legend-box {
        background-color: #eae7df;
        border-radius: 12px;
        padding: 15px;
        margin-top: 15px;
        border: 1px solid #d5d0c3;
    }
    .legend-item {
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-size: 13px;
        font-weight: 600;
        color: #111111;
        margin-bottom: 6px;
    }
    .dot {
        height: 10px;
        width: 10px;
        border-radius: 50%;
        display: inline-block;
        margin-right: 8px;
    }
    label, p, span {
        color: #111111 !important;
        font-weight: 500;
    }

    /* FIX FOR DOWNLOAD BUTTON */
    .stDownloadButton > button {
        background-color: #1b382b !important;
        color: #ffffff !important;
        font-weight: 700 !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        border-radius: 10px !important;
        border: 1px solid #11271d !important;
        padding: 10px 20px !important;
    }
    .stDownloadButton > button:hover {
        background-color: #2a5240 !important;
        color: #ffffff !important;
    }
    </style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# 2. Data Loading & Decision Engine Functions
# ---------------------------------------------------------
@st.cache_data
def load_data():
    return pd.read_excel("Data_PekanPahang.xlsx")

df = load_data()

def get_dynamic_recommendations(filtered_data, selected_severity, selected_factor):
    if selected_severity == "High":
        rec1 = {"title": "1. Immediate Evacuation Readiness", "color": "#b71c1c", "text": "Activate Pusat Pemindahan Sementara (PPS) shelters and issue SMS emergency broadcasts for high-risk zones."}
        rec2 = {"title": "2. Priority Logistics Staging", "color": "#b71c1c", "text": "Deploy rescue boats, emergency rations, and medical teams directly to affected high-density population nodes."}
        rec3 = {"title": "3. 24/7 Command Center Monitoring", "color": "#b71c1c", "text": "Establish a dedicated disaster response task force with live GIS monitoring across high-severity sites."}
    elif selected_severity == "Medium":
        rec1 = {"title": "1. Targeted Drainage Clearing", "color": "#e65100", "text": "Dispatch JPS maintenance units to clear potential culvert blockages before conditions escalate."}
        rec2 = {"title": "2. Community Alert Advisory", "color": "#e65100", "text": "Distribute local flood advisories and ensure community leaders inspect local response kits."}
        rec3 = {"title": "3. Secondary Shelter Pre-check", "color": "#e65100", "text": "Inspect backup relief centers and ensure power generators are fully operational."}
    elif selected_severity == "Low":
        rec1 = {"title": "1. Routine Infrastructure Audit", "color": "#1b382b", "text": "Schedule bi-annual structural safety and drainage capacity audits for low-risk zones."}
        rec2 = {"title": "2. Baseline Environmental Tracking", "color": "#1b382b", "text": "Maintain standard satellite and rain-gauge monitoring across baseline agricultural sites."}
        rec3 = {"title": "3. Long-term Mitigation Planning", "color": "#1b382b", "text": "Incorporate long-term land-use planning guidelines to prevent future risk accumulation."}
    elif selected_factor == "Flood-prone area":
        rec1 = {"title": "1. Canal & Sluice Gate Check", "color": "#b71c1c", "text": "Inspect Pahang River sluice gates and clear primary drainage arteries."}
        rec2 = {"title": "2. Mobile Pump Deployment", "color": "#e65100", "text": "Pre-position high-capacity water pumps at critical low-lying village basins."}
        rec3 = {"title": "3. Retention Basin Management", "color": "#1b382b", "text": "Lower water levels in regional retention ponds to accommodate incoming monsoon surge."}
    elif selected_factor == "Coastal erosion":
        rec1 = {"title": "1. Coastal Revetment Staging", "color": "#b71c1c", "text": "Place temporary rock armoring along active shoreline erosion hotspots."}
        rec2 = {"title": "2. Coastal Buffer Zone Enforcement", "color": "#e65100", "text": "Restrict new heavy infrastructure construction within 100 meters of the high-tide line."}
        rec3 = {"title": "3. Mangrove Restoration Drive", "color": "#1b382b", "text": "Initiate bio-engineering coastal protection using native mangrove replanting."}
    else:
        rec1 = {"title": "1. Multi-Hazard Resource Staging", "color": "#b71c1c", "text": "Pre-position emergency flood relief and medical supplies in High Severity zones with population counts exceeding 400."}
        rec2 = {"title": "2. Infrastructure Upgrades", "color": "#e65100", "text": "Prioritize drainage clearing and coastal bund reinforcement across identified flood-prone and coastal erosion points."}
        rec3 = {"title": "3. Early Warning Deployment", "color": "#1b382b", "text": "Deploy IoT water-level sensors and predictive GIS alert systems across high-density clusters along Pahang River basin."}

    return rec1, rec2, rec3

# ---------------------------------------------------------
# 3. Filter Processing Logic
# ---------------------------------------------------------
all_severities = df["Severity"].unique().tolist()
all_factors = sorted(df["Contributing_Factor"].dropna().unique().tolist())

# Default states
selected_severity = "All severities"
selected_factor = "All factors"

# ---------------------------------------------------------
# 4. Header Section
# ---------------------------------------------------------
col_header_left, col_header_right = st.columns([3, 1])

with col_header_left:
    st.markdown('<p class="hero-tag">PEKAN DISTRICT, PAHANG · GEOSPATIAL RISK MONITORING</p>', unsafe_allow_html=True)
    st.markdown('<h1 class="hero-title">Pekan District Vulnerability & Risk Atlas</h1>', unsafe_allow_html=True)
    st.markdown('<p class="hero-sub">Interactive spatial decision-support platform for hazard assessment and disaster management in Pekan District.</p>', unsafe_allow_html=True)

# ---------------------------------------------------------
# 5. Main Content: Left Filter Panel & Right GIS Map
# ---------------------------------------------------------
col_left, col_right = st.columns([1, 2.8])

with col_left:
    st.markdown("""
    <div style="font-size: 11px; letter-spacing: 1.5px; font-weight:800; color:#111111;">FILTER CONTROLS 🔍</div>
    <h2 style="font-family: 'Playfair Display', serif; font-size: 28px; color:#000000; margin-top:0px;">Spatial Filters</h2>
    """, unsafe_allow_html=True)
    
    search_query = st.text_input("Search Location Name or ID", placeholder="e.g. Kampung Api Larat, H01...")
    selected_severity = st.selectbox("Severity Level", options=["All severities"] + all_severities)
    selected_factor = st.selectbox("Contributing Factor", options=["All factors"] + all_factors)

    # Filter Logic
    filtered_df = df.copy()
    if selected_severity != "All severities":
        filtered_df = filtered_df[filtered_df["Severity"] == selected_severity]
    if selected_factor != "All factors":
        filtered_df = filtered_df[filtered_df["Contributing_Factor"] == selected_factor]
    if search_query.strip():
        q = search_query.strip().lower()
        filtered_df = filtered_df[
            filtered_df["Location Name"].str.lower().str.contains(q, na=False) |
            filtered_df["Hotspot_ID"].str.lower().str.contains(q, na=False) |
            filtered_df["Contributing_Factor"].str.lower().str.contains(q, na=False)
        ]

    # Embedded Legend Box in Filter Column
    st.markdown(f"""
    <div class="legend-box">
        <div style="font-size: 11px; letter-spacing: 1.5px; font-weight:800; color:#111111; margin-bottom: 10px;">SEVERITY CLASSIFICATION</div>
        <div class="legend-item">
            <span><span class="dot" style="background:#b71c1c;"></span> <b>High</b> (≥ 400 pop)</span>
            <b style="color:#000000;">{len(filtered_df[filtered_df['Severity']=='High'])}</b>
        </div>
        <div class="legend-item">
            <span><span class="dot" style="background:#e65100;"></span> <b>Medium</b> (200 – 399 pop)</span>
            <b style="color:#000000;">{len(filtered_df[filtered_df['Severity']=='Medium'])}</b>
        </div>
        <div class="legend-item">
            <span><span class="dot" style="background:#1b5e20;"></span> <b>Low</b> (&lt; 200 pop)</span>
            <b style="color:#000000;">{len(filtered_df[filtered_df['Severity']=='Low'])}</b>
        </div>
        <hr style="margin: 10px 0; border: 0; border-top: 1.5px solid #bbb7a9;">
        <div style="font-size: 12px; font-weight:600; color: #222222;">Thresholds defined by human population exposure scale.</div>
    </div>
    """, unsafe_allow_html=True)

top_filtered_factor = filtered_df['Contributing_Factor'].mode()[0] if not filtered_df.empty else "N/A"

with col_header_right:
    st.markdown(f"""
    <div style="text-align: right; font-size: 13px; color: #111111; padding-top: 20px; font-weight:600;">
        <span style="color:#000000;">{len(filtered_df)} Active Records</span> · WGS 84 Coordinates<br>
        Top Hazard: <b style="color:#000000;">{top_filtered_factor}</b>
    </div>
    """, unsafe_allow_html=True)

# ---------------------------------------------------------
# 6. Dynamic KPI Metric Cards 
# ---------------------------------------------------------
k1, k2, k3, k4 = st.columns(4)

with k1:
    st.markdown(f"""
    <div class="card-box">
        <div style="font-size: 11px; letter-spacing: 1.5px; font-weight:800; color:#222222;">TOTAL HOTSPOTS <span style="float:right; color:#1b5e20;">●</span></div>
        <div style="font-size: 38px; font-weight:800; margin: 8px 0; color:#000000;">{len(filtered_df)}</div>
        <div style="font-size: 12px; font-weight:600; color:#333333;">in current view</div>
    </div>
    """, unsafe_allow_html=True)

with k2:
    st.markdown(f"""
    <div class="card-box">
        <div style="font-size: 11px; letter-spacing: 1.5px; font-weight:800; color:#222222;">AFFECTED POPULATION <span style="float:right; color:#e65100;">●</span></div>
        <div style="font-size: 38px; font-weight:800; margin: 8px 0; color:#000000;">{filtered_df['Affected_Population'].sum():,}</div>
        <div style="font-size: 12px; font-weight:600; color:#333333;">residents represented</div>
    </div>
    """, unsafe_allow_html=True)

with k3:
    high_count = len(filtered_df[filtered_df['Severity'] == 'High'])
    st.markdown(f"""
    <div class="card-box">
        <div style="font-size: 11px; letter-spacing: 1.5px; font-weight:800; color:#222222;">HIGH SEVERITY <span style="float:right; color:#b71c1c;">●</span></div>
        <div style="font-size: 38px; font-weight:800; margin: 8px 0; color:#000000;">{high_count}</div>
        <div style="font-size: 12px; font-weight:600; color:#333333;">priority response zones</div>
    </div>
    """, unsafe_allow_html=True)

with k4:
    st.markdown(f"""
    <div class="card-box">
        <div style="font-size: 11px; letter-spacing: 1.5px; font-weight:800; color:#222222;">TOP RISK FACTOR <span style="float:right; color:#4a148c;">●</span></div>
        <div style="font-size: 20px; font-weight:800; margin: 12px 0; color:#000000;">{top_filtered_factor}</div>
        <div style="font-size: 12px; font-weight:600; color:#333333;">primary hazard factor</div>
    </div>
    """, unsafe_allow_html=True)

st.write("") 

# ---------------------------------------------------------
# 7. Map Rendering
# ---------------------------------------------------------
with col_right:
    st.markdown(f"""
    <div style="display: flex; justify-content: space-between; align-items: center;">
        <div>
            <div style="font-size: 11px; letter-spacing: 1.5px; font-weight:800; color:#111111;">GIS VISUALIZATION</div>
            <h2 style="font-family: 'Playfair Display', serif; font-size: 28px; color:#000000; margin-top:0px;">Interactive Hotspot Map</h2>
        </div>
        <div style="background:#d4edda; border: 1px solid #c3e6cb; padding: 5px 14px; border-radius: 20px; font-size: 12px; color:#155724; font-weight:700;">
            {len(filtered_df)} / {len(df)} Active Hotspots
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    m = folium.Map(location=[3.485, 103.380], zoom_start=11, tiles="OpenStreetMap")
    color_map = {"High": "#b71c1c", "Medium": "#e65100", "Low": "#1b5e20"}

    for _, row in filtered_df.iterrows():
        popup_html = f"""
        <div style="font-family: Arial; font-size: 12px; color:#000000; width: 180px;">
            <b style="font-size:13px;">{row['Location Name']}</b><br>
            <b>ID:</b> {row['Hotspot_ID']}<br>
            <b>Severity:</b> <b style="color:{color_map.get(row['Severity'])};">{row['Severity']}</b><br>
            <b>Affected Pop:</b> {row['Affected_Population']:,}<br>
            <b>Factor:</b> {row['Contributing_Factor']}
        </div>
        """
        folium.CircleMarker(
            location=[row["Latitude"], row["Longitude"]],
            radius=8 if row["Severity"] == "High" else 6,
            color=color_map.get(row["Severity"], "blue"),
            fill=True,
            fill_color=color_map.get(row["Severity"], "blue"),
            fill_opacity=0.85,
            popup=popup_html
        ).add_to(m)

    map_html = m._repr_html_()
    components.html(map_html, height=480, scrolling=False)

# ---------------------------------------------------------
# 8. Detailed Hotspot Register (Data Table)
# ---------------------------------------------------------
def style_severity(val):
    if val == "High":
        return "background-color: #f8d7da; color: #721c24; font-weight: bold;"
    elif val == "Medium":
        return "background-color: #fff3cd; color: #856404; font-weight: bold;"
    elif val == "Low":
        return "background-color: #d4edda; color: #155724; font-weight: bold;"
    return ""

st.markdown("""
<div>
    <div style="font-size: 11px; letter-spacing: 1.5px; font-weight:800; color:#111111;">LOCATION DATA</div>
    <h2 style="font-family: 'Playfair Display', serif; font-size: 28px; color:#000000; margin-top:0px;">Detailed Hotspot Register</h2>
</div>
""", unsafe_allow_html=True)

table_df = filtered_df[["Hotspot_ID", "Location Name", "Severity", "Affected_Population", "Contributing_Factor"]]
styled_df = table_df.style.map(style_severity, subset=["Severity"])

st.dataframe(
    styled_df,
    hide_index=True,
    use_container_width=True,
    height=300
)

# ---------------------------------------------------------
# 9. Bottom Analytics: Bar Chart + Donut Chart
# ---------------------------------------------------------
chart_left, chart_right = st.columns(2)

with chart_left:
    st.markdown("""
    <div style="font-size: 11px; letter-spacing: 1.5px; font-weight:800; color:#111111;">FACTOR ANALYSIS</div>
    <h3 style="font-family: 'Playfair Display', serif; font-size: 22px; color:#000000; margin-top:0px;">Top Contributing Risk Factors</h3>
    """, unsafe_allow_html=True)
    
    factor_counts = filtered_df['Contributing_Factor'].value_counts().head(7).reset_index()
    factor_counts.columns = ['Factor', 'Count']
    
    fig_bar = px.bar(
        factor_counts, 
        x='Count', 
        y='Factor', 
        orientation='h',
        color_discrete_sequence=['#1b382b']
    )
    fig_bar.update_layout(
        margin=dict(l=0, r=0, t=10, b=0),
        height=280,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color="#000000", size=13, family="Plus Jakarta Sans"),
        xaxis=dict(
            showline=True, linecolor="#000000", linewidth=2,
            tickfont=dict(color="#000000", size=12, weight="bold"),
            gridcolor="#dcd8cd"
        ),
        yaxis=dict(
            showline=True, linecolor="#000000", linewidth=2,
            tickfont=dict(color="#000000", size=12, weight="bold"),
            autorange="reversed"
        )
    )
    st.plotly_chart(fig_bar, use_container_width=True)

with chart_right:
    st.markdown("""
    <div style="font-size: 11px; letter-spacing: 1.5px; font-weight:800; color:#111111;">RISK COMPOSITION</div>
    <h3 style="font-family: 'Playfair Display', serif; font-size: 22px; color:#000000; margin-top:0px;">Severity Level Breakdown</h3>
    """, unsafe_allow_html=True)
    
    sev_counts = filtered_df['Severity'].value_counts().reset_index()
    sev_counts.columns = ['Severity', 'Count']
    
    fig_donut = px.pie(
        sev_counts, 
        names='Severity', 
        values='Count', 
        hole=0.6,
        color='Severity',
        color_discrete_map={"High": "#b71c1c", "Medium": "#e65100", "Low": "#1b5e20"}
    )
    fig_donut.update_layout(
        margin=dict(l=0, r=0, t=10, b=0),
        height=280,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color="#000000", size=13, family="Plus Jakarta Sans"),
        legend=dict(
            font=dict(color="#000000", size=12, weight="bold")
        )
    )
    st.plotly_chart(fig_donut, use_container_width=True)

# ---------------------------------------------------------
# 10. Dynamic Executive Action Plan & CSV Export
# ---------------------------------------------------------
st.markdown("---")

rec1, rec2, rec3 = get_dynamic_recommendations(filtered_df, selected_severity, selected_factor)

st.markdown(f"""
<div>
    <div style="font-size: 11px; letter-spacing: 1.5px; font-weight:800; color:#111111;">EXECUTIVE STRATEGY</div>
    <h2 style="font-family: 'Playfair Display', serif; font-size: 28px; color:#000000; margin-top:0px;">
        Action Plan for {selected_severity if selected_severity != 'All severities' else 'Selected'} Risks
    </h2>
</div>
""", unsafe_allow_html=True)

col_r1, col_r2, col_r3 = st.columns(3)

for col, rec in zip([col_r1, col_r2, col_r3], [rec1, rec2, rec3]):
    with col:
        st.markdown(f"""
        <div class="card-box" style="border-left: 5px solid {rec['color']}; min-height: 140px;">
            <h4 style="margin-top:0; color:{rec['color']};">{rec['title']}</h4>
            <p style="font-size:13px; color:#222; margin-bottom:0;">{rec['text']}</p>
        </div>
        """, unsafe_allow_html=True)

st.write("")

csv_data = filtered_df.to_csv(index=False).encode('utf-8')
st.download_button(
    label="📥 Export Filtered Report (CSV)",
    data=csv_data,
    file_name="Pekan_Hotspots_Report.csv",
    mime="text/csv",
)
