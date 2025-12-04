#all basic data info extraction from netcdf
import os
from netCDF4 import Dataset

# --- Your NetCDF file path ---
file_path = r"C:\Users\sdeep\OneDrive\Desktop\tar_nc_extraction\old_mum_tar\CDWRVRL-Level1B-IMDScan_BC-319-IMDScanB-2025-11-30-23_34_24\CDWRVRL-Level1B-IMDScan_BC-319-IMDScanB-2025-11-30-23_34_24.nc"

# --- Create output log path in same folder ---
folder = os.path.dirname(file_path)
file_name = os.path.basename(file_path).replace(".nc", "_log.txt")
log_file = os.path.join(folder, file_name)

# Open NetCDF file
nc = Dataset(file_path, mode='r')

with open(log_file, "w") as f:

    # Write file info
    f.write("=== FILE INFO ===\n")
    f.write(str(nc))
    f.write("\n\n")

    # Write dimensions
    f.write("=== DIMENSIONS ===\n")
    for dim in nc.dimensions.values():
        f.write(str(dim) + "\n")
    f.write("\n")

    # Write variables
    f.write("=== VARIABLES ===\n")
    for var_name, var in nc.variables.items():
        f.write(f"\nVariable: {var_name}\n")
        f.write(f"  Dimensions: {var.dimensions}\n")
        f.write(f"  Shape: {var.shape}\n")
        f.write(f"  Data type: {var.dtype}\n")
        if hasattr(var, "units"):
            f.write(f"  Units: {var.units}\n")

# Close file
nc.close()

print(f"Log file created successfully at:\n{log_file}")

