def clean_public_domains(df, email_col_name, public_domain_file='public_email_domains.csv'):
    """
    Drop rows with public email domains and provide a summary of the cleaning.

    Args:
        df (pd.DataFrame): The dataframe containing the email addresses.
        email_col_name (str): Name of the column containing email addresses.
        public_domain_file (str): Path to the CSV file with the list of public domains.

    Returns:
        pd.DataFrame: A cleaned dataframe with rows containing public domains dropped.
    """

    # Load the public domain list from the CSV file
    free_email_providers = pd.read_csv(public_domain_file)

    # Always extract domain from the email column
    df['domain'] = df[email_col_name].str.split('@').str[1]

    # Filter and count the occurrences of each domain in the dataframe
    public_domain_counts = df[df['domain'].isin(free_email_providers['public_email_domain'])]['domain'].value_counts()

    # Print summary
    total_emails = len(df)
    total_public_domains = len(public_domain_counts)
    print(f"Total email addresses: {total_emails}")
    print(f"Number of public domain types found: {total_public_domains}")
    print(f"Total public domain emails: {public_domain_counts.sum()}")
    print("\nCounts for each public domain:")
    print(public_domain_counts)

    # Drop rows with public domains
    cleaned_df = df[~df['domain'].isin(free_email_providers['public_email_domain'])].drop(columns=['domain'])

    return cleaned_df