# A Data Dump Analysis

This repository contains scripts for analyzing Voltamogram data. The project involves sorting, unifying, and plotting data from various sources.

## Project Structure

- `type_sort.py`: Sorts data into different types.
- `union_xyz.py`: Unifies XYZ data.
- `union_final.py`: Merges final data into a single dataset.
- `plot.py`: Plots current (I) vs. voltage (V) for each distinct position (Y, Z, X).
- `plot_res.py`: Plots I vs V for each distinct (Y,Z,X) with the lim marks(I_lim, Half_I_lim, etc...)
- `index_2d.py`: 2D Color graded Histogram of Y by X with Imon-1[A] as Color and the GIF of those images.
- `procedure.py`: Automates the execution of the above scripts in sequence.

## Usage

1. Clone the repository:
    ```sh
    git clone https://github.com/awahabbaga/A_Data_Dump_Analysis.git
    cd A_Data_Dump_Analysis
    ```

2. Ensure all dependencies are installed:
    ```sh
    pip install -r requirements.txt
    ```

3. Upload the data dump  
    > A **.asc** or **.csv** file. Just need a ***comma*** separated file.

4. Run the automated procedure script:
    ```sh
    python procedure.py
    ```

## Outputs

- The filtered data will be saved in the `./filtered` directory.
- Plots of I vs. V for each distinct position will be saved in `./filtered/plots`.

## Contributing

Feel free to fork the repository and submit pull requests. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License.
