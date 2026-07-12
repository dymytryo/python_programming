def split_dataframe_to_csv(df: pd.DataFrame, max_lines: int = 500, file_name: str = 'DataFrame_split',
                           header: bool = False) -> int:
    """
    Splits a DataFrame into multiple CSV files based on a maximum number of lines per file.

    This function will divide the input DataFrame into several subsets, each with a number of
    rows up to the specified maximum. Each subset is then saved as a CSV file with or without headers.
    It also provides a confirmation of successful operation and includes error handling.

    Args:
        df (pd.DataFrame): The DataFrame to be split and saved.
        max_lines (int): The maximum number of lines each CSV file should contain. Defaults to 500.
        file_name (str): The base name for the output CSV files. Defaults to 'DataFrame_split'.
        header (bool): Whether to write the header with column names to the CSV file. Defaults to False.

    Returns:
        int: The number of files generated.

    Raises:
        ValueError: If 'df' is not a DataFrame or 'max_lines' is not a positive integer.
        OSError: If there is an error in writing files to the disk.

    Examples:
        >>> split_dataframe_to_csv(upload_df, 500, 'my_data', '/path/to/directory/', header=True)
        # This will split `upload_df` into multiple CSV files with headers and save them to the specified directory.
    """
    # Validate inputs
    if not isinstance(df, pd.DataFrame):
        raise ValueError("The provided 'df' argument must be a pandas DataFrame.")
    
    if not isinstance(max_lines, int) or max_lines <= 0:
        raise ValueError("The provided 'max_lines' must be a positive integer.")

    try:
        # Calculate the number of files needed
        num_files = math.ceil(len(df) / max_lines)
        files_created = 0

        # Create and save each subset of the DataFrame as a CSV file
        for i in range(num_files):
            start_index = i * max_lines
            end_index = min((i + 1) * max_lines, len(df))  # Ensure the end index does not go beyond the DataFrame length

            # Generate the subset and convert to CSV
            subset = df[start_index:end_index]
            file_path = f"{file_name}_{i+1}.csv"
            subset.to_csv(file_path, index=False, header=header)
            files_created += 1

        print(f"Splitting complete. {files_created} files were generated.")

        return files_created

    except Exception as e:
        print(f"An error occurred: {e}")
        raise
      
# First, we will create a simple example DataFrame with 10 records.
example_df = pd.DataFrame({
    'Column1': range(10),
    'Column2': ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
})

# Test out the split
split_dataframe_to_csv(example_df, 1, 'example_split')
