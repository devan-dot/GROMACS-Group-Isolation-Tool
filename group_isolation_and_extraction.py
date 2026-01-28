#!/usr/bin/env python3

import os
import sys
import subprocess

# ============================================================
# To check file exists
# ============================================================
def check_file(path, description):
    if not os.path.isfile(path):
        print(f"Error: {description} not found -> {path}")
        sys.exit(1)

# ============================================================
# To get group names from index file
# ============================================================
def parse_index_groups(index_file):
    groups = {}
    with open(index_file) as f:
        number = -1
        for line in f:
            line = line.strip()
            if line.startswith('[') and line.endswith(']'):
                number += 1
                name = line.strip('[]').strip()
                groups[str(number)] = name
    return groups

# ============================================================
# To know which file types to process
# ============================================================
print("\nSelect which file types you want to process:")
print("1 = XTC trajectory")
print("2 = GRO structure")
print("3 = PDB structure")
print("4 = TPR structure (single frame)")

choices = input("Enter numbers separated by commas (example: 1,2 or 1,2,3,4): ").split(',')
choices = [c.strip() for c in choices]

valid = {'1', '2', '3', '4'}
if not all(c in valid for c in choices):
    print("Invalid selection.")
    sys.exit(1)

# ============================================================
# To get base files for selected filetypes
# ============================================================
tpr_file = input("\nEnter TPR file (required for centering): ").strip()
index_file = input("Enter index file (.ndx): ").strip()

check_file(tpr_file, "TPR file")
check_file(index_file, "Index file")

groups = parse_index_groups(index_file)

print("\nAvailable index groups:")
for num, name in groups.items():
    print(f"{num} = {name}")

group_number = input("\nEnter group number to center and extract: ").strip()

if group_number not in groups:
    print("Invalid group number.")
    sys.exit(1)

group_name = groups[group_number].replace(" ", "_")
print(f"Selected group: {group_name}")

# ============================================================
# TRJCONV
# ============================================================
def run_trjconv(input_file, output_file):
    cmd = [
        "gmx", "trjconv",
        "-s", tpr_file,
        "-f", input_file,
        "-n", index_file,
        "-o", output_file,
        "-center",
        "-pbc", "mol"
    ]

    print("\nRunning:", " ".join(cmd))

    process = subprocess.Popen(
        cmd,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    stdout, stderr = process.communicate(input=f"{group_number}\n{group_number}\n")

    if process.returncode != 0:
        print(stderr)
        sys.exit(1)

    print(f"Finished -> {output_file}")

# ============================================================
# To collect filenames FIRST 
# ============================================================
xtc = gro = pdb = None

print("\nEnter input filenames for the selected file types:")

if '1' in choices:
    xtc = input("XTC file: ").strip()

if '2' in choices:
    gro = input("GRO file: ").strip()

if '3' in choices:
    pdb = input("PDB file: ").strip()

# TPR does not need a filename prompt because it uses the base TPR

# ============================================================
# Run processing
# ============================================================
if xtc:
    check_file(xtc, "XTC file")
    run_trjconv(xtc, f"{group_name}_only.xtc")

if gro:
    check_file(gro, "GRO file")
    run_trjconv(gro, f"{group_name}_only.gro")

if pdb:
    check_file(pdb, "PDB file")
    run_trjconv(pdb, f"{group_name}_only.pdb")

if '4' in choices:
    print("\nProcessing TPR as structure input (single frame)")
    run_trjconv(tpr_file, f"{group_name}_only.pdb")

print("\nAll selected operations completed successfully.")
print("\nVisit https://github.com/devan-dot?tab=repositories for ore information.")


