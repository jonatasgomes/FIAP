import streamlit as st
import pandas as pd
import plotly.express as px
import os

# Load NDVI data
file_path = os.path.join(os.path.dirname(__file__), "NDVI_Stats.csv")
df = pd.read_csv(file_path)

# Streamlit UI
st.title("NDVI Analysis for Mato Grosso")

# Since your data doesn't have field_id, use system:index instead
index_id = st.selectbox("Select Index", df["system:index"].unique())

# Filter data
df_selected = df[df["system:index"] == index_id]

# Display the NDVI value
st.subheader(f"NDVI Statistics for Index: {index_id}")
st.metric("Mean NDVI", f"{df_selected['mean'].values[0]:.4f}")

# Show the data
st.subheader("Raw Data")
st.dataframe(df_selected)

# If you want to visualize more when you have multiple entries:
# st.subheader("All Data")
# fig = px.bar(df, x="system:index", y="mean", title="NDVI Values by Index")
# st.plotly_chart(fig)
