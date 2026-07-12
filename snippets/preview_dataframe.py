def preview_dataframe(df: pd.DataFrame) -> None:
    """
    Temporarily sets the display options to show the entire DataFrame and then resets them back to default.

    This function is useful for inspecting the full content of a DataFrame without permanently altering the global display settings.

    Args:
        df (pd.DataFrame): The DataFrame to be previewed.

    Raises:
        TypeError: If the input argument is not a pandas DataFrame.

    Example:
        >>> data = pd.DataFrame({'A': range(5), 'B': range(5, 10)})
        >>> preview_dataframe(data)
    """
    if not isinstance(df, pd.DataFrame):
        raise TypeError("The input argument must be a pandas DataFrame.")

    try:
        pd.options.display.max_rows = None
        pd.options.display.max_columns = None
        pd.options.display.max_colwidth = None
        display(df.head(10))
    finally:
        # Reset the options in the 'finally' block to ensure they are reset even if an error occurs
        pd.reset_option('display.max_rows')
        pd.reset_option('display.max_columns')
        pd.reset_option('display.max_colwidth')
    
