import os
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image

# Load the provided CSV file
file_path = 'final_unified_matrices.csv'
data = pd.read_csv(file_path)

# Directory to save the histograms
output_dir = 'index_histograms'
os.makedirs(output_dir, exist_ok=True)

# Getting the unique Index values in the dataset
unique_indices = data['Index'].unique()

# Creating and saving 2D histograms for each unique Index value
image_paths = []

# Creating and saving 2D histograms for each unique Index value
for index_value in unique_indices:
    filtered_data = data[data['Index'] == index_value]
    
    plt.figure(figsize=(10, 6))
    plt.hist2d(filtered_data['X-pos[m]'], filtered_data['Y-pos[m]'], bins=5, weights=filtered_data['Imon-1[A]'], cmap='viridis')
    plt.colorbar(label='Imon-1[A]')
    plt.xlabel('X-pos[m]')
    plt.ylabel('Y-pos[m]')
    plt.title(f'2D Histogram of Y by X with Imon-1[A] as Color (Index = {index_value})')
    
    # Save the figure
    img_path = os.path.join(output_dir, f'index_{index_value}.png')
    plt.savefig(img_path)
    plt.close()
    image_paths.append(img_path)

    # Create a GIF from the saved images
    gif_path = os.path.join(output_dir, 'histograms.gif')
    with Image.open(image_paths[0]) as img:
        img.save(gif_path, save_all=True, append_images=[Image.open(p) for p in image_paths[1:]], duration=500, loop=0)

    print(f"GIF saved at: {gif_path}")
