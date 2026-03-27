import os
import json
import pandas as pd

path = "data/aggregated/insurance/country/india/state"

data_list = []

for state in os.listdir(path):
    state_path = os.path.join(path, state)

    for year in os.listdir(state_path):
        year_path = os.path.join(state_path, year)

        for file in os.listdir(year_path):
            if file.endswith(".json"):
                file_path = os.path.join(year_path, file)

                with open(file_path, "r") as f:
                    data = json.load(f)

                    if "data" in data and data["data"]:
                        for item in data["data"]["transactionData"]:
                            data_list.append({
                                "state": state,
                                "year": int(year),
                                "quarter": int(file.strip(".json")),
                                "transaction_type": item["name"],
                                "count": item["paymentInstruments"][0]["count"],
                                "amount": item["paymentInstruments"][0]["amount"]
                            })

df = pd.DataFrame(data_list)

print(df.head())
print(df.shape)