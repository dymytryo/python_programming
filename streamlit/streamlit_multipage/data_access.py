"""Shared loaders for the multipage app.

Pages must not import the entrypoint. Streamlit runs the entrypoint as
`__main__`, so importing it by name executes a second copy of the module, which
calls `st.navigation` again and recurses. Shared code belongs in a plain module
like this one, which both the entrypoint and every page can import.

Streamlit puts the entrypoint's folder on `sys.path`, so `import data_access`
resolves from `views/overview.py` without any package plumbing.
"""

from pathlib import Path

import pandas as pd
import streamlit as st

DATA = Path(__file__).parents[1] / "data" / "orders.csv"


@st.cache_data
def load_orders() -> pd.DataFrame:
    """Read once per process. Every page and every session shares the result."""
    df = pd.read_csv(DATA, parse_dates=["order_date"])
    df["margin"] = df["revenue"] - df["cost"]
    return df
