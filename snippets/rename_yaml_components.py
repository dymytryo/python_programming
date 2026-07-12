# pip install pyyaml
# When migration off of dbt 1.7, the `tests` keyword was changed to `data_tests`. 
import os
import yaml
import logging

DBT_PROJECT_DIR = "/Users/dvaliaiev/PycharmProjects/dbt/" 
LOG_FILE = "schema_update.log"

# Setup basic logging
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    filemode="w",  # Overwrite log file each run
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def rename_tests_key_in_dict(obj):
    """
    Recursively rename 'tests' -> 'data_tests' keys in a nested Python object.
    """
    if isinstance(obj, dict):
        # If this dict has a 'tests' key, rename it to 'data_tests'
        if "tests" in obj:
            obj["data_tests"] = obj.pop("tests")
            logging.info("  Renamed 'tests' key to 'data_tests'")
        
        # Recursively process all values
        for key, value in obj.items():
            rename_tests_key_in_dict(value)

    elif isinstance(obj, list):
        # Recursively process each item in a list
        for item in obj:
            rename_tests_key_in_dict(item)

def process_schema_file(file_path):
    """
    Load a schema file as YAML, rename 'tests' to 'data_tests', and rewrite if changes are made.
    Logs the status of the update.
    """
    with open(file_path, "r") as f:
        try:
            data = yaml.safe_load(f)
        except yaml.YAMLError as e:
            logging.error(f"  YAML parsing error in file: {file_path}\n  {e}")
            return
    
    if data is None:
        # File may be empty or only contain comments
        logging.info(f"No YAML data found in {file_path}. Skipping.")
        return

    # Store original data for comparison
    old_data_str = yaml.safe_dump(data, sort_keys=False)
    
    # Perform the rename
    rename_tests_key_in_dict(data)

    # Dump updated data
    new_data_str = yaml.safe_dump(data, sort_keys=False)

    # Compare old vs new; if changed, overwrite file
    if old_data_str != new_data_str:
        with open(file_path, "w") as f:
            f.write(new_data_str)
        logging.info(f"Updated file: {file_path}")
    else:
        logging.info(f"No changes needed for file: {file_path}")

def main():
    """
    Walk through the dbt project directory, process any schema.yml or _schema.yml files.
    """
    logging.info("Starting DBT schema files update...")
    for root, dirs, files in os.walk(DBT_PROJECT_DIR):
        for file_name in files:
            if file_name.endswith("schema.yml"):
                file_path = os.path.join(root, file_name)
                logging.info(f"Processing file: {file_path}")
                process_schema_file(file_path)
    logging.info("DBT schema files update complete.")
