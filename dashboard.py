import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import altair as alt

# Title
st.title("Cloud Cost Management Dashboard")

# Sample Cloud Cost Data
data = pd.DataFrame(
    {
        "Service": ["Compute", "Storage", "Networking", "Database", "AI Services", "Security"],
        "Cost": np.random.randint(500, 5000, 6),
    }
)

# Matplotlib Bar Chart - Service Cost Breakdown
st.subheader("Service Cost Breakdown")
fig, ax = plt.subplots()
ax.bar(data["Service"], data["Cost"], color='skyblue')
ax.set_xlabel("Service")
ax.set_ylabel("Cost ($)")
ax.set_title("Cloud Service Cost Breakdown")
st.pyplot(fig)

# Plotly Pie Chart - Cost Distribution by Service
st.subheader("Cost Distribution by Service")
fig_pie = px.pie(data, names="Service", values="Cost", title="Cost Distribution by Service")
st.plotly_chart(fig_pie)

# Altair Line Chart - Monthly Cost Trend
st.subheader("Monthly Cost Trend")
monthly_data = pd.DataFrame(
    {
        "Month": pd.date_range(start="2024-01-01", periods=6, freq='M').strftime('%b %Y'),
        "Cost": np.random.randint(10000, 50000, 6),
    }
)
chart = (
    alt.Chart(monthly_data)
    .mark_line(point=True)
    .encode(x="Month", y="Cost", tooltip=["Month", "Cost"])
    .properties(title="Monthly Cloud Cost Trend")
)
st.altair_chart(chart, use_container_width=True)

# Additional Data - Region Wise Costs
st.subheader("Region-wise Cloud Cost Breakdown")
region_data = pd.DataFrame(
    {
        "Region": ["US-East", "US-West", "Europe", "Asia", "Australia"],
        "Cost": np.random.randint(5000, 20000, 5),
    }
)
fig_bar = px.bar(region_data, x="Region", y="Cost", title="Region-wise Cloud Cost Breakdown", color="Region")
st.plotly_chart(fig_bar)

# Heatmap of Costs by Service and Region
st.subheader("Cost Heatmap by Service and Region")
heatmap_data = pd.DataFrame(
    np.random.randint(500, 5000, size=(6, 5)),
    columns=["US-East", "US-West", "Europe", "Asia", "Australia"],
    index=["Compute", "Storage", "Networking", "Database", "AI Services", "Security"]
)
st.write(heatmap_data.style.background_gradient(cmap="Blues"))
