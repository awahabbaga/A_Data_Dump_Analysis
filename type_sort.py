import pandas as pd

def make_columns_unique(df):
    df.columns = pd.Index([f"{col}_{i}" if list(df.columns).count(col) > 1 else col 
                           for i, col in enumerate(df.columns)])
    return df

def read_and_combine_matrices(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Initialize variables to store matrices and the current matrix
    matrices_dict = {'Type1': [], 'Type2': [], 'Type3': []}
    current_matrix = []
    inside_matrix = False
    current_keyword = None

    # Define the patterns for each type
    patterns = {
        'Type1': ['Summary', '"Ramp Stimulation"'],
        'Type2': ['Sweep_2_'],
        'Type3': ['Summary', '"Charge vs. Potential"']
    }

    # Read the file line by line
    for line in lines:
        for type_name, pattern in patterns.items():
            if all(p in line for p in pattern):
                inside_matrix = True
                current_keyword = type_name
                break

        if inside_matrix:
            if '"Index"' in line:
                if current_matrix:
                    try:
                        # Create a DataFrame from the current matrix
                        df = pd.DataFrame(current_matrix[1:], columns=current_matrix[0])
                        # Make columns unique
                        df = make_columns_unique(df)
                        matrices_dict[current_keyword].append(df)
                    except ValueError as e:
                        print(f"Skipping invalid matrix due to error: {e}")
                    current_matrix = []
                current_matrix.append(line.strip().split(','))
            elif line.strip() == '':  # End of current matrix
                inside_matrix = False
                if current_matrix:
                    try:
                        # Create a DataFrame from the current matrix
                        df = pd.DataFrame(current_matrix[1:], columns=current_matrix[0])
                        # Make columns unique
                        df = make_columns_unique(df)
                        matrices_dict[current_keyword].append(df)
                    except ValueError as e:
                        print(f"Skipping invalid matrix due to error: {e}")
                    current_matrix = []
            else:
                current_matrix.append(line.strip().split(','))

    # Add the last matrix if it exists
    if current_matrix:
        try:
            # Create a DataFrame from the current matrix
            df = pd.DataFrame(current_matrix[1:], columns=current_matrix[0])
            # Make columns unique
            df = make_columns_unique(df)
            matrices_dict[current_keyword].append(df)
        except ValueError as e:
            print(f"Skipping invalid matrix due to error: {e}")

    # Combine all matrices for each type into separate dataframes
    combined_matrices = {}
    for type_name, matrices in matrices_dict.items():
        if matrices:
            combined_matrix = pd.concat(matrices, ignore_index=True)
            combined_matrices[type_name] = combined_matrix
        else:
            print(f"No matrices found for type: {type_name}")

    return combined_matrices

################################################################
################################ File Name Here
################################################################
# Path to the source file
file_path = '500nm.asc'

# Read and combine the matrices
combined_matrices = read_and_combine_matrices(file_path)

# Define the required columns for each type
required_columns = {
    'Type1': ["Index", "Y-pos[m]", "Z-pos[m]"],
    'Type2': ["Index", "Time[s]       _1", "Imon-1[A]", "Time[s]       _3", "Emon-1[V]"],
    'Type3': ["Index", "X-pos[m]", "Z-pos[m]"]
}

# Filter and save the required columns for each combined matrix
for type_name, combined_matrix in combined_matrices.items():
    if type_name in required_columns:
        # Clean column names by stripping whitespace and removing quotes
        combined_matrix.columns = combined_matrix.columns.str.strip().str.replace('"', '')

        # Display the cleaned column names
        print(f"Cleaned column names for {type_name}: {combined_matrix.columns.tolist()}")

        # Filter the required columns
        filtered_matrix = combined_matrix[required_columns[type_name]]

        # Save the filtered matrix to a new CSV file
        output_file_path = f'./filtered/filtered_combined_matrices_{type_name}.csv'
        filtered_matrix.to_csv(output_file_path, index=False, float_format='%.9E')

        print(f"Filtered combined matrices for {type_name} saved to: {output_file_path}")
