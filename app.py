import streamlit as st
import json
import pandas as pd
from pathlib import Path

st.set_page_config(page_title="CloudWarden Web", layout="wide")

st.title("☁️ CloudWarden IAM Audit Dashboard")
st.markdown("Visualize findings from AWS IAM security audits")

# Load JSON Report
report_path = Path("reports/sample_report.json")
if not report_path.exists():
    st.error("Audit report not found at reports/sample_report.json")
    st.stop()

with open(report_path, "r") as f:
    data = json.load(f)

if not data:
    st.warning("No findings in report.")
    st.stop()

df = pd.DataFrame(data)

# Sidebar Filter
finding_types = df['type'].unique()
selected_types = st.sidebar.multiselect("Filter by Finding Type", finding_types, default=list(finding_types))

filtered_df = df[df['type'].isin(selected_types)]

# Metrics
# Metrics
col1, col2 = st.columns(2)
col1.metric("🔍 Total Findings", len(filtered_df))
col2.metric("👥 Affected Users", filtered_df['user'].nunique())

# Charts
st.subheader("📊 Finding Types Overview")
chart_data = filtered_df['type'].value_counts().reset_index()
chart_data.columns = ['Finding Type', 'Count']
st.bar_chart(chart_data.set_index('Finding Type'))

# Optional Pie Chart
try:
    import matplotlib.pyplot as plt

    pie_data = chart_data.set_index('Finding Type')['Count']
    fig, ax = plt.subplots()
    ax.pie(pie_data, labels=pie_data.index, autopct='%1.1f%%')
    ax.set_title("IAM Finding Distribution")
    st.pyplot(fig)

except ImportError:
    st.info("Install matplotlib to enable pie chart: pip install matplotlib")


# Table
st.subheader("📋 IAM Findings")
st.dataframe(filtered_df.reset_index(drop=True), use_container_width=True)

# Download Button
st.download_button(
    label="📥 Download Filtered JSON",
    data=filtered_df.to_json(orient="records", indent=2),
    file_name="filtered_iam_findings.json",
    mime="application/json"
)
