% Python for High Performance Computing
% Andrea Zonca, UCSB
% 13 Nov 2012

# Topics

* Trivially parallel tasks: IPython parallel
* Fully parallel software: HDF5 and PyTrilinos

# Trivially parallel tasks with IPython parallel

## Architecture:

* Submit function+arguments to a queue (managed by the `controller`) consumed by workers (engines)
* function is *serial*, no IPython-specific, easy debugging
* works the same in serial, locally on multi-core, or on large cluster

# IPython parallel: Local example

open IPython notebook `ipythonparallel.ipynb`

## Tips

Launch `ipcluster` from same folder of the script so the engines have same path

Define the function in its own module, otherwise necessary to rewrite the import statements

# IPython parallel on a HPC cluster

* Launch `ipcontroller` on the login node
* Submit ipengine job to the queue management system (see documentation on how to build a pbs script)
* Open IPython on the login node and submit jobs
to the controller

# Example run for Planck

* 1.5TB of raw data in ~3000 FITS files
* read files, simple processing and rewrite to disk
* run IPython parallel with up to 500 engines
* process the jobs in ~3 hours

# Distributed Linear Algebra

Large complete C++ packages with Python support

* PETSC, petsc4py
* Trilinos, PyTrilinos

Both use C++ for MPI communication and LAPACK/BLAS for computing

Both subclass numpy arrays

# Trilinos example

`pytrilinos.ipynb`

export pytrilinos.py and run with mpirun -n 3 python pytrilinos.py
