import os
import csv
import numpy as np
from netCDF4 import Dataset

# ----------------------------------------------------------
# INPUT NC FILE
# ----------------------------------------------------------
file_path = r"C:\Users\sdeep\OneDrive\Desktop\tar_nc_extraction\old_mum_tar\CDWRVRL-Level1B-IMDScan_BC-319-IMDScanB-2025-11-30-23_34_24\CDWRVRL-Level1B-IMDScan_BC-319-IMDScanB-2025-11-30-23_34_24.nc"

base_folder = os.path.dirname(file_path)
output_folder = os.path.join(base_folder, "Extracted_Variables_CSV")
os.makedirs(output_folder, exist_ok=True)

nc = Dataset(file_path, "r")

print("\nExtracting all variables...\n")

for var_name, var in nc.variables.items():

    data = var[:]
    csv_path = os.path.join(output_folder, f"{var_name}.csv")

    print(f"Saving {var_name}  -->  {csv_path}")

    # ============================================================
    # CASE 1: 3-D variables  (Elevation, Azimuth, RangeBins)
    # ============================================================
    if data.ndim == 3 and data.shape == (10, 360, 1659):

        with open(csv_path, "w", newline='') as f:
            writer = csv.writer(f)

            # Header
            header = ["Elevation", "Azimuth"] + [f"RangeBin_{i}" for i in range(data.shape[2])]
            writer.writerow(header)

            # Loop through all elevation & azimuth
            for elev in range(data.shape[0]):
                for azi in range(data.shape[1]):
                    row = [elev, azi] + list(data[elev, azi, :])
                    writer.writerow(row)

    # ============================================================
    # CASE 2: 2-D variables  (Elevation, Azimuth)
    # ============================================================
    elif data.ndim == 2 and data.shape == (10, 360):

        with open(csv_path, "w", newline='') as f:
            writer = csv.writer(f)

            writer.writerow(["Elevation", "Azimuth", var_name])

            for elev in range(10):
                for azi in range(360):
                    writer.writerow([elev, azi, data[elev, azi]])

    # ============================================================
    # CASE 3: 1-D variables
    # ============================================================
    elif data.ndim == 1:

        with open(csv_path, "w", newline='') as f:
            writer = csv.writer(f)

            writer.writerow([var_name])

            for val in data:
                writer.writerow([val])

    # ============================================================
    # CASE 4: Empty variables
    # ============================================================
    elif data.size == 0:

        with open(csv_path, "w", newline='') as f:
            f.write("EMPTY VARIABLE (size=0)\n")

    # ============================================================
    # CASE 5: Fallback for unknown shapes
    # ============================================================
    else:

        with open(csv_path, "w", newline='') as f:
            f.write(f"Unsupported shape: {data.shape}\n")

print("\nAll variables extracted successfully!")
print(f"Extracted CSV folder: {output_folder}")
