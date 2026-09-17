"""The rerun model: what happens to your script every time a widget changes.

Streamlit has no callback-driven view layer. Every interaction re-executes this
entire file from the first line to the last, and the value a widget function
returns is whatever the user last set it to. This app makes that visible by
printing a counter that increments on every rerun, using the one variable that
is allowed to survive: `st.session_state`.

Run it:

    streamlit run streamlit_hello_app.py
"""

import time

import streamlit as st

st.set_page_config(page_title="Rerun model", layout="centered")

# `run_count` lives in session state, so it is the only thing on this page that
# is not rebuilt from scratch on each rerun.
st.session_state.setdefault("run_count", 0)
st.session_state["run_count"] += 1

# A module-level variable, by contrast, is reassigned every single run.
script_started_at = time.strftime("%H:%M:%S")

st.title("Every interaction reruns the whole script")

st.metric("Times this script has executed", st.session_state["run_count"])
st.caption(f"This run started at {script_started_at}.")

st.divider()

st.subheader("Widgets return values, they do not fire callbacks")

# Each widget call does two things at once: it renders the control, and it
# returns that control's current value. On the first run it returns the default;
# on every later run it returns what the user set.
name = st.text_input("Customer name", value="Acme Logistics")
seats = st.slider("Seats", min_value=1, max_value=500, value=25)
plan = st.selectbox("Plan", ["Starter", "Growth", "Enterprise"])
annual = st.checkbox("Bill annually", value=True)

unit_price = {"Starter": 12, "Growth": 28, "Enterprise": 55}[plan]
months = 12 if annual else 1
discount = 0.15 if annual else 0.0
total = seats * unit_price * months * (1 - discount)

st.write(f"**{name}** on {plan}: {seats} seats at ${unit_price} per month")
st.write(f"Billed amount: **${total:,.2f}**")

st.info(
    "Move any control above and watch the run counter climb. The script did not "
    "patch one widget, it ran again from the top and rebuilt the page."
)

st.divider()

st.subheader("Layout containers")

# Layout calls return container objects. Writing into a container places the
# element where the container sits, no matter where in the script you are.
left, right = st.columns(2)
left.metric("Monthly", f"${seats * unit_price:,.0f}")
right.metric("Contract", f"${total:,.0f}", delta=f"-{discount:.0%}" if discount else None)

with st.sidebar:
    st.header("Sidebar")
    st.write("The sidebar is just another container.")
    st.write(f"Current plan: {plan}")

tab_summary, tab_detail = st.tabs(["Summary", "Detail"])
with tab_summary:
    st.write(f"{seats} seats, billed {'annually' if annual else 'monthly'}.")
with tab_detail:
    st.json(
        {
            "customer": name,
            "plan": plan,
            "seats": seats,
            "unit_price": unit_price,
            "months": months,
            "discount": discount,
            "total": round(total, 2),
        }
    )

with st.expander("Why the counter never resets"):
    st.write(
        "Refreshing the browser starts a new session and clears session state, "
        "so the counter goes back to 1. Interacting with a widget does not."
    )
