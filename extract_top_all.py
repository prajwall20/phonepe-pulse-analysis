import os
import json
import pandas as pd

# -----------------------------
# TOP TRANSACTION
# -----------------------------
path_txn = "data/top/transaction/country/india/state"
txn_list = []

for state in os.listdir(path_txn):
    for year in os.listdir(os.path.join(path_txn, state)):
        for file in os.listdir(os.path.join(path_txn, state, year)):
            if file.endswith(".json"):
                with open(os.path.join(path_txn, state, year, file), "r") as f:
                    data = json.load(f)

                    if data.get("data"):
                        for key in ["districts", "pincodes"]:
                            if key in data["data"]:
                                for item in data["data"][key]:
                                    txn_list.append({
                                        "state": state,
                                        "year": int(year),
                                        "quarter": int(file.strip(".json")),
                                        "type": key[:-1],
                                        "name": item["entityName"],
                                        "count": item["metric"]["count"],
                                        "amount": item["metric"]["amount"]
                                    })

txn_df = pd.DataFrame(txn_list)
txn_df.to_csv("top_transaction.csv", index=False)
print("✅ Top Transaction:", txn_df.shape)


# -----------------------------
# TOP USER
# -----------------------------
path_user = "data/top/user/country/india/state"
user_list = []

for state in os.listdir(path_user):
    for year in os.listdir(os.path.join(path_user, state)):
        for file in os.listdir(os.path.join(path_user, state, year)):
            if file.endswith(".json"):
                with open(os.path.join(path_user, state, year, file), "r") as f:
                    data = json.load(f)

                    if data.get("data"):
                        for key in ["districts", "pincodes"]:
                            if key in data["data"]:
                                for item in data["data"][key]:
                                    user_list.append({
                                        "state": state,
                                        "year": int(year),
                                        "quarter": int(file.strip(".json")),
                                        "type": key[:-1],
                                        "name": item["name"],
                                        "count": item["registeredUsers"]
                                    })

user_df = pd.DataFrame(user_list)
user_df.to_csv("top_user.csv", index=False)
print("✅ Top User:", user_df.shape)


# -----------------------------
# TOP INSURANCE
# -----------------------------
path_ins = "data/top/insurance/country/india/state"
ins_list = []

for state in os.listdir(path_ins):
    for year in os.listdir(os.path.join(path_ins, state)):
        for file in os.listdir(os.path.join(path_ins, state, year)):
            if file.endswith(".json"):
                with open(os.path.join(path_ins, state, year, file), "r") as f:
                    data = json.load(f)

                    if data.get("data"):
                        for key in ["districts", "pincodes"]:
                            if key in data["data"]:
                                for item in data["data"][key]:
                                    ins_list.append({
                                        "state": state,
                                        "year": int(year),
                                        "quarter": int(file.strip(".json")),
                                        "type": key[:-1],
                                        "name": item["entityName"],
                                        "count": item["metric"]["count"],
                                        "amount": item["metric"]["amount"]
                                    })

ins_df = pd.DataFrame(ins_list)
ins_df.to_csv("top_insurance.csv", index=False)
print("✅ Top Insurance:", ins_df.shape)