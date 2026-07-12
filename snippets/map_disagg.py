import pandas as pd
from typing import List, Any

def map_disagg(df: DataFrame, column_name: str) -> DataFrame:
    """
    This function's goal is to undo Presto SQL MAP_AGG function in output written into Pandas dataframe. 
    Dynamically expands a column in a DataFrame that contains dictionaries into multiple new columns,
    based on the maximum number of key-value pairs in any dictionary in the column. 
    Each row's dictionary will be expanded into 'key_i' and 'value_i' columns, where 'i' is the pair index.

    Args:
        df (DataFrame): The DataFrame containing the column to expand.
        column_name (str): The name of the column to expand.

    Returns:
        DataFrame: A new DataFrame with the original data and the dynamically created columns.

    Raises:
        ValueError: If the specified column is not found in the DataFrame.

    Example:
        >>> data = {'map_agg': [{'a': '1', 'b': '2'}, {'c': '3', 'd': '4', 'e': '5'}]}
        >>> df = pd.DataFrame(data)
        >>> new_df = expand_map_column_dynamic(df, 'map_agg')
        >>> print(new_df)
    """
    if column_name not in df.columns:
        raise ValueError(f"Column '{column_name}' not found in DataFrame.")

    # Determine the maximum number of key-value pairs in any row
    max_pairs = df[column_name].apply(lambda x: len(x)).max()

    # Function to extract keys and values based on the maximum number of pairs
    def extract_keys_values(row: dict) -> List[Any]:
        pairs = [row.get(key) for key in sorted(row.keys())] + [None] * (max_pairs - len(row))
        keys_values = [item for pair in zip(sorted(row.keys()), pairs) for item in pair]
        return keys_values + [None] * (2 * max_pairs - len(keys_values))

    # Create new columns based on the maximum number of key-value pairs
    column_labels = [f"{kind}{i}" for i in range(1, max_pairs + 1) for kind in ["key", "value"]]
    df[column_labels] = df[column_name].apply(extract_keys_values).tolist()

    return df.drop(column_name, axis=1)

# Example usage
data = {'map_agg': [{'love': '46032', 'hope': '271177'}, {'faith': '12345', 'love': '67890', 'hope': '55555'}]}
df = pd.DataFrame(data)

new_df = expand_map_column_dynamic(df, 'map_agg')
new_df

def test_map_disagg():
    """
    Tests the expand_map_column_dynamic function for various scenarios.

    Raises:
        AssertionError: If any of the test conditions fail.
    """

    # Test data setup
    data = {
        'map_agg': [
            {'a': '1', 'b': '2'},
            {'c': '3', 'd': '4', 'e': '5'},
            {'f': '6'}
        ]
    }
    df = pd.DataFrame(data)

    # Test case 1: Correct column expansion
    expanded_df = expand_map_column_dynamic(df, 'map_agg')
    assert 'key1' in expanded_df and 'value1' in expanded_df, "Column 'key1' or 'value1' not found"
    assert 'key3' in expanded_df and 'value3' in expanded_df, "Column 'key3' or 'value3' not found"
    assert expanded_df['key3'].isnull().values.any(), "Missing values not handled correctly"

    # Test case 2: Handling missing values
    assert expanded_df.iloc[0]['key3'] is None and expanded_df.iloc[0]['value3'] is None, "Missing values not filled with None"
    assert expanded_df.iloc[2]['key2'] is None and expanded_df.iloc[2]['value2'] is None, "Missing values not filled with None"

    # Test case 3: Raising ValueError for non-existent column
    try:
        expand_map_column_dynamic(df, 'non_existent_column')
        assert False, "ValueError not raised for non-existent column"
    except ValueError:
        pass

    print("All tests passed!")


test_map_disagg()
