#!/usr/bin/env python3
"""
Cross-match TIC IDs/sectors/cadence and copy matching PNG light curve plots
to a new output folder.

Usage:
    python copy_tic_plots.py

Edit SOURCE_DIR and OUTPUT_DIR below to match your paths.
"""

import os
import shutil


SOURCE_DIR = os.path.expanduser("~/Downloads")   # folder containing your PNGs
OUTPUT_DIR = os.path.expanduser("~/Downloads/matched_lightcurves")  # destination


# Target list: (TIC_id, sector, cadence)
TARGETS = [
    (677945, 91, "fast"),
    (706595, 91, "slow"),
    (709015, 91, "slow"),
    (741119, 91, "slow"),
    (741596, 91, "slow"),
    (771548, 91, "fast"),
    (771548, 91, "slow"),
    (857186, 92, "slow"),
    (1003831, 8, "slow"),
    (1003831, 34, "slow"),
    (1042868, 21, "slow"),
    (1042868, 48, "slow"),
    (1129033, 4, "slow"),
    (1129033, 31, "fast"),
    (1167538, 5, "slow"),
    (1167538, 31, "slow"),
    (1167538, 32, "slow"),
    (1528696, 5, "slow"),
    (1528696, 32, "fast"),
    (2468648, 92, "slow"),
    (2521105, 91, "fast"),
    (2621212, 91, "fast"),
    (2621212, 91, "slow"),
    (2760219, 29, "slow"),
    (2760219, 69, "slow"),
    (2760219, 96, "slow"),
    (2764004, 91, "slow"),
    (4070275, 32, "slow"),
    (4610830, 42, "fast"),
    (4610830, 42, "slow"),
    (4610830, 70, "slow"),
    (4616072, 6, "slow"),
    (4616072, 7, "slow"),
    (4616072, 33, "fast"),
    (4616072, 33, "slow"),
    (4616072, 87, "slow"),
    (4672985, 31, "fast"),
    (4672985, 31, "slow"),
    (4918918, 21, "slow"),
    (4918918, 48, "slow"),
    (5882269, 43, "slow"),
    (5882269, 45, "slow"),
    (6139066, 43, "slow"),
    (6139066, 44, "slow"),
    (6139066, 45, "slow"),
    (6139066, 71, "slow"),
    (6663331, 13, "slow"),
    (6663331, 67, "slow"),
    (6663331, 94, "slow"),
    (6892385, 44, "slow"),
    (6892385, 45, "slow"),
    (6892385, 46, "slow"),
    (6892385, 71, "slow"),
    (6892385, 72, "slow"),
    (6893917, 45, "slow"),
    (6893917, 46, "slow"),
    (6893917, 71, "fast"),
    (6893917, 71, "slow"),
    (6893917, 72, "fast"),
    (7020254, 7, "slow"),
    (7020254, 34, "fast"),
    (7020254, 34, "slow"),
    (7020254, 45, "slow"),
    (7020254, 46, "slow"),
    (7020254, 71, "slow"),
    (7020254, 72, "slow"),
    (7059054, 44, "slow"),
    (7059054, 45, "slow"),
    (7059054, 46, "slow"),
    (7088246, 13, "slow"),
    (7088246, 67, "slow"),
    (7088246, 94, "slow"),
    (7422496, 5, "slow"),
    (7422496, 6, "slow"),
    (7422496, 31, "slow"),
    (7422496, 32, "slow"),
    (7422496, 33, "slow"),
    (7422496, 87, "slow"),
    (7548817, 40, "slow"),
    (7548817, 52, "slow"),
    (7548817, 54, "slow"),
    (7548817, 74, "slow"),
    (7548817, 79, "slow"),
    (7548817, 80, "slow"),
    (7548817, 81, "slow"),
    (8348911, 24, "slow"),
    (8348911, 25, "slow"),
    (8348911, 51, "slow"),
    (8348911, 52, "slow"),
    (8348911, 79, "slow"),
    (8400842, 19, "slow"),
    (8400842, 59, "fast"),
    (8400842, 59, "slow"),
    (8400842, 73, "fast"),
    (8400842, 86, "fast"),
    (8400842, 86, "slow"),
    (8516795, 40, "slow"),
    (8516795, 53, "slow"),
    (8516795, 54, "slow"),
    (8516795, 80, "slow"),
    (8599009, 80, "fast"),
    (8599009, 80, "slow"),
    (8918021, 42, "slow"),
    (8918021, 70, "slow"),
    (8918021, 92, "slow"),
    (8963531, 42, "slow"),
    (8963531, 70, "slow"),
    (8963531, 92, "slow"),
    (8967242, 22, "slow"),
    (8967242, 48, "fast"),
    (8967242, 48, "slow"),
    (9006668, 29, "fast"),
    (9006668, 29, "slow"),
    (9006668, 69, "fast"),
    (9006668, 69, "slow"),
    (9006668, 96, "fast"),
    (9006668, 96, "slow"),
    (9030096, 42, "slow"),
    (9030096, 70, "slow"),
    (9030096, 92, "slow"),
    (9030119, 42, "slow"),
    (9030119, 70, "slow"),
    (9030119, 92, "slow"),
    (9054633, 42, "slow"),
    (9054633, 70, "slow"),
    (9054633, 92, "slow"),
    (9155187, 47, "slow"),
    (9155187, 60, "slow"),
    (9385460, 64, "slow"),
    (9443323, 59, "slow"),
    (9443323, 73, "slow"),
    (9443323, 86, "slow"),
    (10195089, 92, "fast"),
]


def build_filename(tic, sector, cadence):
    """Construct expected PNG filename from TIC id, sector, and cadence."""
    return f"TIC{tic}_sector{sector}_cadence{cadence}_lightcurve.png"


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Build a lookup set of all PNG files in the source directory (recursive)
    print(f"Scanning source directory: {SOURCE_DIR}")
    all_files = {}
    for root, _, files in os.walk(SOURCE_DIR):
        for f in files:
            if f.lower().endswith(".png"):
                all_files[f] = os.path.join(root, f)
    print(f"  Found {len(all_files)} PNG files total.\n")

    copied, missing = [], []

    for tic, sector, cadence in TARGETS:
        fname = build_filename(tic, sector, cadence)
        if fname in all_files:
            src = all_files[fname]
            dst = os.path.join(OUTPUT_DIR, fname)
            shutil.copy2(src, dst)
            copied.append(fname)
            print(f"  ✔  Copied: {fname}")
        else:
            missing.append(fname)
            print(f"  ✗  NOT FOUND: {fname}")

    print(f"\n{'='*60}")
    print(f"Done. Copied {len(copied)}/{len(TARGETS)} files to:\n  {OUTPUT_DIR}")
    if missing:
        print(f"\nMissing ({len(missing)} files):")
        for m in missing:
            print(f"  {m}")


if __name__ == "__main__":
    main()
