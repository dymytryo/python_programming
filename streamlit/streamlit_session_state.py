"""Session state: the only per-user memory that survives a rerun.

`st.session_state` is a dict scoped to one browser session. Anything you put in
it is still there on the next rerun; everything else in the script is rebuilt.
Three facts drive most of the confusion around it:

1. A widget given `key="x"` writes its value to `st.session_state["x"]`, and
   reading or assigning that key is the same as reading or setting the widget.
2. Assigning to a widget's key after the widget has been created in the same
   run raises an error. Set the default before the widget, or set it inside a
   callback, which Streamlit runs before the rerun begins.
3. When a widget stops being rendered, Streamlit drops its key from session
   state. State that must outlive a hidden widget needs its own separate key.

Run it:

    streamlit run streamlit_session_state.py
"""

import streamlit as st

st.set_page_config(page_title="Session state", layout="centered")
st.title("Session state and callbacks")

# Seed defaults exactly once. `setdefault` is the safe form: on later reruns the
# key already exists and the current value is left alone.
st.session_state.setdefault("cart", [])
st.session_state.setdefault("log", [])

CATALOG = {"Starter seat": 12, "Growth seat": 28, "Enterprise seat": 55, "Onboarding": 1500}


def add_to_cart() -> None:
    """Callbacks run before the rerun, so they may write to widget keys.

    This is the only place you can reset `item_qty` without hitting the "cannot
    be modified after the widget is instantiated" error.
    """
    item = st.session_state["item_choice"]
    qty = st.session_state["item_qty"]
    st.session_state["cart"].append({"item": item, "qty": qty, "price": CATALOG[item]})
    st.session_state["log"].append(f"added {qty} x {item}")
    st.session_state["item_qty"] = 1  # legal here, illegal in the script body


def clear_cart() -> None:
    st.session_state["cart"] = []
    st.session_state["log"].append("cleared cart")


left, right = st.columns([2, 1])

with left:
    # `key=` is what binds these widgets to session state.
    st.selectbox("Item", list(CATALOG), key="item_choice")
    st.number_input("Quantity", min_value=1, max_value=100, value=1, step=1, key="item_qty")
    st.button("Add to cart", on_click=add_to_cart, type="primary")
    st.button("Clear cart", on_click=clear_cart)

with right:
    subtotal = sum(line["qty"] * line["price"] for line in st.session_state["cart"])
    st.metric("Lines", len(st.session_state["cart"]))
    st.metric("Subtotal", f"${subtotal:,.2f}")

if st.session_state["cart"]:
    st.dataframe(st.session_state["cart"], hide_index=True)
else:
    st.caption("Cart is empty.")

st.divider()

st.subheader("Forms batch a rerun")

# Without a form, every keystroke and every control change reruns the script.
# Inside a form, nothing reruns until the submit button is pressed, and the
# widget values are read as a single set.
with st.form("quote_form"):
    company = st.text_input("Company")
    seats = st.number_input("Seats", min_value=1, value=10)
    notes = st.text_area("Notes")
    submitted = st.form_submit_button("Submit quote")

if submitted:
    st.success(f"Quote recorded for {company or 'unnamed company'}: {seats} seats.")
    st.session_state["log"].append(f"quoted {company or 'unnamed'} for {seats} seats")
    if notes:
        st.caption(f"Notes: {notes}")

st.divider()

st.subheader("What is in session state right now")
st.write({k: v for k, v in st.session_state.items() if k != "log"})

with st.expander("Event log"):
    for entry in reversed(st.session_state["log"][-20:]):
        st.text(entry)
