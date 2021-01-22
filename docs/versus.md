---
sort: 3
---

# Comparison of `gmx_MMPBSA` vs other programs
This comparison is based on the documentation of the different programs

| Feature | [g_mmpbsa](https://github.com/RashmiKumari/g_mmpbsa) | [GMXPBSA 2.1](https://github.com/aspitaleri/gmxpbsa) | [MMPBSA.py](https://ambermd.org/doc12/Amber20.pdf#chapter.34) <sup>1</sup> | [gmx_MMPBSA](https://github.com/Valdes-Tresanco-MS/gmx_MMPBSA/) |
|:---|:---:|:---:|:---:|:---:|
| **Normal binding free energies**| PB | PB | PB and GB | PB and GB |
| GB models |  |  | 1, 2, 3, 5, 7 and 8  | 1, 2, 3, 5, 7 and 8 |
| **Stability** |  | | ✔️  | ✔️  |
| **Alanine scanning** | ✔️  <sup>2</sup> | ✔️  | ✔️  | ✔️  |
| **Entropy corrections** <sup>3</sup>|  |  | nmode and qh | nmode, qh, and IE |
| **Decomposition schemes** | Per-Residues | | Per-Residues and Per-Wise | Per-Residues and Per-Wise |
| **QM/MMGBSA** |   | | ✔️  | ✔️  |
| **MM/3D-RISM** |   | | ✔️  | ✔️  |
| **Membrane Protein MMPBSA** |   |   | ✔️  | ✔️  |
| **GROMACS Version** | 4.x, 5.x and 2016+ <sup>4</sup> | 4.x, 5.x and 20xx.x <sup>5</sup> | --- | 4.x, 5.x and 20xx.x |
| **Approximations** | ST | ST | ST and MT | ST and MT |
| **API** |     | | ✔️  | ✔️  |
| **Graphical Analyzer** |   | |  | ✔️  |
| Energy to PDB | ✔️  |   |  | ✔️  |
| Energetic Terms charts | Per-Frame | Per-Frame | Average (dat file) / Average and Per-Frame (API) <sup>6</sup>  | Average and Per-frame |
| Energetic Terms charts representation | xmgrace/ matplotlib/ gnuplot | xmgrace/ matplotlib/ gnuplot | API and graphics library | gmx_MMPBSA_gui |
| **Externals programs** | APBS (1.2.x, 1.3.x or 1.4.x) | APBS (1.x.x) <sup>7</sup> |  AmberTools20 | AmberTools20 |
| **Parallel computation** | Depends on APBS version | ✔️  | ✔️  | ✔️  |
| **Steps for:** | | | | |
| Calculation and Summary | Multiple | Multiple | One | One |
| Analysis| Multiple | Multiple | Multiple | One |

<sup>1</sup> MMPBSA.py is included in AMBER package.

<sup>2</sup> Without documentation.

<sup>3</sup> nmode = Normal modes approximation, qh = Quasic-Harmony approximation and IE = Interaction Entropy
approximation

<sup>4</sup> GROMACS 20xx.x is not officially supported. There is a Pull Request that offers a minimum of compatibility 
with versions higher than 2016.x but with limitations 

<sup>5</sup> It is not clear if it supports the GROMACS versions 20xx, but we assume that it does because 
it is 
script-based.

<sup>6</sup>The user can obtain each energetic term per frame or its average values using the API. This means that
 user must be familiar with Python to handle the API, perform custom calculations or graph such data.

<sup>7</sup> It is not clear if it supports the APBS versions 3.x.x , but we assume that it does because it is 
script-based.