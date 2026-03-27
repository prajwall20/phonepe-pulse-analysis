import os
import json
import pandas as pd

# -----------------------------
# INSURANCE DATA
# -----------------------------
insurance_path = "data/aggregated/insurance/country/india/state"
insurance_list = []

for state in os.listdir(insurance_path):
    for year in os.listdir(os.path.join(insurance_path, state)):
        for file in os.listdir(os.path.join(insurance_path, state, year)):
            if file.endswith(".json"):
                with open(os.path.join(insurance_path, state, year, file), "r") as f:
                    data = json.load(f)

                    if "data" in data and data["data"]:
                        for item in data["data"]["transactionData"]:
                            insurance_list.append({
                                "state": state,
                                "year": int(year),
                                "quarter": int(file.strip(".json")),
                                "type": item["name"],
                                "count": item["paymentInstruments"][0]["count"],
                                "amount": item["paymentInstruments"][0]["amount"]
                            })

insurance_df = pd.DataFrame(insurance_list)
insurance_df.to_csv("insurance_state.csv", index=False)
print("✅ Insurance:", insurance_df.shape)


# -----------------------------
# TRANSACTION DATA
# -----------------------------
transaction_path = "data/aggregated/transaction/country/india/state"
transaction_list = []

for state in os.listdir(transaction_path):
    for year in os.listdir(os.path.join(transaction_path, state)):
        for file in os.listdir(os.path.join(transaction_path, state, year)):
            if file.endswith(".json"):
                with open(os.path.join(transaction_path, state, year, file), "r") as f:
                    data = json.load(f)

                    if "data" in data and data["data"]:
                        for item in data["data"]["transactionData"]:
                            for inst in item["paymentInstruments"]:
                                transaction_list.append({
                                    "state": state,
                                    "year": int(year),
                                    "quarter": int(file.strip(".json")),
                                    "type": item["name"],
                                    "count": inst["count"],
                                    "amount": inst["amount"]
                                })

transaction_df = pd.DataFrame(transaction_list)
transaction_df.to_csv("transaction_state.csv", index=False)
print("✅ Transaction:", transaction_df.shape)


# -----------------------------
# USER DATA (FIXED)
# -----------------------------
user_path = "data/aggregated/user/country/india/state"
user_list = []

for state in os.listdir(user_path):
    for year in os.listdir(os.path.join(user_path, state)):
        for file in os.listdir(os.path.join(user_path, state, year)):
            if file.endswith(".json"):
                with open(os.path.join(user_path, state, year, file), "r") as f:
                    data = json.load(f)

                    # SAFE CHECK
                    if (
                        "data" in data and
                        data["data"] and
                        "usersByDevice" in data["data"] and
                        data["data"]["usersByDevice"] is not None
                    ):
                        for item in data["data"]["usersByDevice"]:
                            user_list.append({
                                "state": state,
                                "year": int(year),
                                "quarter": int(file.strip(".json")),
                                "brand": item.get("brand"),
                                "count": item.get("count"),
                                "percentage": item.get("percentage")
                            })

user_df = pd.DataFrame(user_list)
user_df.to_csv("user_state.csv", index=False)

print("✅ User:", user_df.shape)