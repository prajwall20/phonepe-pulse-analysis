import os
import json
import pandas as pd

# -----------------------------
# TOP TRANSACTION DATA
# -----------------------------
path = "data/top/transaction/country/india/state"
data_list = []

for state in os.listdir(path):
    for year in os.listdir(os.path.join(path, state)):
        for file in os.listdir(os.path.join(path, state, year)):
            if file.endswith(".json"):
                with open(os.path.join(path, state, year, file), "r") as f:
                    data = json.load(f)

                    if "data" in data and data["data"]:

                        # TOP DISTRICTS
                        if "districts" in data["data"]:
                            for item in data["data"]["districts"]:
                                data_list.append({
                                    "state": state,
                                    "year": int(year),
                                    "quarter": int(file.strip(".json")),
                                    "type": "district",
                                    "name": item["entityName"],
                                    "count": item["metric"]["count"],
                                    "amount": item["metric"]["amount"]
                                })

                        # TOP PINCODES
                        if "pincodes" in data["data"]:
                            for item in data["data"]["pincodes"]:
                                data_list.append({
                                    "state": state,
                                    "year": int(year),
                                    "quarter": int(file.strip(".json")),
                                    "type": "pincode",
                                    "name": item["entityName"],
                                    "count": item["metric"]["count"],
                                    "amount": item["metric"]["amount"]
                                })

df = pd.DataFrame(data_list)

# Save CSV
df.to_csv("top_transaction.csv", index=False)

print("✅ Top Transaction:", df.shape)