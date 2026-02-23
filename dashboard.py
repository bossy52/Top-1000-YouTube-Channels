import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Top 1000 YouTube Channels Dashboard", layout="wide")

st.title("Top 1000 YouTube Channels Interactive Dashboard")

# Upload CSV
uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    st.sidebar.header("Filter")

    # Filter Category
    if "category" in df.columns:
        category = st.sidebar.multiselect(
            "Select Category",
            df["category"].dropna().unique()
        )
        if category:
            df = df[df["category"].isin(category)]

    # Filter Rank
    if "rank" in df.columns:
        rank_range = st.sidebar.slider(
            "Select Rank Range",
            int(df["rank"].min()),
            int(df["rank"].max()),
            (1, 50)
        )
        df = df[(df["rank"] >= rank_range[0]) & (df["rank"] <= rank_range[1])]

    # KPI
    col1, col2, col3 = st.columns(3)

    if "subscribers" in df.columns:
        col1.metric("Total Subscribers", f"{df['subscribers'].sum():,}")

    if "video views" in df.columns:
        col2.metric("Total Views", f"{df['video views'].sum():,}")

    col3.metric("Total Channels", len(df))

    st.divider()

    # Chart 1 Top Channels
    if "subscribers" in df.columns and "channel name" in df.columns:
        top10 = df.sort_values("subscribers", ascending=False).head(10)

        fig1 = px.bar(
            top10,
            x="channel name",
            y="subscribers",
            text_auto=True,
            title="Top 10 Channels by Subscribers"
        )
        st.plotly_chart(fig1, use_container_width=True)

    # Chart 2 Category
    if "category" in df.columns:
        cat_count = df["category"].value_counts().reset_index()
        cat_count.columns = ["category", "count"]

        fig2 = px.pie(
            cat_count,
            names="category",
            values="count",
            title="Channel Categories Distribution"
        )
        st.plotly_chart(fig2, use_container_width=True)

    # Chart 3 Subscribers vs Views
    if "subscribers" in df.columns and "video views" in df.columns:
        fig3 = px.scatter(
            df,
            x="subscribers",
            y="video views",
            size="subscribers",
            hover_name="channel name",
            title="Subscribers vs Video Views"
        )
        st.plotly_chart(fig3, use_container_width=True)

    st.divider()

    # Full Data
    st.subheader("Full Dataset")
    st.dataframe(df)

else:
    st.info("Please upload the YouTube dataset CSV file.")
