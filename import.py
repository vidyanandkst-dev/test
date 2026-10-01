import io
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Cabinet Dimension Calculator", layout="centered")
st.title("Cabinet Dimension and Area Calculator")

# --- Inputs Section ---
st.header("1. Input Dimensions")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Internal Chamber (cm)")
    c3 = st.number_input("Cabinet Width W", min_value=0.0, value=61.0, step=0.1)
    c4 = st.number_input("Cabinet Depth D", min_value=0.0, value=52.9, step=0.1)
    c5 = st.number_input("Cabinet Height H", min_value=0.0, value=130.0, step=0.1)

with col2:
    st.subheader("Insulation Addition (cm)")
    d3 = st.number_input("Width Insulation", min_value=0.0, value=8.0, step=0.1)
    d4 = st.number_input("Depth Insulation", min_value=0.0, value=8.0, step=0.1)
    d5 = st.number_input("Height Insulation", min_value=0.0, value=8.0, step=0.1)


# --- Calculations Section ---
c7 = c3 * c4 * c5               # Internal Volume in cm3
c8 = c7 / 1000000               # Converted to m3
c9 = c7 / 1000                  # Converted to Liters

surface_area_cm2 = 2 * (c3 * c4 + c3 * c5 + c4 * c5)
surface_area_m2 = surface_area_cm2 / 10000


# --- Outputs Section ---
st.header("2. Area and Volume Calculation Results")

st.markdown("### Internal Volume")
st.metric(label="Volume (cm3)", value=f"{c7:,.1f} cm3")
st.metric(label="Volume (m3)", value=f"{c8:,.4f} m3")
st.metric(label="Volume (liters)", value=f"{c9:,.1f} liters")

st.markdown("### Internal Surface Area Verification")
st.metric(label="Surface Area (cm2)", value=f"{surface_area_cm2:,.1f} cm2")
st.metric(label="Surface Area (m2)", value=f"{surface_area_m2:,.2f} m2")


# --- Save / Export Section ---
st.header("3. Export Data")

# Create a clean data structure for Excel export
export_data = {
    "Metric Name": [
        "Cabinet Width W (cm)",
        "Cabinet Depth D (cm)",
        "Cabinet Height H (cm)",
        "Internal Volume (cm3)",
        "Internal Volume (m3)",
        "Internal Volume (liters)",
        "Internal Surface Area (cm2)",
        "Internal Surface Area (m2)",
    ],
    "Value": [c3, c4, c5, c7, c8, c9, surface_area_cm2, surface_area_m2],
}
df_export = pd.DataFrame(export_data)

# Convert dataframe to Excel bytes in background memory
buffer = io.BytesIO()
with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
    df_export.to_excel(writer, index=False, sheet_name="Calculations")
buffer.seek(0)

# Display download/save button
st.download_button(
    label="💾 Save Results to Excel",
    data=buffer,
    file_name="cabinet_calculations.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
)
