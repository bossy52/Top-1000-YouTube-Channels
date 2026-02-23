import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Top 1000 YouTube Channels Dashboard",
    layout="wide"
)

st.title("📊 Top 1000 YouTube Channels Interactive Dashboard")

st.markdown("Upload dataset (CSV) from Kaggle to start analysis")

# Upload CSV
uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    # ทำชื่อคอลัมน์ให้เป็นมาตรฐาน
    df.columns = df.columns.str.lower().str.strip()

    st.sidebar.header("Filter Dashboard")

    # -------- Filter Category --------
    if "category" in df.columns:
        category_filter = st.sidebar.multiselect(
            "Select Category",
            df["category"].dropna().unique()
        )
        if category_filter:
            df = df[df["category"].isin(category_filter)]

    # -------- Filter Rank --------
    if "rank" in df.columns:
        min_rank = int(df["rank"].min())
        max_rank = int(df["rank"].max())

        rank_range = st.sidebar.slider(
            "Select Rank Range",
            min_rank,
            max_rank,
            (min_rank, min_rank + 50)
        )

        df = df[
            (df["rank"] >= rank_range[0]) &
            (df["rank"] <= rank_range[1])
        ]

    # -------- Search Channel --------
    if "channel name" in df.columns:
        search = st.sidebar.text_input("Search Channel Name")
        if search:
            df = df[df["channel name"].str.contains(search, case=False)]

    # -------- KPI --------
    st.subheader("📌 Key Statistics")

    col1, col2, col3, col4 = st.columns(4)

    if "subscribers" in df.columns:
        col1.metric(
            "Total Subscribers",
            f"{int(df['subscribers'].sum()):,}"
        )

    if "video views" in df.columns:
        col2.metric(
            "Total Views",
            f"{int(df['video views'].sum()):,}"
        )

    if "video count" in df.columns:
        col3.metric(
            "Total Videos",
            f"{int(df['video count'].sum()):,}"
        )

    col4.metric("Total Channels", len(df))

    st.divider()

    # -------- Chart 1 Top Channels --------
    if "subscribers" in df.columns and "channel name" in df.columns:
        st.subheader("Top 10 Channels by Subscribers")

        top10 = df.sort_values(
            "subscribers",
            ascending=False
        ).head(10)

        fig1 = px.bar(
            top10,
            x="channel name",
            y="subscribers",
            text_auto=True
        )

        st.plotly_chart(fig1, use_container_width=True)

    # -------- Chart 2 Category --------
    if "category" in df.columns:
        st.subheader("Channel Category Distribution")

        cat_data = df["category"].value_counts().reset_index()
        cat_data.columns = ["category", "count"]

        fig2 = px.pie(
            cat_data,
            names="category",
            values="count"
        )

        st.plotly_chart(fig2, use_container_width=True)

    # -------- Chart 3 Views vs Subscribers --------
    if "subscribers" in df.columns and "video views" in df.columns:
        st.subheader("Subscribers vs Views")

        fig3 = px.scatter(
            df,
            x="subscribers",
            y="video views",
            size="subscribers",
            hover_name="channel name"
        )

        st.plotly_chart(fig3, use_container_width=True)

    # -------- Chart 4 Most Active Channels --------
    if "video count" in df.columns and "channel name" in df.columns:
        st.subheader("Top Channels by Video Count")

        active = df.sort_values(
            "video count",
            ascending=False
        ).head(10)

        fig4 = px.bar(
            active,
            x="channel name",
            y="video count",
            text_auto=True
        )

        st.plotly_chart(fig4, use_container_width=True)

    st.divider()

    # -------- Full Data --------
    st.subheader("📄 Full Dataset")
    st.dataframe(df)

else:
    st.info("Please upload the Top 1000 YouTube Channels dataset (.csv)")
