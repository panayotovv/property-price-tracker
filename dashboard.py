import streamlit as st
import pandas as pd
import plotly.express as px
from database.repository import get_expensive_properties


# -------------------------------------------------
# Page Config
# -------------------------------------------------
st.set_page_config(
    page_title="Sofia Real Estate Analytics",
    layout="wide"
)

st.title("🏙 Sofia Real Estate Analytics Dashboard")


# -------------------------------------------------
# Load Data (Cached)
# -------------------------------------------------
@st.cache_data
def load_data():
    properties = get_expensive_properties()

    return pd.DataFrame([
        {
            "title": p.title,
            "price": p.price,
            "area": p.area,
            "district": p.location,
            "scraped_at": p.scraped_at,
            "price_per_m2": p.price / p.area if p.area else 0
        }
        for p in properties
    ])


df = load_data()

if df.empty:
    st.warning("No data available.")
    st.stop()


# -------------------------------------------------
# Sidebar Filters
# -------------------------------------------------
st.sidebar.header("Filters")

min_price, max_price = st.sidebar.slider(
    "Price Range (€)",
    int(df.price.min()),
    int(df.price.max()),
    (int(df.price.min()), int(df.price.max()))
)

min_area, max_area = st.sidebar.slider(
    "Area Range (m²)",
    int(df.area.min()),
    int(df.area.max()),
    (int(df.area.min()), int(df.area.max()))
)

selected_districts = st.sidebar.multiselect(
    "District",
    options=df.district.unique(),
    default=df.district.unique()
)

filtered_df = df[
    (df.price >= min_price) &
    (df.price <= max_price) &
    (df.area >= min_area) &
    (df.area <= max_area) &
    (df.district.isin(selected_districts))
]

if filtered_df.empty:
    st.warning("No properties match selected filters.")
    st.stop()


# -------------------------------------------------
# KPI SECTION
# -------------------------------------------------
total_listings = len(filtered_df)
total_market_value = filtered_df.price.sum()
average_area = filtered_df.area.mean()

weighted_price_m2 = (
    filtered_df.price.sum() / filtered_df.area.sum()
    if filtered_df.area.sum() else 0
)

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Listings", total_listings)
col2.metric("Total Market Value", f"{total_market_value:,.0f} €")
col3.metric("Average Area", f"{average_area:,.0f} m²")
col4.metric("Avg Price per m²", f"{weighted_price_m2:,.2f} €")

st.markdown("---")


# -------------------------------------------------
# Scatter Plot + Histogram
# -------------------------------------------------
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("📈 Price vs Area")

    fig_scatter = px.scatter(
        filtered_df,
        x="area",
        y="price",
        color="district",
        hover_data=["title", "price_per_m2"],
        title="Price vs Area"
    )

    st.plotly_chart(fig_scatter, use_container_width=True)


with col_right:
    st.subheader("📊 Price per m² Distribution")

    fig_hist = px.histogram(
        filtered_df,
        x="price_per_m2",
        nbins=20,
        title="Distribution of Price per m²"
    )

    st.plotly_chart(fig_hist, use_container_width=True)

st.markdown("---")


# -------------------------------------------------
# District Aggregation (Clean Version)
# -------------------------------------------------
st.subheader("🏙 Average Price per m² by District")

district_avg = (
    filtered_df
    .groupby("district", as_index=False)
    .agg(
        total_price=("price", "sum"),
        total_area=("area", "sum")
    )
)

district_avg["avg_price_m2"] = (
    district_avg["total_price"] / district_avg["total_area"]
)

district_avg = district_avg.sort_values(
    by="avg_price_m2",
    ascending=False
)

fig_bar = px.bar(
    district_avg,
    x="district",
    y="avg_price_m2",
    title="Average Price per m² by District"
)

st.plotly_chart(fig_bar, use_container_width=True)