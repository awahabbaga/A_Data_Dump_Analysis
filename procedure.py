import os
import subprocess

# Function to create a directory if it doesn't exist
def create_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

# Étape 1: Create the './filtered' directory
create_directory('./filtered')

# Étape 2: Execute type_sort.py
#### Put in the name of the file in 'type_sort.py' before executing
subprocess.run(['python', 'type_sort.py'], check=True)

# Étape 3: Execute union_xyz.py
subprocess.run(['python', 'union_xyz.py'], check=True)

# Étape 4: Execute union_final.py
subprocess.run(['python', 'union_final.py'], check=True)

# Étape 5: Execute plot.py
#subprocess.run(['python', 'plot.py'], check=True)

# Étape 5: Execute plot_res.py
### Uncomment to plot the Voltamogram(Sigmoid like looking) and
### And get the Organized Plateau data in 'results_matrix.csv'
### Y-pos[m]', 'Z-pos[m]', 'X-pos[m]', 'I_lim[A]', '1/2I_lim[A]',
### 'E(1/2I_lim)[V]', 'E(1/2I_lim)-0.05[V]', 'I(E-0.05)[A]', 'E(1/2I_lim)+0.05[V]', 'I(E+0.05)[A]'
subprocess.run(['python', 'plot_res.py'], check=True)

# Étape 6: Execute index_2d.py
### Uncomment the following to get the 2D Color graded Histogram of Y by X with Imon-1[A] as Color
### And the GIF of those images
#subprocess.run(['python', 'index_2d.py'], check=True)
