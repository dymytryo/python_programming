# Streamlit

Streamlit turns a Python script into a web application. There is no callback
graph, no component tree to declare, and no separate front end: you write a
script top to bottom, and every `st.*` call appends an element to the page. The
server runs the script, sends the resulting element tree to the browser, and the
browser patches whatever changed.

The cost of that simplicity is one rule that governs everything else: **the whole
script re-executes on every interaction.** Learn that rule and the rest of the
interface follows from it.

## Run the demos

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

streamlit run streamlit_hello_app.py
```

The command starts a local server on `http://localhost:8501` and opens a browser
tab. Edit the file and save: Streamlit detects the change and offers to rerun.
Stop the server with `Ctrl+C`.

Useful flags:

```bash
streamlit run app.py --server.port 8600          # a different port
streamlit run app.py --server.headless true      # do not open a browser
streamlit run app.py -- --my-arg value           # args after -- go to your script
streamlit config show                            # every setting and its default
streamlit cache clear                            # wipe the on-disk cache
streamlit hello                                  # the built-in demo app
streamlit init my_app                            # scaffold streamlit_app.py + requirements.txt
```

## Files in this folder

Each file runs on its own and demonstrates one idea. `data/orders.csv` is 2,400
rows of fabricated sales orders, rebuilt deterministically by its generator.

| File | What it shows |
| --- | --- |
| `streamlit_hello_app.py` | The rerun model, widgets as values, sidebar, columns, tabs |
| `streamlit_caching.py` | `@st.cache_data` against `@st.cache_resource`, cache clearing |
| `streamlit_session_state.py` | State across reruns, widget keys, callbacks, forms |
| `streamlit_fragment_rerun.py` | `@st.fragment`, rerunning part of a page |
| `streamlit_orders_dashboard.py` | Filters, metrics, charts, column config, CSV download |
| `streamlit_multipage/streamlit_multipage_app.py` | `st.navigation` and `st.Page`, shared loaders, conditional pages |
| `data/generate_orders.py` | Regenerates `orders.csv` |

## How it works

A Streamlit session is a websocket connection between one browser tab and the
server. When a widget changes, the browser does not ask for a partial update. It
sends the new widget value and asks the server to run the script again.

```
User moves a slider
        |
        v
Browser sends the widget's new value over the websocket
        |
        v
Server re-executes the ENTIRE script, top to bottom
        |
        +-- st.slider(...) returns the new value instead of the default
        +-- @st.cache_data functions return stored results without running
        +-- st.session_state still holds whatever you put in it
        +-- every other variable is created from scratch
        |
        v
Server sends the new element tree back
        |
        v
Browser diffs it against the screen and patches only what differs
```

Two consequences are worth stating plainly.

**There is no event handler.** `st.slider(...)` both draws the slider and returns
its current value. Code that reacts to the slider is simply the code after it.

**Slow code runs again on every click** unless you cache it. An uncached
`pd.read_csv` at the top of a script re-reads the file each time the user types a
character into a text box.

## What survives a rerun

| Thing | Survives a rerun | Scope | Notes |
| --- | --- | --- | --- |
| Local variables | No | - | Rebuilt every run |
| Globals in the main script | No | - | The entrypoint is re-executed into a fresh module each run |
| Globals in an imported module | Yes | Whole server process | Python imports it once; every session shares it, which makes it unsafe for per-user data |
| Widget values | Yes | One session | Held by widget identity, see below |
| `st.session_state` | Yes | One session | Cleared when the browser tab is refreshed or closed |
| `@st.cache_data` | Yes | Whole server process | Each caller gets a copy of the value |
| `@st.cache_resource` | Yes | Whole server process | Every caller gets the same object |

"One session" means one browser tab. Two tabs on the same app are two sessions
with separate session state and separate widget values, but they share both
caches and any imported module's globals.

## Widgets

A widget call renders a control and returns its current value:

```python
seats = st.slider("Seats", min_value=1, max_value=500, value=25)
plan = st.selectbox("Plan", ["Starter", "Growth", "Enterprise"])
```

Streamlit tracks a widget by an identity derived from its type and its
parameters, including the label. Two widgets whose parameters are identical
collide, which surfaces as a duplicate-element error. Give a widget an explicit
`key` to fix that, and to bind it to session state:

```python
st.number_input("Quantity", min_value=1, value=1, key="item_qty")
st.session_state["item_qty"]   # the same value the widget returned
```

Widget state is tied to the widget being on the page. If a widget stops being
rendered, its key survives exactly one more rerun and is then dropped; when the
widget comes back it is back at its default. Anything that must outlive the
widget needs its own key in session state.

Interactive elements also include `st.button`, `st.form_submit_button`,
`st.file_uploader`, `st.date_input`, `st.multiselect`, `st.segmented_control`,
`st.pills`, `st.data_editor`, and `st.chat_input`. `st.button` returns `True` only
on the run that immediately follows the click, so a button is a one-shot signal,
not a state you can read later.

## Caching

Two decorators, split by what you are caching.

```python
@st.cache_data                     # the RESULT: dataframes, dicts, API responses
def load_orders(path: str) -> pd.DataFrame:
    return pd.read_csv(path)

@st.cache_resource                 # the HANDLE: connections, clients, models
def get_connection():
    return snowflake.connector.connect(**st.secrets["snowflake"])
```

`cache_data` serializes the return value and hands each caller its own copy, so
one session mutating the dataframe cannot corrupt another's. `cache_resource`
stores the object itself and hands out the same reference, which is required for
a connection pool and dangerous for anything a session will mutate.

Both are keyed on the function's qualified name plus a hash of its arguments.
An unhashable argument raises an error; prefix its name with an underscore
(`_conn`) to leave it out of the key.

Common options and operations:

```python
@st.cache_data(ttl="10m", max_entries=20, show_spinner="Loading orders...")
def load_orders(path: str) -> pd.DataFrame:
    ...

load_orders.clear()     # drop this function's entries
st.cache_data.clear()   # drop every cached function's entries
```

Two rules that cause real bugs:

- Do not call `st.*` display functions inside a cached function unless you want
  the output replayed from cache along with the value.
- Do not write to `st.session_state` inside a cached function. The write is
  discarded. Keep a counter or a flag outside the cached body.

`streamlit_caching.py` demonstrates both decorators side by side with an
execution counter, so a cache hit is visible rather than asserted.

## Session state

`st.session_state` is a dict scoped to one browser session, and it is the only
per-user memory that a rerun does not destroy.

```python
st.session_state.setdefault("cart", [])      # seed once, leave later runs alone
st.session_state["cart"].append(line)
```

Setting a widget's key from the script body after the widget has been created
raises an error. Callbacks are the exception, because Streamlit runs them before
the rerun begins:

```python
def add_to_cart() -> None:
    st.session_state["cart"].append(st.session_state["item_choice"])
    st.session_state["item_qty"] = 1          # legal in a callback

st.button("Add to cart", on_click=add_to_cart)
```

Every widget takes `on_change` or `on_click` plus `args` and `kwargs`. The
callback runs, then the script reruns, so the script body always sees the state
the callback left behind.

## Limiting how much reruns

By default one keystroke reruns the whole script. Two tools narrow that.

**Forms** batch several widgets into one rerun. Nothing inside a form triggers a
rerun until the submit button is pressed, and the values are read as one set.

```python
with st.form("quote_form"):
    company = st.text_input("Company")
    seats = st.number_input("Seats", min_value=1, value=10)
    submitted = st.form_submit_button("Submit quote")

if submitted:
    ...
```

**Fragments** narrow the rerun to one function. A widget inside a
`@st.fragment` reruns only that function, leaving the rest of the script alone.

```python
@st.fragment
def region_explorer(df):
    region = st.selectbox("Region", sorted(df["region"].unique()))
    st.line_chart(df[df["region"] == region] ...)
```

A fragment cannot see writes the main script would make after it, so pass what it
needs as arguments or keep shared values in session state. `st.rerun(scope="fragment")`
reruns just the fragment; `run_every="2s"` reruns it on a timer with no user
interaction, which is how live dashboards refresh.

Two more flow-control calls:

- `st.stop()` ends the current run at that line, leaving everything already drawn
  on screen. Useful for an early exit when filters match nothing.
- `st.rerun()` restarts the script immediately, typically after a callback-free
  state change.

## Layout and output

Layout calls return containers, and writing into a container places the element
where the container sits regardless of where you are in the script.

```python
left, right = st.columns([2, 1])
left.metric("Revenue", "$5.9M")
with st.sidebar:
    st.header("Filters")
tab_trend, tab_rows = st.tabs(["Trend", "Rows"])
with st.container(border=True):
    st.write("boxed")
with st.expander("Details"):
    st.write("collapsed by default")
```

For output, `st.write` accepts almost anything and picks a renderer. Where the
type is known, the specific call gives more control: `st.dataframe` for tables,
`st.data_editor` for editable tables, `st.metric` for a single number,
`st.line_chart`, `st.bar_chart`, `st.area_chart`, and `st.map` for quick charts,
and `st.altair_chart`, `st.plotly_chart`, or `st.pyplot` when a chart needs real
configuration.

`st.dataframe` takes a `column_config` that controls formatting without touching
the data:

```python
st.dataframe(
    view,
    hide_index=True,
    column_config={
        "order_date": st.column_config.DateColumn("Date", format="MMM DD, YYYY"),
        "revenue": st.column_config.NumberColumn("Revenue", format="dollar"),
        "margin_rate": st.column_config.ProgressColumn("Margin rate", format="percent",
                                                       min_value=0.0, max_value=0.5),
    },
)
```

`st.download_button` needs its bytes up front, because the click does not make a
server round trip:

```python
st.download_button("Download CSV", data=view.to_csv(index=False).encode(),
                   file_name="orders.csv", mime="text/csv")
```

## Multipage applications

Two mechanisms exist.

1. A folder named `pages/` next to the entrypoint. Every `.py` file in it becomes
   a page, titled and ordered by filename. No configuration and no control. Note
   that the folder name is magic: any app run from the parent folder picks it up.
2. `st.navigation` with `st.Page` objects, which is the one to use for anything
   real.

```python
reporting = [
    st.Page("views/overview.py", title="Overview", icon=":material/dashboard:", default=True),
    st.Page("views/orders.py", title="Orders", icon=":material/table:"),
]
if st.session_state["role"] == "admin":
    nav = st.navigation({"Reporting": reporting, "Internal": [st.Page("views/admin.py")]})
else:
    nav = st.navigation(reporting)
nav.run()
```

Navigation is ordinary Python, so an admin-only page is an `if`, and a grouped
menu is a dict of section name to pages. `st.Page` also takes a callable instead
of a path, and `url_path` controls the address.

The entrypoint reruns on every interaction and then executes the active page, so
shared setup written in the entrypoint runs before the page every time.

One trap: **pages must not import the entrypoint.** Streamlit runs the entrypoint
as `__main__`, so importing it by name executes a second copy, which calls
`st.navigation` again and recurses. Put shared loaders in a plain module and
import that from both. Streamlit inserts the entrypoint's folder into `sys.path`,
so a sibling module imports by bare name from any page.

## Configuration and secrets

Settings live in `.streamlit/config.toml`, either beside the app or in
`~/.streamlit/`. Every key is also a command-line flag and an environment
variable (`STREAMLIT_SERVER_PORT`).

```toml
# .streamlit/config.toml
[server]
port = 8501
maxUploadSize = 50

[theme]
base = "light"
primaryColor = "#B4441E"
```

Credentials live in `.streamlit/secrets.toml`, which must be gitignored, and are
read through `st.secrets`:

```toml
# .streamlit/secrets.toml
[snowflake]
account = "abc12345"
user = "svc_dashboard"
password = "..."
```

```python
conn = st.connection("snowflake")          # reads [connections.snowflake]
df = conn.query("select * from orders limit 100", ttl="10m")
```

`st.connection` wraps the connection in `cache_resource` and the query results in
`cache_data`, which is the correct split and saves writing it yourself. It ships
with SQL (any SQLAlchemy target) and Snowflake connectors.

## Deployment

A Streamlit app is a long-running server process, not a set of request handlers,
so it is deployed like a service:

```bash
streamlit run app.py --server.port 8080 --server.address 0.0.0.0 --server.headless true
```

The three practical options are Streamlit Community Cloud (point it at a public
GitHub repository with a `requirements.txt`), a container behind a reverse proxy,
or a managed platform such as Snowflake's Streamlit in Snowflake or a cloud run
service. Whichever you pick, remember what is shared: both caches and every
imported module's globals are per process, so anything user-specific belongs in
session state, and scaling to multiple replicas means each replica warms its own
cache.

Streamlit has no built-in authentication for self-hosted deployments beyond
`st.login` with an OpenID Connect (OIDC) provider. Hiding a page from
`st.navigation` removes it from routing, which is adequate for an internal tool,
but anything sensitive belongs behind a real identity provider.
