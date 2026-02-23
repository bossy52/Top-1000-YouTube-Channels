import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Top 1000 YouTube Channels Dashboard", layout="wide")

st.title("📊 Top 1000 YouTube Channels Interactive Dashboard")

uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    # ทำชื่อคอลัมน์ให้เป็นมาตรฐาน
    df.columns = df.columns.str.lower().str.strip()

    # เปลี่ยนชื่อคอลัมน์ให้ตรงกับ dataset
    rename_map = {
        "youtuber": "channel name",
        "uploads": "video count",
        "video views": "video views",
        "subscribers": "subscribers",
        "rank": "rank"
    }

    df = df.rename(columns=rename_map)

    # แปลงตัวเลข
    if "rank" in df.columns:
        df["rank"] = pd.to_numeric(df["rank"], errors="coerce")

    if "subscribers" in df.columns:
        df["subscribers"] = (
            df["subscribers"]
            .astype(str)
            .str.replace(",", "", regex=False)
        )
        df["subscribers"] = pd.to_numeric(df["subscribers"], errors="coerce")

    if "video views" in df.columns:
        df["video views"] = (
            df["video views"]
            .astype(str)
            .str.replace(",", "", regex=False)
        )
        df["video views"] = pd.to_numeric(df["video views"], errors="coerce")

    if "video count" in df.columns:
        df["video count"] = pd.to_numeric(df["video count"], errors="coerce")

    st.sidebar.header("Filter Dashboard")

    # Rank Filter
    if "rank" in df.columns:
        min_rank = int(df["rank"].min())
        max_rank = int(df["rank"].max())

        rank_range = st.sidebar.slider(
            "Select Rank Range",
            min_rank,
            max_rank,
            (1, 50)
        )

        df = df[(df["rank"] >= rank_range[0]) & (df["rank"] <= rank_range[1])]

    # Category Filter
    if "category" in df.columns:
        category = st.sidebar.multiselect(
            "Select Category",
            df["category"].dropna().unique()
        )
        if category:
            df = df[df["category"].isin(category)]

    # KPI
    col1, col2, col3 = st.columns(3)

    col1.metric("Total Channels", len(df))

    if "subscribers" in df.columns:
        col2.metric("Total Subscribers", f"{int(df['subscribers'].sum()):,}")

    if "video views" in df.columns:
        col3.metric("Total Views", f"{int(df['video views'].sum()):,}")

    st.divider()

    # Top Channels
    if "channel name" in df.columns and "subscribers" in df.columns:
        top10 = df.sort_values("subscribers", ascending=False).head(10)

        fig1 = px.bar(
            top10,
            x="channel name",
            y="subscribers",
            text_auto=True,
            title="Top 10 Channels by Subscribers"
        )
        st.plotly_chart(fig1, use_container_width=True)

    # Category Chart
    if "category" in df.columns:
        cat = df["category"].value_counts().reset_index()
        cat.columns = ["category", "count"]

        fig2 = px.pie(cat, names="category", values="count")
        st.plotly_chart(fig2, use_container_width=True)

    # Scatter Chart
    if "subscribers" in df.columns and "video views" in df.columns:
        fig3 = px.scatter(
            df,
            x="subscribers",
            y="video views",
            size="subscribers",
            hover_name="channel name"
        )
        st.plotly_chart(fig3, use_container_width=True)

    st.subheader("Full Dataset")
    st.dataframe(df)

else:
    st.info("Please upload the dataset CSV file.")
