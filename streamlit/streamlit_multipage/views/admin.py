"""Admin page. Only reachable when the role in the sidebar is `admin`.

Hiding a page from `st.navigation` removes it from the menu and from routing, so
this is real access control for an internal tool, not a cosmetic filter. It is
still not authentication: pair it with `st.user` and an identity provider, or
put the app behind one, before anything sensitive goes on the page.
"""

import streamlit as st

from data_access import load_orders

st.title("Admin")

orders = load_orders()
st.write("Cache and data controls.")

col_a, col_b = st.columns(2)
col_a.metric("Rows loaded", f"{len(orders):,}", border=True)
col_b.metric("Columns", len(orders.columns), border=True)

if st.button("Clear the data cache", type="primary"):
    load_orders.clear()
    st.toast("Cache cleared; the next page load re-reads the CSV.")

st.subheader("Session state")
st.write(dict(st.session_state))
