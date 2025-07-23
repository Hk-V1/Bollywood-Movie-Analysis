# streamlit_app.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import re

# --- Page Configuration ---
st.set_page_config(page_title="Bollywood Movies Dashboard", layout="wide")

# --- Load and Prepare Data ---
@st.cache_data
def load_data():
    df = pd.read_csv("final_combined_movies.csv")

    # Extract year from title using regex
    df['release_year'] = df['title'].str.extract(r"\((\d{4})\)", expand=False)
    df['release_year'] = pd.to_numeric(df['release_year'], errors='coerce')

    # Create decade column
    df['decade'] = (df['release_year'] // 10 * 10).astype('Int64').astype(str) + "s"

    # Convert ratings
    df['avg_rating'] = pd.to_numeric(df['avg_rating'], errors='coerce')

    return df

df = load_data()

st.title("Bollywood Movies Dashboard")
st.markdown("Explore ratings, tags, and trends in Bollywood movies.")

# --- Sidebar Filters ---
st.sidebar.header("Filter Movies")

decades = df['decade'].dropna().unique()
selected_decades = st.sidebar.multiselect("Choose Decade(s):", sorted(decades), default=sorted(decades))

tags = df['top_relevant_tags'].dropna().unique()
selected_tags = st.sidebar.multiselect("Filter by Tags:", sorted(tags))

min_rating, max_rating = st.sidebar.slider("Minimum Rating Range:", 0.0, 10.0, (0.0, 10.0), 0.1)

# --- Filtered Data ---
filtered_df = df[
    (df['decade'].isin(selected_decades)) &
    (df['avg_rating'].between(min_rating, max_rating))
]

if selected_tags:
    filtered_df = filtered_df[filtered_df['top_relevant_tags'].isin(selected_tags)]

# --- Layout Columns ---
col1, col2 = st.columns(2)

# Average Rating by Decade
with col1:
    st.subheader("Average Rating by Decade")
    avg_rating = (
        filtered_df.groupby("decade")["avg_rating"]
        .mean()
        .reset_index()
        .sort_values("decade")
    )

    fig1, ax1 = plt.subplots()
    sns.lineplot(data=avg_rating, x="decade", y="avg_rating", marker="o", ax=ax1)
    ax1.set_title("Average Ratings Across Decades")
    ax1.set_ylabel("Average Rating")
    ax1.set_xlabel("Decade")
    st.pyplot(fig1)

# Top Tags
with col2:
    st.subheader("Top 10 Tags")
    top_tags = (
        df['top_relevant_tags'].value_counts()
        .head(10)
        .reset_index()
        .rename(columns={'index': 'tag', 'top_relevant_tags': 'count'})
    )

    fig2, ax2 = plt.subplots()
    sns.barplot(data=top_tags, x="count", y="tag", palette="mako", ax=ax2)
    ax2.set_title("Most Frequent Tags")
    ax2.set_xlabel("Count")
    ax2.set_ylabel("Tag")
    st.pyplot(fig2)

# Rating Distribution
st.subheader("Rating Distribution")
fig3, ax3 = plt.subplots()
sns.histplot(filtered_df["avg_rating"], bins=20, kde=True, color="skyblue", ax=ax3)
ax3.set_title("Distribution of Average Ratings")
st.pyplot(fig3)

# Table of Filtered Movies
st.subheader("Filtered Movies Data")
st.dataframe(filtered_df[['title', 'release_year', 'avg_rating', 'top_relevant_tags']].reset_index(drop=True))

# Download CSV
st.download_button(
    label="Download Filtered Data as CSV",
    data=filtered_df.to_csv(index=False).encode('utf-8'),
    file_name='filtered_bollywood_movies.csv',
    mime='text/csv'
)
