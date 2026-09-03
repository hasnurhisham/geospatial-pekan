# Pekan District Vulnerability & Risk Atlas

An interactive spatial decision-support platform designed for hazard assessment, exposure modeling, and disaster management across Pekan District, Pahang.

---

## 🌟 Key Features

* **Interactive GIS Map**: WGS 84 spatial coordinates visualizer featuring dynamic zoom controls and population-weighted hotspot tracking.
* **Severity Exposure Modeling**: Standardized risk classification built on population exposure thresholds:
  * 🔴 **High Severity**: $\ge 400$ affected residents
  * 🟠 **Medium Severity**: $200\text{--}399$ affected residents
  * 🟢 **Low Severity**: $< 200$ affected residents
* **Custom Marker Clustering**: Optimized spatial aggregation using neutral, executive badge clusters (`disableClusteringAtZoom=13`) to prevent visual clutter while preserving pin color integrity upon zoom.
* **Dynamic Executive Action Plan**: Adaptive decision-support cards that generate tailored, factor-specific operational recommendations for local authorities (e.g., JPS drainage checks, coastal revetments).
* **Data Register & Analytics**: Interactive Pandas-styled hotspot table with conditional severity highlighting, distribution charts, and a one-click CSV report generator.

---

## 🛠️ Tech Stack & Requirements

* **Language**: Python 3.9+
* **Framework**: Streamlit
* **Geospatial & Visualization**: Folium, Plotly Express
* **Data Engine**: Pandas, OpenPyXL

---

## 🚀 Quick Start (Local Setup)

1. **Clone or Download** this repository to your local machine.

2. **Install Required Dependencies**:
   ```bash
   pip install -r requirements.txt
3. **Launch the application**:
  ```bash
   streamlit run app.py 
4. **Access the Interface**:
   Open your browser and navigate to http://localhost:8501.
