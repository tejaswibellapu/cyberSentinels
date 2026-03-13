
import streamlit as st
import pandas as pd
import sqlite3
import os
import time
import plotly.express as px

# ---------------- DATABASE PATH ---------------- #

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "../database/threats.db")

# ---------------- PAGE CONFIG ---------------- #

st.set_page_config(page_title="Cyber Autonomous Defense", layout="wide")

# ---------------- CUSTOM STYLE ---------------- #

st.markdown("""
<style>

/* APP BACKGROUND */

.stApp {
    background-color: white;
    color: black;
}

/* TITLES */

h1,h2,h3 {
    color:#1f5fe0 !important;
}

/* METRIC BOX */

[data-testid="stMetric"] {
    background-color:white;
    padding:20px;
    border-radius:12px;
    border:2px solid black;
    text-align:center;
}

[data-testid="stMetricLabel"]{
    font-size:18px !important;
    font-weight:bold !important;
    color:black !important;
}

[data-testid="stMetricValue"]{
    font-size:36px !important;
    font-weight:bold !important;
    color:black !important;
}

/* TABLE TITLE */

.live-title{
    font-size:32px;
    font-weight:900;
    color:black;
    text-transform:uppercase;
    margin-bottom:10px;
}

/* DATAFRAME OUTER BORDER */

[data-testid="stDataFrame"] {
    border:2px solid black !important;
}

/* HEADER ROW */

[data-testid="stDataFrame"] thead th {
    background-color:white !important;
    color:black !important;
    border:1px solid black !important;
    font-weight:bold !important;
    text-transform:uppercase;
}

/* TABLE CELLS */

[data-testid="stDataFrame"] tbody td {
    background-color:white !important;
    color:black !important;
    border:1px solid black !important;
}

/* INDEX COLUMN */

[data-testid="stDataFrame"] tbody th {
    background-color:white !important;
    color:black !important;
    border:1px solid black !important;
}

/* REMOVE STREAMLIT DARK INDEX BAR */

[data-testid="stDataFrame"] [role="rowheader"] {
    background-color:white !important;
    color:black !important;
    border:1px solid black !important;
}

</style>
""", unsafe_allow_html=True)

st.title("🛡 Cyber Autonomous Defense Dashboard")

# ---------------- DATABASE FUNCTION ---------------- #

def load_data():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM threats ORDER BY id DESC", conn)
    conn.close()
    return df

# ---------------- LOAD DATA ---------------- #

df = load_data()

# ---------------- RISK SEVERITY ---------------- #

def classify_risk(score):
    if score > 80:
        return "Critical"
    elif score >= 50:
        return "Medium"
    else:
        return "Low"

if len(df) > 0:
    df["severity"] = df["risk_score"].apply(classify_risk)

# ---------------- METRICS ---------------- #

col1, col2, col3 = st.columns(3)

if len(df) > 0:
    total_attacks = len(df)
    top_attacker = df["attacker_ip"].value_counts().idxmax()
    max_risk = df["risk_score"].max()
else:
    total_attacks = 0
    top_attacker = "None"
    max_risk = 0

col1.metric(" Total Attacks Detected", total_attacks)
col2.metric(" Top Attacker IP", top_attacker)
col3.metric("⚠ Highest Risk Score", max_risk)

st.divider()

# ---------------- LIVE THREAT FEED ---------------- #

st.markdown('<div class="live-title">📡 LIVE THREAT FEED</div>', unsafe_allow_html=True)

if len(df) > 0:

    def color_severity(val):
        if val == "Critical":
            return "color:red; font-weight:bold"
        elif val == "Medium":
            return "color:orange; font-weight:bold"
        elif val == "Low":
            return "color:green; font-weight:bold"
        else:
            return ""

    styled_df = df.style.map(color_severity, subset=["severity"])

    st.dataframe(styled_df, use_container_width=True)

else:
    st.info("No threats detected yet.")

st.divider()

# ---------------- VISUALIZATION ---------------- #

if len(df) > 0:

    col4, col5 = st.columns(2)

    # -------- Risk Score Distribution -------- #

    with col4:

        st.subheader("⚠ Risk Score Distribution")

        fig = px.bar(
            df,
            x=df.index,
            y="risk_score",
            color="severity",
            color_discrete_map={
                "Critical": "red",
                "Medium": "orange",
                "Low": "green"
            }
        )

        fig.update_layout(
            template="plotly_white",
            paper_bgcolor="white",
            plot_bgcolor="white",
            font=dict(color="black", size=14),

            xaxis=dict(
                showline=True,
                linecolor="black",
                tickfont=dict(color="black", size=14),
                title_font=dict(color="black")
            ),

            yaxis=dict(
                showline=True,
                linecolor="black",
                tickfont=dict(color="black", size=14),
                title_font=dict(color="black")
            )
        )

        st.plotly_chart(fig, use_container_width=True)

    # -------- Attacker IP Frequency -------- #

    with col5:

        st.subheader(" Attacker IP Frequency")

        ip_counts = df["attacker_ip"].value_counts().reset_index()
        ip_counts.columns = ["attacker_ip", "count"]

        fig2 = px.bar(
            ip_counts,
            x="attacker_ip",
            y="count",
            color="count",
            color_continuous_scale=[
                "#dbe9f1",
                "#6aaed6",
                "#2171b5",
                "#08306b"
            ]
        )

        fig2.update_layout(
            template="plotly_white",
            paper_bgcolor="white",
            plot_bgcolor="white",
            font=dict(color="black", size=14),

            xaxis=dict(
                showline=True,
                linecolor="black",
                tickfont=dict(color="black", size=13),
                title_font=dict(color="black")
            ),

            yaxis=dict(
                showline=True,
                linecolor="black",
                tickfont=dict(color="black", size=13),
                title_font=dict(color="black")
            ),

            coloraxis_colorbar=dict(
                title_font=dict(color="black"),
                tickfont=dict(color="black")
            )
        )

        st.plotly_chart(fig2, use_container_width=True)

# ---------------- AUTO REFRESH ---------------- #

time.sleep(3)
st.rerun()