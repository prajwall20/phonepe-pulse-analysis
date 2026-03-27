import os
import json
import pandas as pd

# -----------------------------
# MAP TRANSACTION
# -----------------------------
path_txn = "data/map/transaction/hover/country/india/state"
txn_list = []

for state in os.listdir(path_txn):
    for year in os.listdir(os.path.join(path_txn, state)):
        for file in os.listdir(os.path.join(path_txn, state, year)):
            if file.endswith(".json"):
                with open(os.path.join(path_txn, state, year, file), "r") as f:
                    data = json.load(f)

                    if data.get("data") and data["data"].get("hoverData"):
                        for district, val in data["data"]["hoverData"].items():
                            txn_list.append({
                                "state": state,
                                "year": int(year),
                                "quarter": int(file.strip(".json")),
                                "district": district,
                                "count": val["count"],
                                "amount": val["amount"]
                            })

txn_df = pd.DataFrame(txn_list)
txn_df.to_csv("map_transaction.csv", index=False)
print("✅ Map Transaction:", txn_df.shape)


# -----------------------------
# MAP USER
# -----------------------------
path_user = "data/map/user/hover/country/india/state"
user_list = []

for state in os.listdir(path_user):
    for year in os.listdir(os.path.join(path_user, state)):
        for file in os.listdir(os.path.join(path_user, state, year)):
            if file.endswith(".json"):
                with open(os.path.join(path_user, state, year, file), "r") as f:
                    data = json.load(f)

                    if data.get("data") and data["data"].get("hoverData"):
                        for district, val in data["data"]["hoverData"].items():
                            user_list.append({
                                "state": state,
                                "year": int(year),
                                "quarter": int(file.strip(".json")),
                                "district": district,
                                "registered_users": val.get("registeredUsers"),
                                "app_opens": val.get("appOpens")
                            })

user_df = pd.DataFrame(user_list)
user_df.to_csv("map_user.csv", index=False)
print("✅ Map User:", user_df.shape)


# -----------------------------
# MAP INSURANCE
# -----------------------------
path_ins = "data/map/insurance/hover/country/india/state"
ins_list = []

for state in os.listdir(path_ins):
    for year in os.listdir(os.path.join(path_ins, state)):
        for file in os.listdir(os.path.join(path_ins, state, year)):
            if file.endswith(".json"):
                with open(os.path.join(path_ins, state, year, file), "r") as f:
                    data = json.load(f)

                    if data.get("data") and data["data"].get("hoverData"):
                        for district, val in data["data"]["hoverData"].items():
                            ins_list.append({
                                "state": state,
                                "year": int(year),
                                "quarter": int(file.strip(".json")),
                                "district": district,
                                "count": val["count"],
                                "amount": val["amount"]
                            })

ins_df = pd.DataFrame(ins_list)
ins_df.to_csv("map_insurance.csv", index=False)
print("✅ Map Insurance:", ins_df.shape)