"""A working dashboard: filters, metrics, charts, and a download.

This is the shape most internal Streamlit tools end up in, and it puts the
earlier pieces together. Loading is cached so filtering is instant, filter
widgets live in the sidebar, the aggregation runs on every rerun because it is
cheap, and the result is offered as a CSV download.

The deliberate ordering is: cache the expensive read, filter with plain pandas,
then render. There is no reactive graph to declare. The script is the graph.

Run it:

    streamlit run streamlit_orders_dashboard.py
"""

from pathlib import Path

import pandas as pd
import streamlit as st

DATA = Path(__file__).parent / "data" / "orders.csv"

st.set_page_config(page_title="Orders dashboard", layout="wide")


@st.cache_data
def load_orders(path: str) -> pd.DataFrame:
    df = pd.read_csv(path, parse_dates=["order_date"])
    df["margin"] = df["revenue"] - df["cost"]
    df["month"] = df["order_date"].dt.to_period("M").dt.to_timestamp()
    return df


orders = load_orders(str(DATA))

st.title("Orders")
st.caption(f"{orders['order_date'].min():%b %d, %Y} to {orders['order_date'].max():%b %d, %Y}, synthetic data.")

with st.sidebar:
    st.header("Filters")
    date_range = st.date_input(
        "Order date",
        value=(orders["order_date"].min().date(), orders["order_date"].max().date()),
        min_value=orders["order_date"].min().date(),
        max_value=orders["order_date"].max().date(),
    )
    regions = st.multiselect("Region", sorted(orders["region"].unique()))
    segments = st.multiselect("Segment", sorted(orders["segment"].unique()))
    channels = st.multiselect("Channel", sorted(orders["channel"].unique()))
    min_revenue = st.slider("Minimum order revenue", 0, 25_000, 0, step=500)

view = orders

# `st.date_input` with a range returns a 1-tuple while the user is mid-selection,
# so guard for the incomplete case rather than unpacking blindly.
if isinstance(date_range, tuple) and len(date_range) == 2:
    start, end = (pd.Timestamp(d) for d in date_range)
    view = view[view["order_date"].between(start, end)]

if regions:
    view = view[view["region"].isin(regions)]
if segments:
    view = view[view["segment"].isin(segments)]
if channels:
    view = view[view["channel"].isin(channels)]
view = view[view["revenue"] >= min_revenue]

if view.empty:
    st.warning("No orders match these filters.")
    st.stop()  # stops this run here; the widgets above stay on screen

revenue = view["revenue"].sum()
margin = view["margin"].sum()

kpi = st.columns(4)
kpi[0].metric("Revenue", f"${revenue:,.0f}", border=True)
kpi[1].metric("Margin", f"${margin:,.0f}", delta=f"{margin / revenue:.1%} rate", border=True)
kpi[2].metric("Orders", f"{len(view):,}", border=True)
kpi[3].metric("Average order", f"${revenue / len(view):,.0f}", border=True)

tab_trend, tab_mix, tab_rows = st.tabs(["Trend", "Mix", "Rows"])

with tab_trend:
    by_month = view.groupby("month", as_index=False)[["revenue", "margin"]].sum()
    st.line_chart(by_month, x="month", y=["revenue", "margin"], x_label="Month", y_label="USD")

with tab_mix:
    left, right = st.columns(2)
    with left:
        by_segment = view.groupby("segment", as_index=False)["revenue"].sum()
        st.bar_chart(by_segment, x="segment", y="revenue", x_label="Segment", y_label="Revenue")
    with right:
        by_region = view.groupby("region", as_index=False)["margin"].sum()
        st.bar_chart(by_region, x="region", y="margin", x_label="Region", y_label="Margin", horizontal=True)

    discount_effect = (
        view.groupby("discount")
        .agg(orders=("order_id", "size"), margin_rate=("margin", "sum"))
        .assign(margin_rate=lambda d: d["margin_rate"] / view.groupby("discount")["revenue"].sum())
        .reset_index()
    )
    st.dataframe(
        discount_effect,
        hide_index=True,
        column_config={
            "discount": st.column_config.NumberColumn("Discount", format="percent"),
            "orders": st.column_config.NumberColumn("Orders", format="%d"),
            "margin_rate": st.column_config.ProgressColumn(
                "Margin rate", format="percent", min_value=0.0, max_value=0.5
            ),
        },
    )

with tab_rows:
    st.dataframe(
        view[["order_id", "order_date", "region", "segment", "channel", "units", "revenue", "margin"]],
        hide_index=True,
        column_config={
            "order_date": st.column_config.DateColumn("Date", format="MMM DD, YYYY"),
            "revenue": st.column_config.NumberColumn("Revenue", format="dollar"),
            "margin": st.column_config.NumberColumn("Margin", format="dollar"),
        },
    )
    # `download_button` needs the bytes up front, because there is no server
    # round trip when the user clicks it.
    st.download_button(
        "Download these rows as CSV",
        data=view.to_csv(index=False).encode(),
        file_name="orders_filtered.csv",
        mime="text/csv",
    )
