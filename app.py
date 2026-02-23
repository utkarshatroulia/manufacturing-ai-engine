import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Manufacturing AI Engine", layout="wide")

# ---------- STYLE ----------
st.markdown("""
<style>
.main {
    background-color: #0e1117;
}
h1, h2, h3, h4 {
    color: #ffffff;
}
.metric-container {
    background-color: #1c1f26;
    padding: 15px;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

st.title("⚙ AI-Driven Manufacturing Optimization Engine")
st.caption("Adaptive Multi-Objective Golden Signature Framework")

# ---------- LOAD DATA ----------
data = pd.read_csv("manufacturing_data.csv")

# Normalize
data["Yield_Score"] = (data["Yield"] - data["Yield"].min()) / (data["Yield"].max() - data["Yield"].min())
data["Energy_Score"] = 1 - ((data["Energy_Consumption"] - data["Energy_Consumption"].min()) /
                             (data["Energy_Consumption"].max() - data["Energy_Consumption"].min()))
data["Quality_Score_Norm"] = (data["Quality_Score"] - data["Quality_Score"].min()) / \
                             (data["Quality_Score"].max() - data["Quality_Score"].min())

data["Optimization_Score"] = (
    0.4 * data["Yield_Score"] +
    0.3 * data["Energy_Score"] +
    0.3 * data["Quality_Score_Norm"]
)

# ---------- SESSION STATE ----------
if "golden_signature" not in st.session_state:
    st.session_state.golden_signature = data.loc[data["Optimization_Score"].idxmax()]

golden_signature = st.session_state.golden_signature

# ---------- TABS ----------
tab1, tab2, tab3 = st.tabs(["📊 Dashboard", "📁 Raw Data", "ℹ About System"])

# ================= DASHBOARD =================
with tab1:

    st.subheader("Golden Signature Overview")
    col1, col2, col3 = st.columns(3)

    col1.metric("Golden Yield", round(golden_signature["Yield"],2))
    col2.metric("Golden Energy (kWh)", round(golden_signature["Energy_Consumption"],2))
    col3.metric("Optimization Score", round(golden_signature["Optimization_Score"],3))

    st.divider()

    selected_batch_id = st.selectbox("Select Batch ID for Evaluation", data["Batch_ID"])
    selected_batch = data[data["Batch_ID"] == selected_batch_id].iloc[0]

    energy_diff = selected_batch["Energy_Consumption"] - golden_signature["Energy_Consumption"]
    yield_diff = selected_batch["Yield"] - golden_signature["Yield"]

    st.subheader("Performance Comparison")
    col4, col5, col6 = st.columns(3)

    col4.metric("Energy Difference", round(energy_diff,2))
    col5.metric("Yield Difference", round(yield_diff,2))
    col6.metric("Batch Score", round(selected_batch["Optimization_Score"],3))

    if energy_diff <= 0 and yield_diff >= 0:
        st.success("This batch outperforms the current Golden Signature.")
    elif energy_diff > 0:
        st.warning("This batch consumes more energy than optimal.")
    else:
        st.info("Performance close to optimal.")

    st.divider()

    st.subheader("AI Recommendations")

    if energy_diff > 0:
        st.write("• Reduce Temperature to decrease energy usage.")
    if yield_diff < 0:
        st.write("• Increase Machine Speed to improve yield.")
    if selected_batch["Pressure"] > golden_signature["Pressure"]:
        st.write("• Adjust Pressure to optimal range.")
    if energy_diff <= 0 and yield_diff >= 0:
        st.write("• Maintain current configuration — high efficiency detected.")

    st.divider()

    st.subheader("Sustainability Impact")

    energy_saved = max(0, -energy_diff)
    carbon_saved = energy_saved * 0.8
    cost_saved = energy_saved * 8

    col7, col8, col9 = st.columns(3)
    col7.metric("Energy Saved (kWh)", round(energy_saved,2))
    col8.metric("Carbon Reduced (kg CO2)", round(carbon_saved,2))
    col9.metric("Cost Saved (₹)", round(cost_saved,2))

    if energy_diff <= 0 and yield_diff >= 0:
        if st.button("Approve as New Golden Signature"):
            st.session_state.golden_signature = selected_batch
            st.success("Golden Signature Updated Successfully!")

    st.divider()

    st.subheader("Optimization Trend")
    plt.figure()
    plt.plot(data["Batch_ID"], data["Optimization_Score"])
    plt.xlabel("Batch ID")
    plt.ylabel("Optimization Score")
    st.pyplot(plt)

# ================= RAW DATA =================
with tab2:
    st.subheader("Complete Manufacturing Dataset")
    st.dataframe(data)

    csv = data.to_csv(index=False).encode('utf-8')
    st.download_button("Download Dataset CSV", csv, "manufacturing_data.csv", "text/csv")

# ================= ABOUT =================
with tab3:
    st.subheader("System Architecture")
    st.write("""
    - Multi-objective optimization balancing Yield, Energy, and Quality.
    - Golden Signature dynamic benchmarking.
    - Human-in-the-loop adaptive control.
    - Sustainability impact estimation.
    - Scalable for real-time IoT integration.
    """)

st.divider()
st.caption("Hackathon Prototype | AI-Driven Sustainable Manufacturing Intelligence")