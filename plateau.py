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

# Filter the dataframe where 'Emon-1[V]' > 0.2V
df_filtered = df[df['Emon-1[V]'] > 0.2]

# Apply Sigmoid function to 'Imon-1[A]' column for filtered data
df_filtered['Sigmoid(Imon-1[A])'] = df_filtered['Imon-1[A]'].apply(lambda x: sigmoid(x) if x > 0 else x)

# Create a directory to save the plots
output_dir = './plots_sp'
os.makedirs(output_dir, exist_ok=True)

# Group by the unique positions (Y, Z, X)
grouped = df_filtered.groupby(['Y-pos[m]', 'Z-pos[m]', 'X-pos[m]'])

# Iterate over each group and plot Sigmoid(Imon-1[A]) vs Emon-1[V]
for name, group in grouped:
    Y_pos, Z_pos, X_pos = name
    plt.figure()
    plt.plot(group['Emon-1[V]'], group['Imon-1[A]'], marker='o', linestyle='-')
    
    # Identify the maximum value of Imon-1[A]
    max_value = group['Imon-1[A]'].max()
    half_max_value = max_value / 2
    
    # Find the Emon-1[V] value corresponding to half_max_value
    half_max_emon = group.iloc[(group['Imon-1[A]'] - half_max_value).abs().argmin()]['Emon-1[V]']
    
    # Calculate the +/- 0.05V range around the Emon-1[V] value
    emon_minus_0_05 = half_max_emon - 0.05
    emon_plus_0_05 = half_max_emon + 0.05
    
    # Find the corresponding Imon-1[A] values for these Emon-1[V] values
    imon_minus_0_05 = group.iloc[(group['Emon-1[V]'] - emon_minus_0_05).abs().argmin()]['Imon-1[A]']
    imon_plus_0_05 = group.iloc[(group['Emon-1[V]'] - emon_plus_0_05).abs().argmin()]['Imon-1[A]']

    #print(f"Imon-1 de V+0.05 : {imon_plus_0_05}")


    # Find the treshold value
    #val_plateau = group[group['Imon-1[A]'] >= imon_plus_0_05]['Imon-1[A]'].mean()
    #print(f'Valeur plateau : {val_plateau}')
    # half_val_plateau
    #half_val_plateau = val_plateau / 2

    # Find the Emon-1[V] value corresponding to half_val_plateau
    half_max_emon = group.iloc[(group['Imon-1[A]'] - half_max_value).abs().argmin()]['Emon-1[V]']

    # Calculate the +/- 0.05V range around the Emon-1[V] value
    emon_minus_0_05 = half_max_emon - 0.05
    emon_plus_0_05 = half_max_emon + 0.05

    # Find the corresponding Imon-1[A] values for these Emon-1[V] values
    imon_minus_0_05 = group.iloc[(group['Emon-1[V]'] - emon_minus_0_05).abs().argmin()]['Imon-1[A]']
    imon_plus_0_05 = group.iloc[(group['Emon-1[V]'] - emon_plus_0_05).abs().argmin()]['Imon-1[A]']

    
    # Plot the maximum value line
    plt.axhline(y=max_value, color='r', linestyle='--', label=f'Plateau at {max_value:.2e}')
    
    # Plot the half maximum value line
    plt.axhline(y=half_max_value, color='g', linestyle='--', label=f'Half Plateau at {half_max_value:.2e}')
    
    # Plot the vertical lines
    plt.axvline(x=half_max_emon, color='b', linestyle='--', label=f'Half Plateau Emon at {half_max_emon:.2f}V')
    plt.axvline(x=emon_minus_0_05, color='m', linestyle='--', label=f'Emon - 0.05V at {emon_minus_0_05:.2f}V')
    plt.axvline(x=emon_plus_0_05, color='m', linestyle='--', label=f'Emon + 0.05V at {emon_plus_0_05:.2f}V')
    
    # Annotate the points of interest
    plt.plot(half_max_emon, half_max_value, 'bo')
    plt.plot(emon_minus_0_05, imon_minus_0_05, 'mo')
    plt.plot(emon_plus_0_05, imon_plus_0_05, 'mo')
    
    # Draw horizontal lines from the vertical lines to the curve
    plt.plot([half_max_emon, half_max_emon], [0, half_max_value], 'b--')
    plt.plot([emon_minus_0_05, emon_minus_0_05], [0, imon_minus_0_05], 'm--')
    plt.plot([emon_plus_0_05, emon_plus_0_05], [0, imon_plus_0_05], 'm--')
    
    # Draw horizontal lines for Imon-1[A] at Emon-1[V] +/- 0.05V
    plt.axhline(y=imon_minus_0_05, color='m', linestyle='--')
    plt.axhline(y=imon_plus_0_05, color='m', linestyle='--')
    
    plt.title(f'Imon-1[A] vs Emon-1[V] for Y={Y_pos:.2E}, Z={Z_pos:.2E}, X={X_pos:.2E}')
    plt.xlabel('Emon-1[V]')
    plt.ylabel('Imon-1[A]')
    plt.grid(True)
    plt.legend()
    
    # Save the plot to a file
    plot_filename = f'plot_Y{Y_pos:.2E}_Z{Z_pos:.2E}_X{X_pos:.2E}.png'
    plt.savefig(os.path.join(output_dir, plot_filename))
    plt.close()

print(f"Plots saved to: {output_dir}")
