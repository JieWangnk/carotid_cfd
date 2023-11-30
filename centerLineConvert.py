"""
This script is used to convert the center line of the plaque to a normal vector field.  
The normal vector field is used to define the slice plane for paraview to slice the geometry at the center line.
The normal vector field is saved to a csv file with header x,y,z,nx,ny,nz
input: centerLinePlaque.csv
output: centerLinePlaqueNormal.csv
we use the extrapolated points to calculate the normal vectors, here we use 2 extrapolated points between each two points

usage: python centerLineConvert.py
"""


import numpy as np
import matplotlib.pyplot as plt

# Read data from csv file
dataPoint = np.genfromtxt('centerLinePlaque.csv', delimiter=',', skip_header=1)

# Number of extrapolated points
num_points = 2
# Extrapolate points
extrapolated_points = []
for i in range(len(dataPoint) - 1):
    for j in range(num_points):
        alpha = j / (num_points - 1)
        interpolated_point = (1 - alpha) * \
            dataPoint[i] + alpha * dataPoint[i + 1]
        extrapolated_points.append(interpolated_point)

extrapolated_points = np.array(extrapolated_points)

# Calculate normal vectors between points
normal_vectors = [[0, 0, 0]]
for i in range(1, len(extrapolated_points)):
    vector = extrapolated_points[i] - extrapolated_points[i - 1]
    norm = np.linalg.norm(vector)
    if norm > 0:
        normal_vector = vector / norm
    else:
        #reverse the vector
        normal_vector = -normal_vectors[i-1]
    normal_vectors.append(normal_vector)


normal_vectors = np.array(normal_vectors)

print('extrapolated_points.shape = ', extrapolated_points.shape)
# save normal vectors and extrapolated points to one file with header x,y,z,nx,ny,nz
data = np.concatenate((extrapolated_points, normal_vectors), axis=1)
np.savetxt('centerLinePlaqueNormal.csv', data, delimiter=',',
           header='x,y,z,nx,ny,nz', comments='')



