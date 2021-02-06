# Installing gmx_MMPBSA

## Requirements

`gmx_MMPBSA` requires AmberTools20 to be installed in your machine with Python3 and the shell environment correctly set
up for Amber. The AmberTools suite is free of charge and you can check 
[Amber Manual](https://ambermd.org/doc12/Amber20.pdf#section.2.1) for a detailed installation guide. Of note, you 
can have more than one AmberTools installed in your machine. In case AmberTools20 is not the default Amber in your 
computer, just make sure to source AmberTools20 before installing/updating/running `gmx_MMPBSA`.
`gmx_MMPBSA` also requires GROMACS (series 4.x.x or 5.x.x or 20xx.x) to be installed in your computer and the shell
environment correctly set up for GROMACS. `gmx_MMPBSA` has been tested with GROMACS 4.6.7, 5.1.2 and 2018.3, although it
should run smoothly with any GROMACS present in the PATH and that is compatible with the files you are using.

`gmx_MMPBSA` contains a module that allows for plotting the results (`gmx_MMPBSA_gui`). For this, it requires the
installation of PyQt5.

    amber.python -m pip install PyQt5

## Installation

You can install `gmx_MMPBSA` from the `stable` version on PYPI:

    amber.python -m pip install gmx_MMPBSA


or the `development` version from GitHub:


    amber.python -m pip install git+https://github.com/Valdes-Tresanco-MS/gmx_MMPBSA

Make sure that you have `git` installed. If not you can install it as follow:

    sudo apt install git

## Update

If you already have installed a previous `gmx_MMPBSA` version, you can update it as follows:

`stable` version (recommended):

    amber.python -m pip install gmx_MMPBSA --upgrade

`development` version from GitHub:

    amber.python -m pip intall git+https://github.com/Valdes-Tresanco-MS/gmx_MMPBSA --upgrade 

Make sure that you have `git` installed.

**We will do our best to keep the PYPI package up to date.**

## After Install

Once the installation is completed, the following warning may appear:

    WARNING: The scripts gmx_MMPBSA and gmx_MMPBSA_gui are installed in 
    '/home/user/path_to_amber_install/amber20/miniconda/bin' which is not on PATH.

This warning is because `pip` installs the executables (`gmx_MMPBSA` and `gmx_MMPBSA_gui`) in \*/amber20/miniconda/bin.

You have two options to solve this:

Add this folder (*/amber20/miniconda/bin) to PATH:

    export PATH="/home/user/path_to_amber_install/amber20/miniconda/bin:$PATH"

*This option is more permanent and is recommended if you don't want to activate and deactivate the conda environment*

```tip
Make sure to update **user** and **path_to_amber_install** in the PATH variable
```

or

initializing the environment of conda amber:

    amber.conda init bash

You can deactivate like this:

    conda deactivate

After using one of the above options, you should be able to run `gmx_MMPBSA` and `gmx_MMPBSA_gui` through the terminal

If when running `gmx_MMPBSA`, you get an error like this:

    ModuleNotFoundError: No module named 'parmed'

please see the following [issue](https://github.com/Valdes-Tresanco-MS/gmx_MMPBSA/issues/2) to see the solution
