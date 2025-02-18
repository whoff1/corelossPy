Core Loss Data Fitting and Visualization

This Python script is designed for processing and fitting core loss data from files containing measurements of magnetic flux density (B) and power loss (P) at different frequencies. The data is extracted from tab-delimited files, and a model is fitted to the data using non-linear least squares optimization.

Requirements

- Python 3.x
- NumPy
- Matplotlib
- SciPy

You can install the required libraries using pip:

pip install numpy matplotlib scipy

File Structure

The script expects the core loss data files to be located in a specific directory (e.g., C:/Users/wagne/Desktop/Py/coreloss/50x600/). The files should be in .tab format, with the first column representing the magnetic flux density (B) and the second column representing the power loss (P) at different magnetic flux densities.

Functionality

Data Extraction

The script scans a specified directory for .tab files containing core loss data. For each file:
- It extracts the frequency value from the filename.
- It reads the B (magnetic flux density) and P (losses) values from the file using NumPy.

Model Fitting

A model based on Bertotti's equation [1] is used to fit the core loss data:

P = x1 * frequency * (B^x0) + x2 * (frequency^2) * (B^2) + x3 * (frequency^1.5) * (B^1.5)

The fitting parameters are obtained using the least_squares function from SciPy, which minimizes the difference between the model's predictions and the observed data.

Visualization

The script generates a plot showing:
- The observed data points (B vs. P).
- The fitted model curve for each frequency.

The plot is displayed for each frequency in the dataset.

Parameters

The fitted parameters are printed and stored in the parameters list for each frequency.

Example Usage

Ensure the core loss data files are placed in the directory specified in the script (e.g., C:/Users/coreloss/50x600/). Once the script is executed, it will automatically process the files, fit the model, and display the plots.

Plotting

The script uses matplotlib to generate a plot for each frequency, displaying the original data and the fitted model.

Adjustments

You can modify the path in the script to point to a different directory containing your .tab files. The script will scan the directory, extract the data, and fit the model accordingly.

The spredsheet compares the coefficients obtained with this python code and coefficients using Excel Solver for the same iron loss data.

License

This project is licensed under the MIT License - see the LICENSE file for details.

[1] G. Bertotti, "General properties of power losses in soft ferromagnetic materials", IEEE Transactions on magnetics, vol. 24, no. 1, pp. 621-630, 1988.
