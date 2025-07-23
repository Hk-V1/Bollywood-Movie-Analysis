import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

@st.cache_data
def load_data():
    df = pd.read_csv("final_combined_movies.csv")
    return df

df = load_data()

st.title("Bollywood Movies Dashboard")
st.markdown("Explore ratings, tags, and trends in Bollywood cinema")

# --- Sidebar Filters ---
st.sidebar.header("Filter Movies")
selected_decade = st.sidebar.multiselect(
    "Select Decade(s)",
    options=df['decade'].dropna().unique(),
    default=df['decade'].dropna().unique()
)

selected_tags = st.sidebar.multiselect(
    "Select Tags",
    options=df['top_relevant_tags'].dropna().unique(),
    default=[]
)

filtered_df = df[df['decade'].isin(selected_decade)]

if selected_tags:
    filtered_df = filtered_df[filtered_df['top_relevant_tags'].isin(selected_tags)]

st.subheader("Average Rating by Decade")
avg_rating_by_decade = (
    filtered_df.groupby("decade")["avg_rating"]
    .mean()
    .reset_index()
    .sort_values("decade")
)

fig, ax = plt.subplots()
sns.lineplot(data=avg_rating_by_decade, x="decade", y="avg_rating", marker="o", ax=ax)
ax.set_title("Average Ratings Across Decades")
st.pyplot(fig)

st.subheader("Most Common Tags")

all_tags_series = df["top_relevant_tags"].dropna()
tag_counts = all_tags_series.value_counts().head(10)

fig2, ax2 = plt.subplots()
sns.barplot(x=tag_counts.values, y=tag_counts.index, palette="viridis", ax=ax2)
ax2.set_title("Top 10 Tags")
st.pyplot(fig2)

st.subheader("Ratings Distribution")

fig3, ax3 = plt.subplots()
sns.histplot(filtered_df['avg_rating'], kde=True, bins=20, ax=ax3, color="skyblue")
ax3.set_title("Distribution of Average Ratings")
st.pyplot(fig3)

# --- Raw Data View ---
with st.expander("View Raw Data"):
    st.dataframe(filtered_df)

