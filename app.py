import streamlit as st
import pandas as pd
import plotly.express as px
import pickle

st.set_page_config(page_title="AgriVision Dashboard", layout="wide")

st.title("AgriVision Dashboard")
st.caption("Agricultural Data Visualization and Crop Recommendation System")

df = pd.read_csv("Data/cleared_crop_data.csv")

with open("crop_model.pkl", "rb") as f:
    model = pickle.load(f)

with open("label_encoder.pkl", "rb") as f:
    le = pickle.load(f)

with st.sidebar:
    st.header("Filters")
    label = st.selectbox("Select Label", options=["All"] + sorted(df["label"].unique().tolist()))

if label == "All":
    filtered_df = df
else:
    filtered_df = df[df["label"] == label]

tab1, tab2, tab3 = st.tabs(["Data", "Charts", "Prediction"])

with tab1:
    c1, c2 = st.columns(2)
    c1.metric("Total Rows Shown", len(filtered_df))
    c2.metric("Unique Labels", filtered_df["label"].nunique())
    selection = st.dataframe(filtered_df.head(10), use_container_width=True, on_select="rerun", selection_mode="multi-row")
    csv = filtered_df.to_csv(index=False).encode("utf-8")
    st.download_button("Download Filtered CSV", csv, "filtered_data.csv", "text/csv")

    st.write("Selected rows:")
    try:
        st.write(filtered_df.iloc[selection.selection.rows])
    except Exception:
        pass

with tab2:
    st.subheader("Label Count")
    st.bar_chart(df["label"].value_counts())

    st.subheader("Nitrogen Trend")
    st.line_chart(df[["N"]].head(20))

    st.subheader("Nitrogen vs Phosphorus")
    st.scatter_chart(df[["N", "P"]].head(50))

    st.subheader("Label Share")
    pie_df = df["label"].value_counts().reset_index()
    pie_df.columns = ["label", "count"]
    fig = px.pie(pie_df, names="label", values="count", title="Label Distribution")
    st.plotly_chart(fig, use_container_width=True)

with tab3:
    st.subheader("Crop Prediction Form")

    with st.form("prediction_form"):
        N = st.number_input("Nitrogen (N)", min_value=0.0, value=0.0)
        P = st.number_input("Phosphorus (P)", min_value=0.0, value=0.0)
        K = st.number_input("Potassium (K)", min_value=0.0, value=0.0)
        temperature = st.number_input("Temperature", min_value=0.0, value=0.0)
        humidity = st.number_input("Humidity", min_value=0.0, value=0.0)
        ph = st.number_input("pH", min_value=0.0, value=0.0)
        rainfall = st.number_input("Rainfall", min_value=0.0, value=0.0)
        submitted = st.form_submit_button("Predict")

    if submitted:
        values = [N, P, K, temperature, humidity, ph, rainfall]

        if any(v == 0 for v in values):
            st.error("Please enter all values. Zero is not allowed for prediction.")
        else:
            input_data = pd.DataFrame(
                [values],
                columns=["N", "P", "K", "temperature", "humidity", "ph", "rainfall"]
            )
            prediction = model.predict(input_data)
            predicted_label = le.inverse_transform(prediction)[0]
            st.success(f"Predicted Crop: {predicted_label}")

with st.expander("What this dashboard shows"):
    st.write("Use the sidebar filter to select a label, view summary metrics, inspect rows, download filtered data, see charts, and fill the prediction form.")

    st.markdown("---")
st.caption("Made by Neha Shrivastav")