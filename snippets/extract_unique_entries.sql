def extract_unique_entries(df: pd.DataFrame, group_column: str) -> pd.DataFrame:
    """
    Extracts a subset of the DataFrame where groups in the specified column occur only once.

    Args:
        df (pd.DataFrame): The DataFrame to process.
        group_column (str): The name of the column containing group names.

    Returns:
        pd.DataFrame: A DataFrame containing only the rows where the group name appears once.

    Raises:
        ValueError: If the specified group_column does not exist in the DataFrame.
        TypeError: If the input is not a pandas DataFrame or the group_column is not a string.
    """
    if not isinstance(df, pd.DataFrame):
        raise TypeError("The input must be a pandas DataFrame.")
    
    if not isinstance(group_column, str):
        raise TypeError("The group_column must be a string.")

    if group_column not in df.columns:
        raise ValueError(f"The specified column '{group_column}' does not exist in the DataFrame.")

    # Count the occurrences of each group
    group_counts = df[group_column].value_counts()

    # Identify groups that occur only once
    single_entry_groups = group_counts[group_counts == 1].index

    # Extract subset of DataFrame with only unique entries
    return df[df[group_column].isin(single_entry_groups)]

# Example usage
sample_data = {'Group': ['A', 'B', 'C', 'A', 'D', 'E', 'B'],
               'Attribute': [1, 2, 3, 4, 5, 6, 7]}

sample_df = pd.DataFrame(sample_data)
unique_entry_subset = extract_unique_entries(sample_df, 'Group')
print(unique_entry_subset)
