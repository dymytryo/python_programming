# Python Programming

Learning notes, notebooks, and practical Python utilities.

## Contents

- Introductory programming notes and notebooks.
- [`lectures/`](lectures/README.md): lecture notebooks for teaching introductory
  Python, one per chapter, with concepts in dependency order, a runnable cell after
  every idea, and a working program at the end.
- [`software_development/`](software_development/README.md): maintainable Python
  software, including resource cleanup, exceptions, object-oriented design, imports,
  environments, packaging, testing, profiling, pandas, and web APIs.
- [`streamlit/`](streamlit/README.md): how Streamlit's rerun model, caching,
  session state, and multipage routing work, with six runnable demo apps over a
  bundled synthetic dataset.
- `snippets/`: reusable Python/data engineering helpers moved from the
  former `python_snippets` workspace.

## Snippet Highlights

- `snippets/clean_public_domains.py` and
  `snippets/public_email_domains.csv`: identify and remove public/free email
  domains from contact datasets.
- `snippets/cross_cluster_df.py`: cluster connected entities across two ID
  columns with NetworkX.
- `snippets/clean_yml.py` and `snippets/rename_yaml_components.py`: dbt/YAML
  maintenance helpers.
