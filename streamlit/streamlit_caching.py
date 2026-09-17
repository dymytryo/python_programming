"""Caching: how to stop the rerun model from redoing expensive work.

Because every interaction re-executes the script, an unguarded query or file
read runs again on every click. The two cache decorators fix that, and they are
not interchangeable:

    @st.cache_data      for the RESULT of a computation: dataframes, dicts,
                        API responses. The value is serialized, and each caller
                        gets its own copy, so one session mutating the result
                        cannot corrupt another session's.

    @st.cache_resource  for the HANDLE to something: a database connection, a
                        loaded model, a client object. Nothing is serialized and
                        every caller gets the same object, which is the point,
                        because a connection pool must be shared.

Both caches live in the server process, not the session, so an entry written by
one user is served to the next. Both are keyed on the function's qualified name
plus a hash of its arguments. An argument that cannot be hashed raises an error
unless you prefix its name with an underscore, which excludes it from the key.

Do not write to `st.session_state` inside a cached function. The write is
discarded, which is why the execution counters below live in a
`@st.cache_resource` object instead.

Run it:

    streamlit run streamlit_caching.py
"""

import time
from pathlib import Path

import pandas as pd
import streamlit as st

DATA = Path(__file__).parent / "data" / "orders.csv"

st.set_page_config(page_title="Caching", layout="wide")
st.title("cache_data and cache_resource")


@st.cache_resource
def execution_counter() -> dict:
    """One mutable dict for the whole process, created on first use.

    A real version of this returns `snowflake.connector.connect(...)` or
    `boto3.client("s3")`. The pattern is the same: build the object once, hand
    the same reference to everyone, never copy it.
    """
    return {"created_at": time.strftime("%H:%M:%S"), "uncached": 0, "cached": 0}


def load_orders_uncached() -> pd.DataFrame:
    execution_counter()["uncached"] += 1
    time.sleep(0.4)  # stands in for a slow query
    return pd.read_csv(DATA, parse_dates=["order_date"])


@st.cache_data(ttl="10m", show_spinner="Loading orders...")
def load_orders(path: str) -> pd.DataFrame:
    """Cached on `path`. The body runs only on a miss."""
    execution_counter()["cached"] += 1
    time.sleep(0.4)
    return pd.read_csv(path, parse_dates=["order_date"])


counts = execution_counter()

region = st.selectbox(
    "Region filter (changing this triggers a rerun)",
    ["All", "West", "Midwest", "Northeast", "South"],
)

col_a, col_b = st.columns(2)

with col_a:
    st.subheader("Without a cache")
    start = time.perf_counter()
    uncached = load_orders_uncached()
    st.write(f"Took **{time.perf_counter() - start:.2f}s**")
    st.write(f"Function body executed **{counts['uncached']}** times")

with col_b:
    st.subheader("With @st.cache_data")
    start = time.perf_counter()
    orders = load_orders(str(DATA))
    st.write(f"Took **{time.perf_counter() - start:.2f}s**")
    st.write(f"Function body executed **{counts['cached']}** times")

st.caption(
    "Change the region filter a few times. The uncached count climbs on every "
    "rerun; the cached count stays at 1, because the argument did not change."
)

st.divider()

if region != "All":
    orders = orders[orders["region"] == region]
st.write(f"{len(orders):,} orders after filtering.")

# The cached frame is a copy, so mutating it here is safe. Doing the same to a
# @st.cache_resource value would change what every other session sees.
orders = orders.assign(margin=orders["revenue"] - orders["cost"])
st.dataframe(orders.head(20), hide_index=True)

st.divider()

st.subheader("The shared resource behind those counters")
st.write(f"Created at **{counts['created_at']}**, and it is the same dict for every session.")
st.caption(
    "Open this app in a second browser tab. The creation time does not change "
    "and the counts keep climbing, because both sessions hold one object."
)

cols = st.columns(2)
if cols[0].button("Clear the data cache"):
    load_orders.clear()  # or st.cache_data.clear() for every cached function
    counts["cached"] = 0
    st.rerun()
if cols[1].button("Clear the resource cache"):
    execution_counter.clear()  # the next call builds a new dict, new timestamp
    st.rerun()
