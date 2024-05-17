import os
import subprocess

# Function to create a directory if it doesn't exist
def create_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

# Étape 1: Create the './filtered' directory
create_directory('./filtered')

# Étape 2: Execute type_sort.py
subprocess.run(['python', 'type_sort.py'], check=True)

# Étape 3: Execute union_xyz.py
subprocess.run(['python', 'union_xyz.py'], check=True)

# Étape 4: Execute union_final.py
subprocess.run(['python', 'union_final.py'], check=True)

# Étape 5: Execute plot.py
#subprocess.run(['python', 'plot.py'], check=True)
