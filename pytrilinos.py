# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

from time import sleep
import numpy as np
from PyTrilinos import Epetra

# <codecell>

# initialize MPI
Comm  = Epetra.PyComm()

# <codecell>

NumElements = 10
MapUnique = Epetra.Map(NumElements, 0, Comm)

# <codecell>

print "Unique map"
print MapUnique

# <codecell>

# Partially overlapping distribution
LocalElements = { 0: [0, 1, 2, 3, 4, 8],
                  1: [3, 4, 5, 6],
                  2: [6, 7, 8, 9] 
                }
MapOverl =  Epetra.Map(-1, LocalElements[Comm.MyPID()], 0, Comm)

# <codecell>

print "Partially overlapping map"
print MapOverl

# <codecell>

# Importer from overlapping to unique
Exporter = Epetra.Export(MapOverl, MapUnique)

# <codecell>

# Create vectors
XOverl = Epetra.Vector(MapOverl)
XUnique = Epetra.Vector(MapUnique) #initialized to 0

# <codecell>

XOverl[:] = Comm.MyPID() + 1
print "Max Value"
print Comm.MyPID(), XOverl.MaxValue()

# <codecell>

Comm.Barrier()
def printVector(label, vector):
    Comm.Barrier()
    if Comm.MyPID() == 0: print label
    sleep(Comm.MyPID())
    print (Comm.MyPID(), vector)
printVector("Overlapping Vector", XOverl)

# <codecell>

XUnique.Export(XOverl, Exporter, Epetra.Average)

# <codecell>

printVector("Unique Vector", XUnique)

# <codecell>

M=np.array([[ 2., -1.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
           [-1.,  2., -1.,  0.,  0.,  0.,  0.,  0.,  0.,  0.],
           [ 0., -1.,  2., -1.,  0.,  0.,  0.,  0.,  0.,  0.],
           [ 0.,  0., -1.,  2., -1.,  0.,  0.,  0.,  0.,  0.],
           [ 0.,  0.,  0., -1.,  2., -1.,  0.,  0.,  0.,  0.],
           [ 0.,  0.,  0.,  0., -1.,  2., -1.,  0.,  0.,  0.],
           [ 0.,  0.,  0.,  0.,  0., -1.,  2., -1.,  0.,  0.],
           [ 0.,  0.,  0.,  0.,  0.,  0., -1.,  2., -1.,  0.],
           [ 0.,  0.,  0.,  0.,  0.,  0.,  0., -1.,  2., -1.],
           [ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0., -1.,  2.]])

# <codecell>

MyGlobalElements  = MapUnique.MyGlobalElements()
Matrix            = Epetra.CrsMatrix(Epetra.Copy, MapUnique, 0)
for i in MyGlobalElements:
    if i > 0:
        Matrix[i, i - 1] = -1
    if i < NumElements - 1:
        Matrix[i, i + 1] = -1
    Matrix[i, i] = 2.
assert Matrix.FillComplete() == 0

# <codecell>

for i in MyGlobalElements:
    print "%d: Matrix(%d, %d) = %e" %(Comm.MyPID(), i, i, Matrix[i, i])

# <codecell>

XUnique2 = Epetra.Vector(MapUnique)
Matrix.Multiply(False, XUnique, XUnique2)

# <codecell>

printVector("Unique Vector", XUnique2)

# <codecell>

from PyTrilinos import AztecOO
Solution = Epetra.Vector(MapUnique)
LinProb = Epetra.LinearProblem(Matrix, Solution, XUnique2)
IterSolver = AztecOO.AztecOO(LinProb)
IterSolver.Iterate(10, 1e-9)
printVector("Correct Solution", XUnique)
printVector("Iterative Solution", Solution)

