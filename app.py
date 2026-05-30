import streamlit as st
import pandas as pd
import plotly.express as px
import pickle

st.set_page_config(page_title="AgriVision Dashboard", layout="wide")
px.defaults.template = "plotly_dark"

st.markdown("""
<style>
:root {
    --bg: #07111f;
    --bg-2: #0b1730;
    --panel: rgba(13, 24, 46, 0.88);
    --panel-2: rgba(17, 29, 55, 0.96);
    --border: rgba(148, 163, 184, 0.16);
    --text: #eef4ff;
    --muted: #9fb0cd;
    --soft-text: #c9d7ef;
    --accent: #38bdf8;
    --accent-2: #4ade80;
    --danger: #fb7185;
    --shadow: 0 18px 45px rgba(0, 0, 0, 0.28);
    --input-bg: rgba(14, 24, 44, 0.92);
    --input-text: #eef4ff;
    --input-border: rgba(148, 163, 184, 0.18);
    --menu-bg: #0f1b33;
    --menu-hover: #162746;
    --menu-text: #eef4ff;
}

/* Force a readable light-mode palette when Streamlit/app switches light */
@media (prefers-color-scheme: light) {
    :root {
        --bg: #eef4fb;
        --bg-2: #dde7f5;
        --panel: rgba(255, 255, 255, 0.92);
        --panel-2: rgba(246, 249, 253, 0.98);
        --border: rgba(42, 58, 92, 0.14);
        --text: #10203a;
        --muted: #4f6487;
        --soft-text: #31486d;
        --shadow: 0 16px 36px rgba(30, 41, 59, 0.10);
        --input-bg: #ffffff;
        --input-text: #10203a;
        --input-border: rgba(42, 58, 92, 0.16);
        --menu-bg: #ffffff;
        --menu-hover: #edf4ff;
        --menu-text: #10203a;
    }
}

.stApp {
    background:
        radial-gradient(circle at top left, rgba(56, 189, 248, 0.12), transparent 25%),
        radial-gradient(circle at top right, rgba(74, 222, 128, 0.10), transparent 22%),
        linear-gradient(180deg, var(--bg) 0%, var(--bg-2) 100%);
    color: var(--text);
}

div.block-container {
    max-width: 1225px;
    padding-top: 6rem;
    padding-bottom: 6rem;
    padding-left: clamp(2rem, 4vw, 4rem);
    padding-right: clamp(2rem, 4vw, 4rem);
}

[data-testid="stSidebar"] {
    display: none;
}

.hero-card {
    background: linear-gradient(135deg, var(--panel), var(--panel-2));
    border: 1px solid var(--border);
    border-radius: 28px;
    padding: 1.55rem 1.6rem 1.35rem 1.6rem;
    margin-bottom: 1.1rem;
    box-shadow: var(--shadow);
}

.eyebrow {
    display: inline-block;
    font-size: 0.78rem;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: var(--accent);
    margin-bottom: 0.55rem;
    font-weight: 800;
}

.hero-title {
    margin: 0;
    color: var(--text);
    font-size: 2.3rem;
    line-height: 1.1;
    font-weight: 900;
}

.hero-subtitle {
    margin-top: 0.65rem;
    color: var(--muted);
    font-size: 1rem;
    max-width: 780px;
    line-height: 1.7;
}

.section-card {
    background: linear-gradient(180deg, var(--panel), var(--panel-2));
    border: 1px solid var(--border);
    border-radius: 24px;
    padding: 1.05rem 1.15rem;
    box-shadow: var(--shadow);
    margin-bottom: 0.9rem;
}

.section-title {
    margin: 0 0 0.25rem 0;
    color: var(--text);
    font-size: 1.22rem;
    font-weight: 800;
}

.section-subtitle {
    margin: 0;
    color: var(--muted);
    font-size: 0.93rem;
    line-height: 1.55;
}

.metric-title {
    margin: 0.35rem 0 0.6rem 0;
    color: var(--text);
    font-size: 1rem;
    font-weight: 800;
}

.metric-card {
    background: linear-gradient(180deg, var(--panel), var(--panel-2));
    border: 1px solid var(--border);
    border-radius: 18px;
    padding: 0.72rem 0.8rem;
    box-shadow: var(--shadow);
    min-height: 92px;
    margin-bottom: 0.55rem;
}

.metric-label {
    color: var(--muted);
    font-size: 0.74rem;
    margin-bottom: 0.2rem;
}

.metric-value {
    color: var(--text);
    font-size: 1.48rem;
    line-height: 1.05;
    font-weight: 800;
}

.metric-delta {
    display: inline-block;
    margin-top: 0.35rem;
    padding: 0.2rem 0.48rem;
    border-radius: 999px;
    font-size: 0.66rem;
    font-weight: 700;
}

.metric-delta.positive {
    color: #16a34a;
    background: rgba(74, 222, 128, 0.14);
    border: 1px solid rgba(74, 222, 128, 0.22);
}

.metric-delta.negative {
    color: #e11d48;
    background: rgba(251, 113, 133, 0.12);
    border: 1px solid rgba(251, 113, 133, 0.18);
}
G
.info-tile {
    background: linear-gradient(180deg, var(--panel), var(--panel-2));
    border: 1px solid var(--border);
    border-radius: 18px;
    padding: 0.85rem 0.95rem;
    margin-top: 0.15rem;
    margin-bottom: 0.35rem;
}

.info-kicker {
    color: var(--accent);
    font-size: 0.74rem;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    font-weight: 800;
    margin-bottom: 0.3rem;
}

.info-value {
    color: var(--text);
    font-size: 1.55rem;
    font-weight: 900;
    line-height: 1.1;
}

.info-sub {
    color: var(--muted);
    font-size: 0.82rem;
    margin-top: 0.22rem;
}

div[data-testid="stRadio"] > div {
    background: var(--panel);
    border: 1px solid var(--border);
    border-radius: 999px;
    padding: 0.34rem 0.75rem;
    width: fit-content;
}

div[data-testid="stRadio"] label {
    color: var(--text) !important;
}

/* Selectbox and input main area */
div[data-baseweb="select"] > div,
div[data-baseweb="input"] > div {
    background: var(--input-bg) !important;
    border-radius: 14px !important;
    border: 1px solid var(--input-border) !important;
    color: var(--input-text) !important;
}

/* Selectbox visible text */
div[data-baseweb="select"] span,
div[data-baseweb="select"] div {
    color: var(--input-text) !important;
}

/* Input text */
input, textarea {
    color: var(--input-text) !important;
    -webkit-text-fill-color: var(--input-text) !important;
}

/* Labels above widgets */
label, .stSelectbox label, .stNumberInput label, .stTextInput label {
    color: var(--soft-text) !important;
    font-weight: 600 !important;
}

/* Dropdown menu popup */
div[role="listbox"] {
    background: var(--menu-bg) !important;
    color: var(--menu-text) !important;
    border: 1px solid var(--input-border) !important;
}

div[role="option"] {
    background: var(--menu-bg) !important;
    color: var(--menu-text) !important;
}

div[role="option"]:hover {
    background: var(--menu-hover) !important;
    color: var(--menu-text) !important;
}

/* Selected item / placeholder / icons inside selectboxes */
[data-baseweb="select"] svg,
[data-baseweb="input"] svg {
    fill: var(--input-text) !important;
    color: var(--input-text) !important;
}

[data-baseweb="select"] *::placeholder,
[data-baseweb="input"] *::placeholder {
    color: var(--muted) !important;
    opacity: 1 !important;
}

/* Metrics, text, dataframe */
div[data-testid="stMetricLabel"] *,
div[data-testid="stMetricValue"] * {
    color: var(--text) !important;
}

div[data-testid="stDataFrame"] {
    border: 1px solid var(--border);
    border-radius: 18px;
    overflow: hidden;
    margin-top: 0.4rem;
}

/* Plotly chart container */
.js-plotly-plot, .plotly, .plot-container {
    color: var(--text) !important;
}

/* Buttons */
.stButton > button,
.stDownloadButton > button,
div[data-testid="stFormSubmitButton"] button {
    border-radius: 14px !important;
    border: 1px solid rgba(74, 222, 128, 0.18) !important;
    background: linear-gradient(135deg, rgba(56, 189, 248, 0.18), rgba(74, 222, 128, 0.18)) !important;
    color: var(--text) !important;
    font-weight: 800 !important;
    min-height: 42px;
}

/* Footer */
.fixed-footer {
    position: fixed;
    bottom: 0;
    left: 0;
    width: 100%;
    background: color-mix(in srgb, var(--bg) 90%, black 10%);
    color: var(--muted);
    text-align: center;
    padding: 10px 0;
    font-size: 13px;
    border-top: 1px solid var(--border);
    z-index: 9999;
    backdrop-filter: blur(8px);
}
</style>
""", unsafe_allow_html=True)


def style_plotly(fig, title):
    fig.update_layout(
        template="plotly_dark",
        title=title,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=20, r=20, t=55, b=20),
        title_font=dict(size=20, color="#f8fbff"),
        font=dict(color="#d9e6fb"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    fig.update_xaxes(showgrid=False, zeroline=False)
    fig.update_yaxes(gridcolor="rgba(148,163,184,0.12)", zeroline=False)
    return fig


def delta_html(current, baseline):
    diff = current - baseline
    cls = "positive" if diff >= 0 else "negative"
    arrow = "↑" if diff >= 0 else "↓"
    return f'<div class="metric-delta {cls}">{arrow} {diff:+.2f}</div>'


def metric_card(title, value, delta_block=""):
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">{title}</div>
            <div class="metric-value">{value}</div>
            {delta_block}
        </div>
        """,
        unsafe_allow_html=True
    )


def performance_snapshot_vertical(filtered_df, df):
    overall_temp = df["temperature"].mean()
    overall_rainfall = df["rainfall"].mean()
    overall_humidity = df["humidity"].mean()

    filtered_temp = filtered_df["temperature"].mean()G
    filtered_rainfall = filtered_df["rainfall"].mean()
    filtered_humidity = filtered_df["humidity"].mean()

    st.markdown('<div class="metric-title">Performance Snapshot</div>', unsafe_allow_html=True)
    metric_card("Avg Temperature", f"{filtered_temp:.2f}", delta_html(filtered_temp, overall_temp))
    metric_card("Avg Rainfall", f"{filtered_rainfall:.2f}", delta_html(filtered_rainfall, overall_rainfall))
    metric_card("Avg Humidity", f"{filtered_humidity:.2f}", delta_html(filtered_humidity, overall_humidity))


df = pd.read_csv("Data/cleared_crop_data.csv")

with open("crop_model.pkl", "rb") as f:
    model = pickle.load(f)

with open("label_encoder.pkl", "rb") as f:
    le = pickle.load(f)

if "active_section" not in st.session_state:
    st.session_state.active_section = "Data"

if "data_label" not in st.session_state:
    st.session_state.data_label = "All"

if "chart_label" not in st.session_state:
    st.session_state.chart_label = "All"

label_options = ["All"] + sorted(df["label"].unique().tolist())

st.markdown("""
<div class="hero-card">
    <div class="eyebrow">Agriculture Intelligence Dashboard</div>
    <h1 class="hero-title">AgriVision Dashboard</h1>
    <div class="hero-subtitle">
        A polished analytical workspace for crop data exploration, visual discovery, and crop prediction using soil and environmental inputs.
    </div>
</div>
""", unsafe_allow_html=True)

section = st.radio(
    "Navigation",
    ["Data", "Charts", "Prediction"],
    key="active_section",
    horizontal=True,
    label_visibility="collapsed"
)

if section == "Data":
    st.markdown("""
        <div class="section-card">
            <div class="section-title">Filtered Data Explorer</div>
            <div class="section-subtitle">Inspect the filtered dataset, review the current subset, and download it for external use.</div>
        </div>
    """, unsafe_allow_html=True)

    filter_left, filter_space = st.columns([1.7, 4.3], gap="medium")
    with filter_left:
        data_label = st.selectbox(
            "Select Label",
            options=label_options,
            key="data_label"
        )

    if data_label == "All":
        filtered_df = df.copy()
    else:
        filtered_df = df[df["label"] == data_label].copy()

    left_col, right_col = st.columns([0.82, 2.78], gap="large")

    with left_col:
        performance_snapshot_vertical(filtered_df, df)

    with right_col:
        d1, d2, d3 = st.columns(3, gap="medium")

        d1.markdown(
            f"""
            <div class="info-tile">
                <div class="info-kicker">Rows in View</div>
                <div class="info-value">{len(filtered_df)}</div>
                <div class="info-sub">Currently displayed records</div>
            </div>
            """,
            unsafe_allow_html=True
        )
        d2.markdown(
            f"""
            <div class="info-tile">
                <div class="info-kicker">Unique Labels</div>
                <div class="info-value">{filtered_df["label"].nunique()}</div>
                <div class="info-sub">Distinct crop categories</div>
            </div>
            """,
            unsafe_allow_html=True
        )
        d3.markdown(
            f"""
            <div class="info-tile">
                <div class="info-kicker">Mean pH</div>
                <div class="info-value">{filtered_df["ph"].mean():.2f}</div>
                <div class="info-sub">Average soil acidity level</div>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.dataframe(
            filtered_df.head(15),
            use_container_width=True,
            hide_index=True
        )

        csv = filtered_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            "Download Filtered CSV",
            csv,
            "filtered_data.csv",
            "text/csv"
        )

elif section == "Charts":
    st.markdown("""
        <div class="section-card">
            <div class="section-title">Dynamic Chart Studio</div>
            <div class="section-subtitle">Choose a crop label, a column, and a chart type to generate an interactive visual instantly.</div>
        </div>
    """, unsafe_allow_html=True)

    chart_filter1, chart_filter2, chart_filter3 = st.columns([1.1, 1.1, 1.1], gap="medium")

    with chart_filter1:
        chart_label = st.selectbox(
            "Select Label",
            options=label_options,
            key="chart_label"
        )

    if chart_label == "All":
        chart_df = df.copy()
    else:
        chart_df = df[df["label"] == chart_label].copy()

    with chart_filter2:
        selected_column = st.selectbox(
            "Select Column",
            options=chart_df.columns.tolist()
        )

    is_numeric = pd.api.types.is_numeric_dtype(chart_df[selected_column])
    chart_options = ["Histogram", "Line Chart", "Box Plot", "Bar Chart", "Area Chart"] if is_numeric else ["Bar Chart", "Pie Chart"]

    with chart_filter3:
        selected_chart = st.selectbox(
            "Select Chart Type",
            options=chart_options
        )

    left_col, right_col = st.columns([0.82, 2.78], gap="large")

    with left_col:
        performance_snapshot_vertical(chart_df, df)

    with right_col:
        info1, info2, info3 = st.columns(3, gap="medium")

        info1.markdown(
            f"""
            <div class="info-tile">
                <div class="info-kicker">Chart Rows</div>
                <div class="info-value">{len(chart_df)}</div>
                <div class="info-sub">Rows available for plotting</div>
            </div>
            """,
            unsafe_allow_html=True
        )
        info2.markdown(
            f"""
            <div class="info-tile">
                <div class="info-kicker">Column Type</div>
                <div class="info-value">{"Numeric" if is_numeric else "Categorical"}</div>
                <div class="info-sub">Detected from selected field</div>
            </div>
            """,
            unsafe_allow_html=True
        )
        info3.markdown(
            f"""
            <div class="info-tile">
                <div class="info-kicker">Distinct Values</div>
                <div class="info-value">{chart_df[selected_column].nunique()}</div>
                <div class="info-sub">Unique entries in selection</div>
            </div>
            """,
            unsafe_allow_html=True
        )

        if is_numeric:
            if selected_chart == "Histogram":
                fig = px.histogram(chart_df, x=selected_column, nbins=25)
                st.plotly_chart(style_plotly(fig, f"Histogram — {selected_column} ({chart_label})"), use_container_width=True)

            elif selected_chart == "Line Chart":
                line_df = chart_df.reset_index().rename(columns={"index": "row_id"})
                fig = px.line(line_df, x="row_id", y=selected_column, markers=True)
                st.plotly_chart(style_plotly(fig, f"Line Chart — {selected_column} ({chart_label})"), use_container_width=True)

            elif selected_chart == "Box Plot":
                fig = px.box(chart_df, y=selected_column, points="outliers")
                st.plotly_chart(style_plotly(fig, f"Box Plot — {selected_column} ({chart_label})"), use_container_width=True)

            elif selected_chart == "Bar Chart":
                bar_df = chart_df.reset_index().rename(columns={"index": "row_id"}).head(20)
                fig = px.bar(bar_df, x="row_id", y=selected_column)
                st.plotly_chart(style_plotly(fig, f"Bar Chart — first 20 rows of {selected_column} ({chart_label})"), use_container_width=True)

            elif selected_chart == "Area Chart":
                area_df = chart_df.reset_index().rename(columns={"index": "row_id"})
                fig = px.area(area_df, x="row_id", y=selected_column)
                st.plotly_chart(style_plotly(fig, f"Area Chart — {selected_column} ({chart_label})"), use_container_width=True)

            s1, s2, s3 = st.columns(3, gap="medium")
            s1.metric("Minimum", f"{chart_df[selected_column].min():.2f}")
            s2.metric("Average", f"{chart_df[selected_column].mean():.2f}")
            s3.metric("Maximum", f"{chart_df[selected_column].max():.2f}")

        else:
            chart_data = chart_df[selected_column].value_counts().reset_index()
            chart_data.columns = [selected_column, "count"]

            if selected_chart == "Bar Chart":
                fig = px.bar(chart_data, x=selected_column, y="count")
                st.plotly_chart(style_plotly(fig, f"Bar Chart — {selected_column} ({chart_label})"), use_container_width=True)

            elif selected_chart == "Pie Chart":
                fig = px.pie(chart_data, names=selected_column, values="count", hole=0.45)
                st.plotly_chart(style_plotly(fig, f"Pie Chart — {selected_column} ({chart_label})"), use_container_width=True)

elif section == "Prediction":
    st.markdown("""
        <div class="section-card">
            <div class="section-title">Crop Prediction Workspace</div>
            <div class="section-subtitle">Enter soil and environmental values to predict the most suitable crop from the trained model.</div>
        </div>
    """, unsafe_allow_html=True)

    with st.form("prediction_form"):
        f1, f2 = st.columns(2, gap="large")

        with f1:
            N = st.number_input("Nitrogen (N)", min_value=0.0, value=0.0)
            P = st.number_input("Phosphorus (P)", min_value=0.0, value=0.0)
            K = st.number_input("Potassium (K)", min_value=0.0, value=0.0)
            temperature = st.number_input("Temperature", min_value=0.0, value=0.0)

        with f2:
            humidity = st.number_input("Humidity", min_value=0.0, value=0.0)
            ph = st.number_input("pH", min_value=0.0, value=0.0)
            rainfall = st.number_input("Rainfall", min_value=0.0, value=0.0)

        submitted = st.form_submit_button("Predict Crop")

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

st.markdown(
    """
    <div class="fixed-footer">
        Made by Neha Shrivastav
    </div>
    """,
    unsafe_allow_html=True
)