# The input file

## Description

As `gmx_MMPBSA` is based on [MMPBSA.py](https://pubs.acs.org/doi/10.1021/ct300418h), it uses an input file containing
all the specification for the MM/PB(GB)SA calculation. The input file is designed to be as syntactically similar to
other programs in Amber as possible. The input file has the same namelist structure as both sander and pmemd. The
allowed namelists are &general, &gb, &pb, &rism, &alanine_scanning, &nmode, and &decomp. The input variables recognized
in each namelist are described below, but those in &general are typically variables that apply to all aspects of the
calculation or parameters required for build amber topologies from GROMACS files. The &gb namelist is unique to
Generalized Born calculations, &pb is unique to Poisson Boltzmann calculations, &rism is unique to 3D-RISM calculations,
&alanine_scanning is unique to alanine scanning calculations, &nmode is unique to the normal mode calculations used to
approximate vibrational entropies, and &decomp is unique to the decomposition scheme. All of the input variables are
described below according to their respective namelists. Integers and floating point variables should be typed as-is
while strings should be put in either single- or double-quotes. All variables should be set with `variable = value` and
separated by commas. See several
[examples](../../Documentation/input_file#sample-input-files) below. As you will see, several
calculations can be performed in the same run (_i.e._ &gb and &pb, &gb and &alanine_scanning, &pb and &decomp, etc).
Variables will usually be matched to the minimum number of characters required to uniquely identify that variable within
that namelist. Variables require at least 4 characters to be matched unless that variable name has fewer than 4
characters (in which case the whole variable name is required). For example, “star” in &general will match “startframe”.
However, “stare” and “sta” will match nothing.

### **`&general` namelist variables**

`assign_chainID` Defines the chains ID assignment mode. _It is ignored when defining a reference structure
(recommended)_. If `assign_chainID = 1`, gmx_MMPBSA check if the structure has no chains ID and it is assigned according
to the structure`*`. If `assign_chainID = 2`, `gmx_MMPBSA` re-assign the chains ID, exist or not, according to the
structure`*` (can generate inconsistencies). If a `*.gro` file was used for complex structure
(`-cs` flag) and not reference structure was provided, `gmx_MMPBSA` assume `assign_chainID = 1`. (Default = 0)

```tip
`*` _The chain ID is assigned according to two criteria: **terminal amino acids** and **residue numbering**. If
both criteria or residue numbering changes are present, we assign a new chain ID. If there are terminal amino acids but
the numbering of the residue continues, we do not change the ID of the chain._
```

`debug_printlevel` MMPBSA.py prints errors by raising exceptions, and not catching fatal errors. If debug_printlevel is
set to 0, then detailed tracebacks (effectively the call stack showing exactly where in the program the error occurred)
is suppressed, so only the error message is printed. If debug_printlevel is set to 1 or higher, all tracebacks are
printed, which aids in debugging of issues. (Default = 0) (Advanced Option)

```tip
_Now `gmx_MMPBSA` shows the command-line used to build AMBER topologies when `debug_printlevel = 1 or higher`._ 
```

`startframe` The frame from which to begin extracting snapshots from the full, concatenated trajectory comprised of
every trajectory file placed on the command-line. This is always the first frame read. (Default = 1)

`endframe` The frame from which to stop extracting snapshots from the full, concatenated trajectory comprised of every
trajectory file supplied on the command-line. (Default = 9999999)

`entropy` It specifies whether to perform a quasi-harmonic entropy (QH) approximation with ptraj or the
[Interaction Entropy (IE)](https://pubs.acs.org/doi/abs/10.1021/jacs.6b02682) approximation. The allowed values are
(default = 0):

* 0: Don’t
* 1: perform QH
* 2: perform IE

```tip
 _Included Interaction entropy aproximation._
 ```

`entropy_seg` Specify the representative segment (in %), starting from the `endframe`, for the calculation of the
Interaction Entropy, _e.g._: `entropy_seg = 25` means that the last quartile of the total number of frames
(`(endframe-startframe)/interval`) will be used to calculate the average Interaction Entropy. (Default = 25) (Only
if `entropy = 2`)

`entropy_temp` Specify the temperature to calculate the entropy term `−TΔS` (Only if `entropy` = 2). Avoid
inconsistencies with defined internal temperature (298.15 K) when nmode is used (Default = 298.15)

`gmx_path` Define an additional path to search for GROMACS executables. This path takes precedence over the path defined
in the PATH variable. In these path the following executables will be searched: `gmx`, `gmx_mpi`, `gmx_d`,
`gmx_mpi_d` (Gromcas > 5.x.x), `make_ndx` and `trjconv` (GROMACS 4.x.x)

`interval` The offset from which to choose frames from each trajectory file. For example, an interval of 2 will pull
every 2nd frame beginning at startframe and ending less than or equal to endframe. (Default = 1)

`netcdf` Specifies whether or not to use NetCDF trajectories internally rather than writing temporary ASCII trajectory
files. For very large trajectories, this could offer significant speedups, and requires less temporary space. However,
this option is incompatible with alanine scanning. Default value is 0.

* 0: Do NOT use temporary NetCDF trajectories
* 1: Use temporary NetCDF trajectories

`PBRadii` PBRadii to build amber topology files (Default = 3):

* 1: bondi, recommended when igb = 7
* 2: mbondi, recommended when igb = 1
* 3: mbondi2, recommended when igb = 2 or 5
* 4: mbondi3, recommended when igb = 8

`protein_forcefield` Define the force field used to build Amber topology for proteins. Make sure this force field is the
same as the one used in GROMACS (Default = "oldff/leaprc.ff99SB")
Force fields tested:

* "oldff/leaprc.ff99"
* "oldff/leaprc.ff03"
* "oldff/leaprc.ff99SB"
* "oldff/leaprc.ff99SBildn"
* "leaprc.protein.ff14SB"

```tip
_This notation format is the one used in tleap._
```

`ligand_forcefield` Define the force field used to build Amber topology for small molecules or glycams. Make sure this
force field is the same as the one used for GROMACS (Default = "leaprc.gaff"). Force fields tested:

* "leaprc.gaff"
* "leaprc.gaff2"
* "leaprc.GLYCAM_06j-1"    (Compatible with amber12SB and later)
* "leaprc.GLYCAM_06EPb"    (Compatible with amber12SB and later)
* "gmxMMPBSA/leaprc.GLYCAM_06h-1"    `*`(Included in gmx_MMPBSA package. Compatible with amber99SB and earlier)
* "gmxMMPBSA/leaprc.zaa99SB"    `*`Parameters for Zwitterionic amino acids. (Included in gmx_MMPBSA package. Compatible
  with amber 99SB)

```tip
`*` We create a new folder (named _gmxMMPBSA_) in each one of the Amber's parameter folders (
$AMBERHOME/dat/leap/[cmd, prep, lib, parm]/gmxMMPBSA). This way, we keep gmx_MMPBSA data separated from Amber's.

_This notation format is the one used in tleap._
```

`ions_parameters` Define ions parameters to build the Amber topology. (Default = 1)

* 1: frcmod.ions234lm_126_tip3p
* 2: frcmod.ions234lm_iod_tip4pew
* 3: frcmod.ions234lm_iod_spce
* 4: frcmod.ions234lm_hfe_spce
* 5: frcmod.ions234lm_126_tip4pew
* 6: frcmod.ions234lm_126_spce
* 7: frcmod.ions234lm_1264_tip4pew
* 8: frcmod.ions234lm_1264_tip3p
* 9: frcmod.ions234lm_1264_spce
* 10: frcmod.ions234lm_iod_tip3p
* 11: frcmod.ions234lm_hfe_tip4pew
* 12: frcmod.ions234lm_hfe_tip3p

`reuse_files` Define whether the trajectories files will be reused when the program ends in error. (Default = 0)

* 0: Don't reuse. If there are temporary trajectory files, they will be deleted
* 1: Reuse existing trajectory file

```warning
Note that the trajectories files may not be generated correctly due to internal errors or interruptions. Please use 
it with care.
```

`solvated_trajectory` Define if it is necessary to build a clean trajectory with no water and ions (Default = 1)

* 0: Don’t
* 1: Build clean trajectory


`use_sander` use sander for energy calculations, even when mmpbsa_py_energy will suffice (Default = 0)

* 0: Use mmpbsa_py_energy when possible
* 1: Always use sander

`verbose` The variable that specifies how much output is printed in the output file. There are three allowed values (
Default = 1):

* 0: print difference terms
* 1: print all complex, receptor, and ligand terms
* 2: also print bonded terms if one trajectory is used

### **`&gb` namelist variables**

`ifqnt` Specifies whether a part of the system is treated with quantum mechanics. This functionality requires sander igb
Generalized Born method to use (seeSection 4). Allowed values are 1, 2, 5, 7 and 8. (Default = 5) All models are now
available with both mmpbsa_py_energy and sander.(Default = 0)

* 0: Potential function is strictly classical
* 1: Use QM/MM

`qm_residues` Comma- or semicolon-delimited list of complex residues to treat with quantum mechanics. All whitespace is
ignored. All residues treated with quantum mechanics in the complex must be treated with quantum mechanics in the
receptor or ligand to obtain meaningful results.

`intdiel` Define Internal dielectric constant without use external *.mdin file (Default = 1.0)

`qm_theory` Which semi-empirical Hamiltonian should be used for the quantum calculation. No default, this must be
specified. See its description in the QM/MM section of the manual for options.

`qmcharge_com` The charge of the quantum section for the complex. (Default = 0)

`qmcharge_lig` The charge of the quantum section of the ligand. (Default = 0)

`qmcharge_rec` The charge of the quantum section for the receptor. (Default = 0)

`qmcut` The cutoff for the qm/mm charge interactions. (Default = 9999.0)

`saltcon` Salt concentration in Molarity. (Default = 0.0)

`surfoff` Offset to correct (by addition) the value of the non-polar contribution to the solvation free energy term
(Default 0.0)

`surften` Surface tension value (Default = 0.0072). Units in kcal/mol/ Å 2

`molsurf` When set to 1, use the molsurf algorithm to calculate the surface area for the nonpolar solvation term. When
set to 0, use LCPO (Linear Combination of Pairwise Overlaps). (Default 0)

`probe` Radius of the probe molecule (supposed to be the size of a solvent molecule), in Angstroms, to use when
determining the molecular surface (only applicable when molsurf is set to 1). Default is 1.4.

`msoffset` Offset to apply to the individual atomic radii in the system when calculating the molsurf surface. See the
description of the molsurf action command in [cpptraj](https://ambermd.org/doc12/Amber20.pdf#chapter.32). Default is 0.

### **`&pb` namelist variables**

`inp` Option to select different methods to compute non-polar solvation free energy (Default = 2).

* 0: No non-polar solvation free energy is computed
* 1: The total non-polar solvation free energy is modeled as a single term linearly proportional to the solvent
  accessible surface area, as in the PARSE parameter set, that is, if INP = 1, USE_SAV must be equal to 0.
* 2: The total non-polar solvation free energy is modeled as two terms: the cavity term and the dispersion term. The
  dispersion term is computed with a surface-based integration method closely related to the PCM solvent for quantum
  chemical programs. Under this framework, the cavity term is still computed as a term linearly proportional to the
  molecular solvent-accessible-surface area (SASA) or the molecular volume enclosed by SASA.

`cavity_offset` Offset value used to correct non-polar free energy contribution (Default = -0.5692) This is not used for
APBS.

`cavity_surften` Surface tension. (Default = 0.0378 kcal/mol Angstrom 2 ). Unit conversion to kJ done automatically for
APBS.

`exdi` External dielectric constant (Default = 80.0).

`indi` Internal dielectric constant (Default = 1.0).

`fillratio` The ratio between the longest dimension of the rectangular finite-difference grid and that of the solute
(Default = 4.0).

`scale` Resolution of the Poisson Boltzmann grid. It is equal to the reciprocal of the grid spacing. (Default = 2.0)

`istrng` Ionic strength in Molarity. It is converted to mM for PBSA and kept as M for APBS. (Default = 0.0)

`linit` Maximum number of iterations of the linear Poisson Boltzmann equation to try (Default = 1000)

`prbrad` Solvent probe radius in Angstroms. Allowed values are 1.4 and 1.6 (Default = 1.4)

`radiopt` The option to set up atomic radii according to 0: the prmtop, or 1: pre-computed values (see Amber manual for
more complete description). (Default = 1)

`sander_apbs` Option to use APBS for PB calculation instead of the built-in PBSA solver. This will work only through the
iAPBS interface built into sander.APBS. Instructions for this can be found online at the iAPBS/APBS websites. Allowed
values are 0: Don’t use APBS, or 1: Use sander.APBS. (Default = 0)

`memopt` Turn on membrane protein support (Default = 0).

`emem` Membrane dielectric constant (Default = 1.0).

`mthick` Membrane thickness (Default = 40.0).

`mctrdz` Absolute membrane center in the z-direction (Default=0.0, use protein center as the membrane center).

`poretype` Turn on the automatic membrane channel/pore finding method (Default=1).

A more thorough description of these and other options can be
found [here](https://ambermd.org/doc12/Amber20.pdf#chapter.6). Please also note that the default options have changed
over time. For a detailed discussion of all related options on the quality of the MM/PB(GB)SA calculations, please check
this [publication](https://onlinelibrary.wiley.com/doi/10.1002/jcc.24467).

### **`&alanine_scanning` namelist variables**

`mutant_only` Option to perform specified calculations only for the mutants. Allowed values are 0: Do mutant and
original or 1: Do mutant only (Default = 0)
Note that all calculation details are controlled in the other namelists, though for alanine scanning to be performed,
the namelist must be included (blank if desired)

`mutant` Define whether the mutation will be perform in receptor or ligand. Allowed values are: receptor, rec, ligand or
lig in any capitalization (Default = receptor or REC)

`mutant_res` Define the specific residue that is going to be mutated. Use the following format CHAIN:RESNUM (eg: 'A:
350'). Please, make sure that your selection is correct and based on GROMACS numbering in processed files.

```tip
These options allow gmx_MMPBSA to do the mutation. This way the user does not have to provide the mutant topology
```


### **`&nmode` namelist variables**

`dielc` Distance-dependent dielectric constant (Default = 1.0)

`drms` Convergence criteria for minimized energy gradient. (Default = 0.001)

`maxcyc` Maximum number of minimization cycles to use per snapshot in sander. (Default = 10000)

`nminterval``∗` Offset from which to choose frames to perform nmode calculations on (Default = 1)

`nmendframe``∗` Frame number to stop performing nmode calculations on (Default = 1000000)

`nmode_igb` Value for Generalized Born model to be used in calculations. Options are 0: Vacuum, 1: HCT GB model (Default

1)

`nmode_istrng` Ionic strength to use in nmode calculations. Units are Molarity. Non-zero values are ignored
if `nmode_igb`
is 0 above. (Default = 0.0)

`nmstartframe``∗` Frame number to begin performing nmode calculations on (Default = 1)

`*` _These variables will choose a subset of the frames chosen from the variables in the &general namelist. Thus, the
  “trajectory” from which snapshots will be chosen for nmode calculations will be the collection of snapshots upon which
  the other calculations were performed._

### **`&decomp` namelist variables**

`csv_format` Print the decomposition output in a Comma-Separated-Variable (CSV) file. CSV files open natively in most
spreadsheets. If set to 1, this variable will cause the data to be written out in a CSV file, and standard error of the
mean will be calculated and included for all data. If set to 0, the standard, ASCII format will be used for the output
file. Default is 1 (CSV-formatted output file)

`dec_verbose` Set the level of output to print in the decomp_output file. (Default = 0)

* 0: DELTA energy, total contribution only
* 1: DELTA energy, total, sidechain, and backbone contributions
* 2: Complex, Receptor, Ligand, and DELTA energies, total contribution only
* 3: Complex, Receptor, Ligand, and DELTA energies, total, sidechain, and backbone contributions

```note
If the values 0 or 2 are chosen, only the Total contributions are required, so only those will be printed to the
mdout files to cut down on the size of the mdout files and the time required to parse them.
```
Note: 

`idecomp` Energy decomposition scheme to use:

* 1: Per-residue decomp with 1-4 terms added to internal potential terms
* 2: Per-residue decomp with 1-4 EEL added to EEL and 1-4 VDW added to VDW potential terms.
* 3: Pairwise decomp with 1-4 terms added to internal potential terms
* 4: Pairwise decomp with 1-4 EEL added to EEL and 1-4 VDW added to VDW potential terms

```warning
(No default. This must be specified!) This functionality requires sander.
```

`print_res` Select residues from the complex to print. Default is print "within 6". This variable also accepts a
sequence of individual residues and/or ranges. The different fields must be either comma- or semicolon-delimited. For
example: print_res = "within 6", where _within_ corresponds to the keyword and _6_ to the maximum distance criterion in
Angstroms necessary to select the residues from both the receptor and the ligand; or print_res = “1, 3-10, 15, 100”, or
print_res = “1; 3-10; 15; 100”. Both of these will print residues 1, 3 through 10, 15, and 100 from the complex topology
file and the corresponding residues in either the ligand and/or receptor topology files.

```note
{:.text-red} 
Using idecomp=3 or 4 (pairwise) with a very large number of printed residues and a large number of 
frames can quickly create very, very large temporary mdout files. Large print selections also demand a large amount 
of memory to parse the mdout files and write decomposition output file (~500 MB for just 250 residues, since that’s 
62500 pairs!) It is not unusual for the output file to take a significant amount of time to print if you have a lot of
data. This is most applicable to pairwise decomp, since the amount of data scales as O(N 2 ).

{:.bg-green-light} 
Based on the above, we decided to add a new option that limits the selection of the residues that will be printed by 
default. The new option (within 6) considerably reduces the number of residues to be printed reducing the 
computational cost. Additionally, it selects the interaction interface residues (according to the selected value) 
automatically, without the user needing to define them explicitly.

```

### **`&rism` namelist variables**

```warning
3D-RISM calculations are performed with the rism3d.snglpnt program built with AmberTools, written by Tyler Luchko. 
It is the most expensive, yet most statistical mechanically rigorous solvation model available in MMPBSA.py. See 
[Chapter 7](https://ambermd.org/doc12/Amber20.pdf#chapter.7) for a more thorough description of options and theory. 
A list of references can be found there, too. One advantage of 3D-RISM is that an arbitrary solvent can be chosen; 
you just need to change the xvvfile specified on the command line 
(see [34.3.2](https://ambermd.org/doc12/Amber20.pdf#subsection.34.3.2)).
```

`buffer` Minimum distance between solute and edge of solvation box. Specify this with grdspc below. Mutually exclusive
with ng and solvbox. Set buffer < 0 if you wish to use ng and solvbox. (Default = 14 Å)
closure The approximation to the closure relation. Allowed choices are kh (Kovalenko-Hirata), hnc (Hypernetted- chain),
or psen (Partial Series Expansion of order-n) where “n” is a positive integer (_e.g._, “pse3”). (Default = ‘kh’)

`closureorder` (Deprecated) The order at which the PSE-n closure is truncated if closure is specified as “pse” or
“psen” (no integers). (Default = 1)

`grdspc` Grid spacing of the solvation box. Specify this with buffer above. Mutually exclusive with ng and solvbox.
(Default = 0.5 Å)

`ng` Number of grid points to use in the x, y, and z directions. Used only if buffer < 0. Mutually exclusive with buffer
and grdspc above, and paired with solvbox below. No default, this must be set if buffer < 0. Define like
“ng=1000,1000,1000”

`polardecomp` Decompose the solvation free energy into polar and non-polar contributions. Note that this will increase
computation time by roughly 80%. 0: Don’t decompose solvation free energy. 1: Decompose solvation free energy. (Default
= 0)

`rism_verbose` Level of output in temporary RISM output files. May be helpful for debugging or following con- vergence.
Allowed values are 0 (just print the final result), 1 (additionally prints the total number of iterations for each
solution), and 2 (additionally prints the residual for each iteration and details of the MDIIS solver).
(Default = 0)

`solvbox` Length of the solvation box in the x, y, and z dimensions. Used only if buffer < 0. Mutually exclusive with
buffer and grdspc above, and paired with ng above. No default, this must be set if buffer < 0. Define like
“solvbox=20,20,20”

`solvcut` Cutoff used for solute-solvent interactions. The default is the value of buffer. Therefore, if you set buffer
< 0 and specify ng and solvbox instead, you must set solvcut to a nonzero value or the program will quit in error. (
Default = buffer )

`thermo` Which thermodynamic equation you want to use to calculate solvation properties. Options are “std”, “gf”, or
“both” (case-INsensitive). “std” uses the standard closure relation, “gf” uses the Gaussian Fluctuation approximation,
and “both” will print out separate sections for both. (Default = “std”). Note that all data are printed out for each
RISM simulation, so no choice is any more computationally demanding than another. Also, you can change this option and
use the -rewrite-output flag to obtain a different printout after-the-fact.

`tolerance` Upper bound of the precision requirement used to determine convergence of the self-consistent solution. This
has a strong effect on the cost of 3D-RISM calculations. (Default = 1e-5).

## Sample input files

```note
You can refer to the [examples](../Examples/) to understand the input file in a practical way.
```

### GB and PB

```
Sample input file for GB and PB calculation
&general
startframe=5, endframe=100, interval=5,
verbose=2, protein_forcefield="oldff/leaprc.ff99SB", ligand_forcefield="leaprc.gaff",
/
&gb
igb=5, saltcon=0.150,
/
&pb
istrng=0.15, fillratio=4.0
/
```

### Alanine scanning

```
Sample input file for Alanine scanning
&general
startframe=5, endframe=21, verbose=2, interval=1,
protein_forcefield="oldff/leaprc.ff99SB", PBRadii=4
/
&gb
igb=8, saltcon=0.150, intdiel=10
/
&alanine_scanning
#make sure to change this parameter to 'ligand' is the mutation is going to be performed 
#in the ligand
mutant='receptor'
mutant_res='B:12'
/
```

### Entropy

```
Sample input file for entropy calculations
&general
#
startframe=5, endframe=21, verbose=2, interval=1,
#entropy variable control whether to perform a quasi-harmonic entropy (QH) approximation or the 
#Interaction Entropy (IE)(https://pubs.acs.org/doi/abs/10.1021/jacs.6b02682) approximation
protein_forcefield="oldff/leaprc.ff99SB", entropy=2, entropy_seg=25, entropy_temp=298
/
&gb
igb=2, saltcon=0.150,
/
#uncomment the next 4 lines for normal mode calculations
#&nmode
#nmstartframe=5, nmendframe=21, nminterval=2,
#maxcyc=50000, drms=0.0001,
#/
/
```

### Decomposition analysis

```
Sample input file with decomposition analysis
#make sure to include at least one residue from both the receptor
#and ligand in the print_res mask of the &decomp section.
#http://archive.ambermd.org/201308/0075.html
&general
startframe=5, endframe=21, interval=1,
/
&gb
igb=5, saltcon=0.150,
/
&decomp
idecomp=2, dec_verbose=3,
print_res="within 4"
#check _GMXMMPBSA_COM_FIXED.pdb file to select which residues are going to be printed
#in the output file
#print_res="40-41,44,47,78,81-82,85,88,115,118,122,215,218-220,232,241"
/
```

### QM/MMGBSA

```
Sample input file for QM/MMGBSA
&general
startframe=5, endframe=100, interval=5,
/
&gb
igb=5, saltcon=0.100, ifqnt=1, qmcharge_com=0,
qm_residues="100-105, 200", qm_theory="PM3"
/
```

### MM/3D-RISM

```
Sample input file for MM/3D-RISM
&general
startframe=20, endframe=100, interval=5,
/
&rism
polardecomp=1, thermo="gf"
/
```

### MMPBSA with membrane proteins

```
Sample input file for MMPBSA with membrane proteins
&general
startframe=1, endframe=100, interval=1, 
debug_printlevel=2, use_sander=1,
/
&pb
radiopt=0, indi=20.0, istrng=0.150,
fillratio=1.25, ipb=1, nfocus=1,
bcopt=10, eneopt=1, cutfd=7.0, cutnb=99.0,
npbverb=1, solvopt=2, inp=2,
memopt=1, emem=7.0, mctrdz=-10.383, mthick=36.086, poretype=1,
maxarcdot=15000
/
```

```note
Comments are allowed by placing a # at the beginning of the line (whites- pace
is ignored). Variable initialization may span multiple lines. In-line comments (_i.e._, putting a # for a comment after
a variable is initialized in the same line) is not allowed and will result in an input error. Variable declarations must
be comma-delimited, though all whitespace is ignored. Finally, all lines between namelists are ignored, so comments can
be added before each namelist without using #.
```