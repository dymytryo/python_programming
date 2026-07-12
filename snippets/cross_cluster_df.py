import pandas as pd
import networkx as nx

def cross_cluster(dataframe: pd.DataFrame, column_a: str, column_b: str, additional_columns: list) -> pd.DataFrame:
    """
    Create clusters based on the connections between two types of entities in a given DataFrame.
    Additionally, aggregates information from additional columns specified.

    Args:
        dataframe (pd.DataFrame): The DataFrame containing the relationship data.
        column_a (str): The name of the first column representing the first entity.
        column_b (str): The name of the second column representing the second entity.
        additional_columns (list): List of names of additional columns to be aggregated.

    Returns:
        pd.DataFrame: A DataFrame where each row represents a cluster with two lists of entity IDs from each column.
        Additionally, includes aggregated data from specified additional columns.

    Raises:
        ValueError: If the specified columns are not found in the DataFrame.

    Example:
        >>> df = pd.DataFrame({'employeeId': ['E1', 'E2', 'E2'], 'departmentId': ['D5', 'D5', 'D6']})
        >>> cross_cluster(df, 'employeeId', 'departmentId', [])
    """
    # Check if specified columns are in the dataframe
    if column_a not in dataframe.columns or column_b not in dataframe.columns or any(col not in dataframe.columns for col in additional_columns):
        raise ValueError("One or more specified columns not found in the DataFrame")

    # Initialize a graph to represent connections
    G = nx.Graph()

    # Initialize a dictionary to hold additional information
    additional_info = {col: {} for col in additional_columns}

    # Iterate over each row in the dataframe
    for _, row in dataframe.iterrows():
        # Extract entity IDs
        entity_a_id = str(row[column_a])
        entity_b_id = str(row[column_b])

        # Create nodes for graph based on entities
        entity_a_node = f'a{entity_a_id}'
        entity_b_node = f'b{entity_b_id}'
        G.add_edge(entity_a_node, entity_b_node)  # Add an edge between these entities in the graph

        # Store additional data with both entity_a_id and entity_b_id as keys
        for col in additional_columns:
            if (entity_a_id, entity_b_id) not in additional_info[col]:
                # Initialize as a list with the first element
                additional_info[col][(entity_a_id, entity_b_id)] = [row[col]]
            else:
                # Append to the existing list for duplicates
                additional_info[col][(entity_a_id, entity_b_id)].append(row[col])

    # Find connected components in the graph, each representing a cluster
    connected_components = list(nx.connected_components(G))
    clusters = []

    # Process each connected component to form a cluster
    for component in connected_components:
        # Extract entities of type A and B from the component
        entities_a = {n[1:] for n in component if n.startswith('a')}
        entities_b = {n[1:] for n in component if n.startswith('b')}

        # Initialize a dictionary to represent the cluster
        cluster = {
            f'{column_a}s': list(entities_a),
            f'{column_b}s': list(entities_b)
        }

        # Aggregate additional column data
        for col in additional_columns:
            col_data = []
            # Iterate through all pairs of entity A and B
            for a_id in entities_a:
                for b_id in entities_b:
                    # Check if the pair exists in additional info and append its data
                    if (a_id, b_id) in additional_info[col]:
                        col_data += additional_info[col][(a_id, b_id)]
            cluster[f'{column_b}_{col}'] = col_data

        clusters.append(cluster)

    # Return the clusters as a DataFrame
    return pd.DataFrame(clusters)

# Sample data
data = {
    'employeeId': ['E1', 'E2', 'E2', 'E3', 'E4', 'E4', 'E5'],
    'departmentId': ['D1', 'D1', 'D2', 'D2', 'D3', 'D1', 'D4'],
    'departmentName': ['HR', 'HR', 'Finance', 'Finance', 'IT', 'HR', 'Marketing'],
    'location': ['New York', 'New York', 'London', 'London', 'San Francisco', 'New York', 'Berlin']
}

# Wrap into a dataframe
df = pd.DataFrame(data)

# Run the function 
cross_cluster(df, 'employeeId', 'departmentId', ['departmentName', 'location'])

# Add additional testing 
def test_cross_cluster():
    # Sample data for testing
    data = {
        'employeeId': ['E1', 'E2', 'E3', 'E4'],
        'departmentId': ['D1', 'D2', 'D2', 'D1'],
        'departmentName': ['HR', 'Finance', 'Finance', 'HR'],
        'location': ['New York', 'London', 'London', 'New York']
    }
    df = pd.DataFrame(data)

    # Expected results
    expected_columns = set(['employeeIds', 'departmentIds', 'departmentId_departmentName', 'departmentId_location'])
    
    # Running the function
    result_df = cross_cluster(df, 'employeeId', 'departmentId', ['departmentName', 'location'])
    
    # Asserting the test conditions
    assert set(result_df.columns) == expected_columns, "DataFrame does not have the correct columns"

    # Asserting a specific cluster
    # Note: This assumes that the result is in a specific order, which might not always be true
    expected_cluster = {
        'employeeIds': ['E1', 'E4'],
        'departmentIds': ['D1'],
        'departmentId_departmentName': ['HR'],
        'departmentId_location': ['New York']
    }

    # Convert the first row of DataFrame to dict for easy comparison
    result_cluster = result_df.iloc[0].apply(lambda x: sorted(x) if isinstance(x, list) else x).to_dict()

    assert all(result_cluster[k] == expected_cluster[k] for k in expected_columns), "Cluster data does not match the expected result"

    print("All tests passed.")

# Run the test
test_cross_cluster_function()
