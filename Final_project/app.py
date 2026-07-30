import streamlit as st
import pandas as pd
import plotly.express as px

# ----------------------------
# Page Configuration
# ----------------------------
st.set_page_config(
    page_title="Netflix Dashboard",
    page_icon="🎬",
    layout="wide"
)

# ----------------------------
# Dashboard Title
# ----------------------------
st.title("🎬 Netflix Movies & TV Shows Dashboard")

st.write("Welcome to my Data Visualization Project!")

st.write("This dashboard analyzes Netflix Movies and TV Shows using interactive charts.")

# ----------------------------
# Load Dataset
# ----------------------------
df = pd.read_csv("netflix_titles_cleaned_fixed.csv")

# ----------------------------
# Show Dataset
# ----------------------------
st.subheader("Netflix Dataset")

st.dataframe(df)

# =====================================
# DASHBOARD SUMMARY
# =====================================

st.markdown("---")
st.subheader("📊 Dashboard Summary")

total_titles = len(df)
movies = len(df[df["type"] == "Movie"])
tv_shows = len(df[df["type"] == "TV Show"])
countries = df["country"].nunique()

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("🎬 Total Titles", total_titles)

with col2:
    st.metric("🎥 Movies", movies)

with col3:
    st.metric("📺 TV Shows", tv_shows)

with col4:
    st.metric("🌍 Countries", countries)
    
    # =====================================
# SIDEBAR FILTERS
# =====================================

st.sidebar.title("🎛 Dashboard Filters")

country_options = ["All"] + sorted(df["country"].dropna().unique().tolist())

selected_country = st.sidebar.selectbox(
    "Country",
    country_options
)

genre_options = ["All"] + sorted(df["listed_in"].dropna().unique().tolist())

selected_genre = st.sidebar.selectbox(
    "Genre",
    genre_options
)

year_options = ["All"] + sorted(df["release_year"].unique().tolist())

selected_year = st.sidebar.selectbox(
    "Release Year",
    year_options
)

# =====================================
# FILTER DATA
# =====================================

filtered_df = df.copy()

if selected_country != "All":
    filtered_df = filtered_df[
        filtered_df["country"] == selected_country
    ]

if selected_genre != "All":
    filtered_df = filtered_df[
        filtered_df["listed_in"] == selected_genre
    ]

if selected_year != "All":
    filtered_df = filtered_df[
        filtered_df["release_year"] == selected_year
    ]
    
    # =====================================
# MOVIES VS TV SHOWS
# =====================================

st.markdown("---")
st.subheader("🎥 Movies vs TV Shows")

type_count = (
    filtered_df["type"]
    .value_counts()
    .reset_index()
)

type_count.columns = ["Type", "Count"]

fig = px.bar(
    type_count,
    x="Type",
    y="Count",
    color="Type",
    text="Count",
    title="Movies vs TV Shows"
)

st.plotly_chart(fig, use_container_width=True)

# =====================================
# NETFLIX CONTENT GROWTH
# =====================================

st.markdown("---")
st.subheader("📈 Netflix Content Growth")

yearly = (
    filtered_df.groupby("release_year")
    .size()
    .reset_index(name="Titles")
)

fig2 = px.line(
    yearly,
    x="release_year",
    y="Titles",
    markers=True,
    title="Netflix Content Released by Year"
)

st.plotly_chart(fig2, use_container_width=True)

# =====================================
# TOP COUNTRIES
# =====================================

st.markdown("---")
st.subheader("🌍 Top 10 Countries")

country_df = filtered_df.copy()

country_df["country"] = country_df["country"].str.split(",")

country_df = country_df.explode("country")

country_df["country"] = country_df["country"].str.strip()

top_country = (
    country_df["country"]
    .value_counts()
    .head(10)
    .reset_index()
)

top_country.columns = ["Country", "Titles"]

fig3 = px.bar(
    top_country,
    x="Country",
    y="Titles",
    color="Titles",
    text="Titles",
    title="Top 10 Countries"
)

st.plotly_chart(fig3, use_container_width=True)

# =====================================
# TOP GENRES
# =====================================

st.markdown("---")
st.subheader("🎭 Top Genres")

genre_df = filtered_df.copy()

genre_df["listed_in"] = genre_df["listed_in"].str.split(",")

genre_df = genre_df.explode("listed_in")

genre_df["listed_in"] = genre_df["listed_in"].str.strip()

top_genre = (
    genre_df["listed_in"]
    .value_counts()
    .head(10)
    .reset_index()
)

top_genre.columns = ["Genre", "Titles"]

fig4 = px.bar(
    top_genre,
    x="Genre",
    y="Titles",
    color="Titles",
    text="Titles",
    title="Top 10 Genres"
)

st.plotly_chart(fig4, use_container_width=True)

# =====================================
# CONTENT RATINGS
# =====================================

st.markdown("---")
st.subheader("⭐ Content Ratings")

rating_df = (
    filtered_df["rating"]
    .value_counts()
    .reset_index()
)

rating_df.columns = ["Rating", "Titles"]

fig5 = px.pie(
    rating_df,
    names="Rating",
    values="Titles",
    title="Netflix Ratings Distribution"
)

st.plotly_chart(fig5, use_container_width=True)

# =====================================
# MONTHLY CONTENT ADDED
# =====================================

st.markdown("---")
st.subheader("📅 Monthly Content Added")

month_df = (
    filtered_df["date_added_month"]
    .value_counts()
    .reset_index()
)

month_df.columns = ["Month", "Titles"]

month_order = [
    "January","February","March","April",
    "May","June","July","August",
    "September","October","November","December"
]

month_df["Month"] = pd.Categorical(
    month_df["Month"],
    categories=month_order,
    ordered=True
)

month_df = month_df.sort_values("Month")

fig6 = px.line(
    month_df,
    x="Month",
    y="Titles",
    markers=True,
    title="Titles Added by Month"
)

st.plotly_chart(fig6, use_container_width=True)

# =====================================
# TOP DIRECTORS
# =====================================

st.markdown("---")
st.subheader("🎬 Top Directors")

director_df = filtered_df.copy()

director_df["director"] = director_df["director"].str.split(",")

director_df = director_df.explode("director")

director_df["director"] = director_df["director"].str.strip()

director_df = director_df[
    director_df["director"] != "Unknown"
]

top_directors = (
    director_df["director"]
    .value_counts()
    .head(10)
    .reset_index()
)

top_directors.columns = ["Director", "Titles"]

fig7 = px.bar(
    top_directors,
    x="Director",
    y="Titles",
    color="Titles",
    text="Titles",
    title="Top Directors on Netflix"
)

st.plotly_chart(fig7, use_container_width=True)

# =====================================
# FILTERED DATASET
# =====================================

st.markdown("---")
st.subheader("📋 Filtered Dataset")

st.dataframe(filtered_df)

# =====================================
# FOOTER
# =====================================

st.markdown("---")

st.markdown(
    """
    ### 🎓 Data Visualization Final Project

    **Student:** Manish Mourya

    **Dataset:** Netflix Movies and TV Shows

    **Tool Used:** Streamlit + Plotly + Pandas
    """
)