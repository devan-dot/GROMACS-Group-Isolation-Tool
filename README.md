- Python3 script that can be used in the extraction and centering of a selected index group from GROMACS files.
- Following file formats can be selected: .pdb, .gro, .xtc and  .tpr
- The script uses gmx trjconv to generate  files containing only the selected group. Output files are named as <group_name>_only.<ext>
- Requirements are :
1) Original files that need to be convereted.
2) A gmx index file that contains the required group that needs to be selected
3) Parent tpr file system topology, coordinates, and box info.
- Dependencies
1) Python: 3.8 or higher
2) GROMACS: 2021, 2022, or 2023 
3) OS: Linux/macOS 
