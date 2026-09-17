"""Fragments: rerunning one part of the page instead of the whole script.

A function decorated with `@st.fragment` becomes its own rerun boundary. When a
widget inside the fragment changes, only the fragment function re-executes; the
rest of the script does not. That turns a slow page into a responsive one when
the expensive work sits outside the interactive part.

The rules worth knowing:

- Elements a fragment draws are confined to the container it is called in.
- A fragment rerun cannot see writes the main script would have made after it.
  Pass what it needs as arguments, or keep shared values in session state.
- `st.rerun(scope="fragment")` reruns just the fragment; the default
  `scope="app"` reruns everything.
- `run_every="2s"` makes a fragment poll on a timer with no user interaction,
  which is how live dashboards are built.

Run it:

    streamlit run streamlit_fragment_rerun.py
"""

import time
from pathlib import Path

import pandas as pd
import streamlit as st

DATA = Path(__file__).parent / "data" / "orders.csv"

st.set_page_config(page_title="Fragments", layout="wide")
st.title("Partial reruns with st.fragment")

st.session_state.setdefault("full_runs", 0)
st.session_state.setdefault("fragment_runs", 0)
st.session_state["full_runs"] += 1


@st.cache_data
def load_orders() -> pd.DataFrame:
    time.sleep(1.0)  # the expensive step this page is trying not to repeat
    return pd.read_csv(DATA, parse_dates=["order_date"])


orders = load_orders()

top = st.columns(2)
top[0].metric("Full script runs", st.session_state["full_runs"])
top[1].metric("Fragment-only runs", st.session_state["fragment_runs"])


@st.fragment
def region_explorer(df: pd.DataFrame) -> None:
    """Interactions inside this function do not rerun the script above it."""
    st.session_state["fragment_runs"] += 1

    region = st.selectbox("Region", sorted(df["region"].unique()))
    channel = st.multiselect("Channel", sorted(df["channel"].unique()), default=list(df["channel"].unique()))

    view = df[(df["region"] == region) & (df["channel"].isin(channel))]
    st.write(f"{len(view):,} orders, ${view['revenue'].sum():,.0f} revenue")

    by_month = (
        view.set_index("order_date")["revenue"].resample("MS").sum().rename("revenue").reset_index()
    )
    st.line_chart(by_month, x="order_date", y="revenue")


with st.container(border=True):
    st.subheader("Fragment")
    region_explorer(orders)

st.caption(
    "Change the region or channel above: the fragment counter climbs and the "
    "full-run counter does not. The one-second load never repeats."
)

st.divider()

st.subheader("Full-script control")
if st.button("Rerun the whole app"):
    st.rerun()  # scope="app" is the default
