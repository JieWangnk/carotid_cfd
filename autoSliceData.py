""""
This script is used to slice the geometry at the center line of the plaque.
The normal vector field is saved to a csv file with header x,y,z,nx,ny,nz
input: centerLinePlaqueNormal.csv
change: the index pointID to slice the geometry at the center line
output: data/{pointID}.csv
usage: /{user_path}/ParaView-5.11.0-MPI-Linux-Python3.9-x86_64/bin/pvbatch autoSliceData.py
excuate this script in the openfoam case directory
"""

import os
import pandas as pd
from paraview.simple import *


class AutoSlice(object):
    def __init__(self, input_file):
        self.input_file = input_file
        self.output_dir = os.path.join(os.getcwd(), 'data')

        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

        self.ffoam = OpenFOAMReader(
            registrationName='f.foam', FileName=input_file)
        self.renderView1 = GetActiveViewOrCreate('RenderView')
        self.ffoamDisplay = Show(
            self.ffoam, self.renderView1, 'UnstructuredGridRepresentation')
        self.extractSurface1 = ExtractSurface(
            registrationName='ExtractSurface1', Input=self.ffoam)
        self.renderView1.Update()
        self.spreadSheetView1 = CreateView('SpreadSheetView')

    def slice_and_save(self, x, y, z, nx, ny, nz, pointID):
        slice1 = Slice(
            registrationName=f'Slice{pointID}', Input=self.extractSurface1)
        slice1.SliceType = 'Plane'
        slice1.HyperTreeGridSlicer = 'Plane'
        slice1.SliceOffsetValues = [0.0]
        slice1.SliceType.Origin = [x, y, z]
        slice1.SliceType.Normal = [nx, ny, nz]
        slice1.HyperTreeGridSlicer.Origin = [x, y, z]

        self.renderView1.Update()

        slice1Display = Show(slice1, self.spreadSheetView1,
                             'SpreadSheetRepresentation')
        self.renderView1.Update()

        ExportView(os.path.join(self.output_dir,
                   f'{pointID}.csv'), view=self.spreadSheetView1)


if __name__ == "__main__":
    input_file = 'f.foam'
    data_slicer = AutoSlice(input_file)

    df = pd.read_csv('centerLinePlaqueNormal.csv')
    pointID = df.index.tolist()  # Use index as pointID
    # start from the 2nd point only slice every 10 points
    pointID = pointID[1::10]
    for i in pointID:
        x = df.loc[i, 'x']
        y = df.loc[i, 'y']
        z = df.loc[i, 'z']
        nx = df.loc[i, 'nx']
        ny = df.loc[i, 'ny']
        nz = df.loc[i, 'nz']
        print(x, y, z, nx, ny, nz)

        data_slicer.slice_and_save(x, y, z, nx, ny, nz, i)
        print(f'Point ID {i} is sliced and saved.')
