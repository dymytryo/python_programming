"""Orders page. Filters here are local to the page; shared state goes in session state."""

import streamlit as st

from data_access import load_orders

orders = load_orders()

st.title("Orders")

segment = st.segmented_control("Segment", sorted(orders["segment"].unique()), selection_mode="multi")
view = orders[orders["segment"].isin(segment)] if segment else orders

st.write(f"{len(view):,} orders")
st.dataframe(
    view[["order_id", "order_date", "region", "segment", "channel", "units", "revenue", "margin"]],
    hide_index=True,
    column_config={
        "order_date": st.column_config.DateColumn("Date", format="MMM DD, YYYY"),
        "revenue": st.column_config.NumberColumn("Revenue", format="dollar"),
        "margin": st.column_config.NumberColumn("Margin", format="dollar"),
    },
)
