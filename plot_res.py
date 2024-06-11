import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os

# Path to the uploaded file
file_path = 'final_unified_matrices.csv'

# Sigmoid function
def sigmoid(x):
    return 1 / (1 + np.exp(-x))

# Read the CSV file
df = pd.read_csv(file_path)

# Filter the dataframe where 0.03V <= 'Emon-1[V]' <= 0.5V
df_filtered = df[(df['Emon-1[V]'] >= 0.03) & (df['Emon-1[V]'] <= 0.5)].copy()

# Apply Sigmoid function to 'Imon-1[A]' column for filtered data
df_filtered.loc[:, 'Sigmoid(Imon-1[A])'] = df_filtered['Imon-1[A]'].apply(lambda x: sigmoid(x) if x > 0 else x)

# Create a directory to save the plots
output_dir = './plots_res'
os.makedirs(output_dir, exist_ok=True)

# Initialize an empty DataFrame to store all shifted data and results
shifted_data_df = pd.DataFrame()
results = []

# Group by the unique positions (Y, Z, X)
grouped = df_filtered.groupby(['Y-pos[m]', 'Z-pos[m]', 'X-pos[m]'])

# Iterate over each group
for name, group in grouped:
    Y_pos, Z_pos, X_pos = name

    # Shift Imon-1[A] values by the min Imon-1[A] value
    group.loc[:, 'Imon-1[A]'] = group['Imon-1[A]'] - group['Imon-1[A]'].min()

    # Append the shifted data to the combined DataFrame
    shifted_data_df = pd.concat([shifted_data_df, group])

    # Plot Imon-1[A] vs Emon-1[V]
    plt.figure()
    plt.plot(group['Emon-1[V]'], group['Imon-1[A]'], marker='o', linestyle='-', label='Data')
    plt.title(f'Imon-1[A] vs Emon-1[V] for Y={Y_pos:.2E}, Z={Z_pos:.2E}, X={X_pos:.2E}')
    plt.xlabel('Emon-1[V]')
    plt.ylabel('Imon-1[A]')
    plt.grid(True)
    plt.legend()

    # Save the plot to a file
    plot_filename = f'plot_Y{Y_pos:.2E}_Z{Z_pos:.2E}_X{X_pos:.2E}.png'
    plt.savefig(os.path.join(output_dir, plot_filename))
    plt.close()

    # Calculate values for results
    max_value = group['Imon-1[A]'].max()
    half_max_value = max_value / 2
    half_max_emon = group['Emon-1[V]'][group['Imon-1[A]'] >= half_max_value].iloc[0]

    emon_minus_0_05 = half_max_emon - 0.05
    emon_plus_0_05 = half_max_emon + 0.05

    imon_minus_0_05 = group['Imon-1[A]'][group['Emon-1[V]'] >= emon_minus_0_05].iloc[0]
    imon_plus_0_05 = group['Imon-1[A]'][group['Emon-1[V]'] >= emon_plus_0_05].iloc[0]

    emon_minus_0_07 = half_max_emon - 0.07
    emon_plus_0_07 = half_max_emon + 0.07

    imon_minus_0_07 = group['Imon-1[A]'][group['Emon-1[V]'] >= emon_minus_0_07].iloc[0]
    imon_plus_0_07 = group['Imon-1[A]'][group['Emon-1[V]'] >= emon_plus_0_07].iloc[0]

    # Store the results in the list
    results.append([Y_pos, Z_pos, X_pos, max_value, half_max_value, half_max_emon, 
                    emon_minus_0_05, imon_minus_0_05, emon_plus_0_05, imon_plus_0_05, 
                    emon_minus_0_07, imon_minus_0_07, emon_plus_0_07, imon_plus_0_07])

# Save the combined shifted data to a new CSV file
shifted_output_csv_path = 'shifted_data.csv'
shifted_data_df.to_csv(shifted_output_csv_path, index=False)

# Convert the results list to a DataFrame and save to CSV
results_df = pd.DataFrame(results, columns=['Y-pos[m]', 'Z-pos[m]', 'X-pos[m]', 'I_lim[A]', '1/2I_lim[A]', 
                                            'E(1/2I_lim)[V]', 'E(1/2I_lim)-0.05[V]', 'I(E-0.05)[A]', 
                                            'E(1/2I_lim)+0.05[V]', 'I(E+0.05)[A]', 'E(1/2I_lim)-0.07[V]', 
                                            'I(E-0.07)[A]', 'E(1/2I_lim)+0.07[V]', 'I(E+0.07)[A]'])
output_csv_path = 'results_matrix.csv'
results_df.to_csv(output_csv_path, index=False)

print(f"Plots saved to: {output_dir}")
print(f"Shifted data saved to: {shifted_output_csv_path}")
print(f"Results matrix saved to: {output_csv_path}")
