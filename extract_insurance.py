import os
import json
import pandas as pd

# Path to insurance data
path = "data/aggregated/insurance/country/india"

data_list = []

# Loop through years
for year in os.listdir(path):
    year_path = os.path.join(path, year)

    # Loop through quarters (json files)
    for file in os.listdir(year_path):
        if file.endswith(".json"):
            file_path = os.path.join(year_path, file)

            with open(file_path, "r") as f:
                data = json.load(f)

                # Extract data safely
                if "data" in data and data["data"]:
                    for item in data["data"]["transactionData"]:
                        data_list.append({
                            "year": int(year),
                            "quarter": int(file.strip(".json")),
                            "transaction_type": item["name"],
                            "count": item["paymentInstruments"][0]["count"],
                            "amount": item["paymentInstruments"][0]["amount"]
                        })

# Convert to DataFrame
df = pd.DataFrame(data_list)

print(df.head())
print(df.shape)