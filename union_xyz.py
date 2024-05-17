import pandas as pd

# Path to the uploaded files
file_path_type1 = './filtered/filtered_combined_matrices_Type1.csv'
file_path_type3 = './filtered/filtered_combined_matrices_Type3.csv'

# Read the CSV files
df_type1 = pd.read_csv(file_path_type1)
df_type3 = pd.read_csv(file_path_type3)

# Display the column names for debugging
print("Type1 columns:", df_type1.columns.tolist())
print("Type3 columns:", df_type3.columns.tolist())

# Merge the DataFrames based on the common column 'Z-pos[m]'
merged_df = pd.merge(df_type1, df_type3, on='Z-pos[m]', suffixes=('_type1', '_type3'))

# Select the required columns
final_columns = ['Y-pos[m]', 'Z-pos[m]', 'X-pos[m]']
final_df = merged_df[final_columns]

# Save the final merged DataFrame to a new CSV file
output_file_path = './filtered/unified_matrices.csv'
final_df.to_csv(output_file_path, index=False, float_format='%.9E')

print(f"Unified matrices saved to: {output_file_path}")
