---
sort: 2
---

# Release history

## Upcoming release
### Additions
* Documentation at Github pages

### Fixes
* Alanine scanning tutorial 


## [gmx_MMPBSA v1.2.0](https://github.com/Valdes-Tresanco-MS/gmx_MMPBSA/releases/tag/v1.2.0)
### Additions

* New ligand force field (Zwitterionic aminoacids)
* A new flag (-cr) added for defining a reference structure (guarantee a better consintency in generated PDB files)
* API documentation

### Fixes
* More comprehensive output log file
* Best handling of structure files

### Changes
gmx editconf is used to generate PDB files instead of gmx trjconv (#14)
gmx_MMPBSA data is copied in AMBER as an independent folder
*gro files can be used as a MD Structure+mass(db) file
Updated tutorial list in README (Protein_DNA_RNA_Ion_ligand BFE calculations)

## [gmx_MMPBSA v1.1.1](https://github.com/Valdes-Tresanco-MS/gmx_MMPBSA/releases/tag/v1.1.1)
### Additions
* New tutorial added (see Protein_DNA_RNA_Ion_ligand tutorial)
 
### Fixes
* Support various metallo-complexes formats

### Changes
* Keep all the temporary files in the folder for debugging purposes

## [gxm_MMPBSA v.1.1.0](https://github.com/Valdes-Tresanco-MS/gmx_MMPBSA/releases/tag/v.1.1.0)
### Additions
* Now supports carbohydrates as ligand. See this tutorial 
* Now supports metalloprotein-ligand complexes. See this tutorial.
* We have added data folder to gmx_MMPBSA module. This folder contains the GLYCAM_06h-1 force field files 
  (Compatible with amber99sb and early, see at http://glycam.org) which is not in AmberTools.

### Fixes
* Minor bugs

### Changes
* We changed the notation of the force fields, now the user can define any force field (We have only tested Amber and 
GLYCAM force fields) available in AmberTools. Charmm is not yet supported. See this section

## [gxm_MMPBSA first release](https://github.com/Valdes-Tresanco-MS/gmx_MMPBSA/releases/tag/v1.0.0)
**This version includes:**

* Compatibility with different Gromacs versions
* Support for all types of calculations available in MMPBSA.py
* Graphical user interface for results analysis (gmx_MMPBSA_gui)
* API modified to get more information
* Some new facilities and types of calculations