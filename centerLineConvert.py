"""
This script is used to convert the center line of the plaque to a normal vector field.  
The normal vector field is used to define the slice plane for paraview to slice the geometry at the center line.
The normal vector field is saved to a csv file with header x,y,z,nx,ny,nz
input: centerLinePlaque.csv
output: centerLinePlaqueNormal.csv

usage: python centerLineConvert.py
"""


import numpy as np

# Read data from csv file
dataPoint = np.genfromtxt('centerLinePlaque.csv', delimiter=',', skip_header=1)

dataPoint = np.array(dataPoint)

# Calculate normal vectors between points
normal_vectors = [[0, 0, 0]]
for i in range(1, len(dataPoint)):
    vector = dataPoint[i] - dataPoint[i - 1]
    norm = np.linalg.norm(vector)
    if norm > 0:
        normal_vector = vector / norm
    else:
        #reverse the vector
        normal_vector = -normal_vectors[i-1]
    normal_vectors.append(normal_vector)


normal_vectors = np.array(normal_vectors)

# save normal vectors and extrapolated points to one file with header x,y,z,nx,ny,nz
data = np.concatenate((dataPoint, normal_vectors), axis=1)
np.savetxt('centerLinePlaqueNormal.csv', data, delimiter=',',
           header='x,y,z,nx,ny,nz', comments='')



