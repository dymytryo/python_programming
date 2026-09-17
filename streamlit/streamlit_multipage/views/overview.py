"""Overview page. Pages are plain scripts; they run top to bottom like any other."""

import streamlit as st

from data_access import load_orders

orders = load_orders()

st.title("Overview")
st.caption(f"Viewing as {st.session_state['role']}.")

by_month = (
    orders.set_index("order_date")[["revenue", "margin"]].resample("MS").sum().reset_index()
)

cols = st.columns(3)
cols[0].metric("Revenue", f"${orders['revenue'].sum():,.0f}", border=True)
cols[1].metric("Margin", f"${orders['margin'].sum():,.0f}", border=True)
cols[2].metric("Orders", f"{len(orders):,}", border=True)

st.line_chart(by_month, x="order_date", y=["revenue", "margin"], x_label="Month", y_label="USD")

st.page_link("views/orders.py", label="Open the order table", icon=":material/table:")
