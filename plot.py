import pandas as pd
import matplotlib.pyplot as plt
import os

# Path to the uploaded file
file_path = 'final_unified_matrices.csv'

# Read the CSV file
df = pd.read_csv(file_path)

# Display the first few rows for debugging
print(df.head())

# Create a directory to save the plots
output_dir = './plots'
os.makedirs(output_dir, exist_ok=True)

# Group by the unique positions (Y, Z, X)
grouped = df.groupby(['Y-pos[m]', 'Z-pos[m]', 'X-pos[m]'])

# Iterate over each group and plot I vs V
for name, group in grouped:
    Y_pos, Z_pos, X_pos = name
    plt.figure()
    plt.plot(group['Emon-1[V]'], group['Imon-1[A]'], marker='o', linestyle='-')
    plt.title(f'I vs V for Y={Y_pos:.2E}, Z={Z_pos:.2E}, X={X_pos:.2E}')
    plt.xlabel('Emon-1[V]')
    plt.ylabel('Imon-1[A]')
    plt.grid(True)
    
    # Save the plot to a file
    plot_filename = f'plot_Y{Y_pos:.2E}_Z{Z_pos:.2E}_X{X_pos:.2E}.png'
    plt.savefig(os.path.join(output_dir, plot_filename))
    plt.close()

print(f"Plots saved to: {output_dir}")
