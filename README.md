# AutoSlice

## Description
Before you start, ensure that you have the pvbatch executable in your system's path or add an alias to your .bashrc file. For example, if you have ParaView installed in your home directory, you can add the following line to your .bashrc file:

```bash
alias pvbatch="/fullPathToParaview/bin/pvbatch"
```
Ensure you have prepared the centerline data and its corresponding normal vectors data file.

### centerLineConvert.py
This script calculates the normal vectors for the centerline and writes the center data points and normal vectors to a file. It's used to convert the centerline of the plaque to a normal vector field.

The normal vector field defines the slicing plane for ParaView to cut the geometry at the centerline. The resulting normal vector field is saved in a CSV file with headers x, y, z, nx, ny, nz.

Input: centerLinePlaque.csv
Output: centerLinePlaqueNormal.csv

## Usage 
```bash
python centerLineConvert.py
```

### AutoSlice.py    
This script is designed to slice the geometry along the centerline using ParaView's batch processing mode (pvbatch). It reads the normal vector field from centerLinePlaqueNormal.csv, slices the geometry at the specified point ID, and saves the sliced data to a CSV file in the data directory.

Input: centerLinePlaqueNormal.csv
Change: Adjust the pointID to specify the desired point to slice along the centerline
Output: data/{pointID}.csv
Location: This script should be executed within the OpenFOAM case directory.

Note: The script is set to use the last time step by default.

## Usage 
```bash
pvbatch AutoSlice.py
```

