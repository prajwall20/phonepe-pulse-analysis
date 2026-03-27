import os
import shutil

# Folder name
folder_name = "csv_data"

# Create folder if not exists
if not os.path.exists(folder_name):
    os.makedirs(folder_name)

# List of CSV files
files = [
    "insurance_state.csv",
    "transaction_state.csv",
    "user_state.csv",
    "top_transaction.csv",
    "top_user.csv",
    "top_insurance.csv",
    "map_transaction.csv",
    "map_user.csv",
    "map_insurance.csv"
]

# Move files
for file in files:
    if os.path.exists(file):
        shutil.move(file, os.path.join(folder_name, file))
        print(f"✅ Moved: {file}")
    else:
        print(f"❌ Not found: {file}")

print("\n🎯 All files organized into 'csv_data' folder")