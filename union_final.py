import pandas as pd

# Path to the uploaded files
file_path_type2 = './filtered/filtered_combined_matrices_Type2.csv'
file_path_unified = './filtered/unified_position_xyz.csv'

# Read the CSV files
df_type2 = pd.read_csv(file_path_type2)
df_unified = pd.read_csv(file_path_unified)

# column names for debugging
print("Type2 columns:", df_type2.columns.tolist())
print("Unified columns:", df_unified.columns.tolist())

# Initialize the resulting DataFrame
result_df = pd.DataFrame()

# Iterate over the rows in the Type2 DataFrame
unified_index = 0
for index, row in df_type2.iterrows():
    if row['Index'] == 0 and unified_index < len(df_unified):
        unified_row = df_unified.iloc[unified_index]
        unified_index += 1
    combined_row = {**unified_row.to_dict(), **row.to_dict()}
    result_df = pd.concat([result_df, pd.DataFrame([combined_row])], ignore_index=True)

# Select and order the required columns, dropping the Time columns
final_columns = ['Y-pos[m]', 'Z-pos[m]', 'X-pos[m]', 'Index', 'Imon-1[A]', 'Emon-1[V]']
final_df = result_df[final_columns]

# Conversion de la colonne Index en int
final_df['Index'] = final_df['Index'].astype(int)

# Save the final DataFrame to a new CSV file
output_file_path = 'final_unified_matrices.csv'
final_df.to_csv(output_file_path, index=False, float_format='%.9E')

print(f"Final unified matrices saved to: {output_file_path}")
