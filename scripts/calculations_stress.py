import os
import pandas as pd
import csv

ccs_file = "results/carver_cluster_stress.csv"
df = pd.read_csv(ccs_file)

# calculate percentage of students with each stressor
for col in df.columns:
    if col.endswith("_count"):
        base = col.replace("_count", "")
        df[f"percent_{base}"] = df[col] / df["total_students"] * 100

# add a column for the school name
df["school"] = df["file"].str.replace("761 - ", "", regex=False)
df["school"] = df["school"].str.replace(".xls", "", regex=False)

df = df[["school", "file"] + [col for col in df.columns if col.startswith("percent_")]]

df = df.sort_values("school")

df.to_csv("results/final_carver_cluster_stress_data.csv", index=False)