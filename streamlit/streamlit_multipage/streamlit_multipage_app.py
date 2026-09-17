"""Multipage entrypoint: one script that declares the navigation.

Streamlit has two multipage mechanisms.

1. Put a `pages/` folder next to the entrypoint. Every `.py` file in it becomes
   a page, ordered and titled by filename. Zero configuration, no control.
2. Call `st.navigation([...])` with `st.Page` objects, as this file does. You
   choose the titles, icons, URLs, grouping, and which pages exist at all, so
   navigation can depend on who is signed in.

The second is the one to reach for in anything real. This folder uses `views/`
rather than `pages/` on purpose: a folder literally named `pages` is picked up
automatically, which would attach these pages to every other app in the parent
folder as well.

The entrypoint reruns on every interaction, so shared setup written here runs
before whichever page is active.

Run it from this folder:

    streamlit run streamlit_multipage_app.py
"""

import streamlit as st

st.set_page_config(page_title="Orders console", layout="wide")

# Anything set here is available to the page that runs next, because the page
# executes as part of this same rerun.
st.session_state.setdefault("role", "analyst")

with st.sidebar:
    st.session_state["role"] = st.radio("Signed in as", ["analyst", "admin"], horizontal=True)

reporting = [
    st.Page("views/overview.py", title="Overview", icon=":material/dashboard:", default=True),
    st.Page("views/orders.py", title="Orders", icon=":material/table:"),
]

# Navigation is just Python, so an admin-only page is an `if`, and a grouped
# menu is a dict of section name to pages.
if st.session_state["role"] == "admin":
    nav = st.navigation({"Reporting": reporting, "Internal": [st.Page("views/admin.py", title="Admin", icon=":material/settings:")]})
else:
    nav = st.navigation(reporting)

nav.run()
