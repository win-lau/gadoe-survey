import os
import pandas as pd
import csv

summary_file = "results/summary_housing.csv"
df = pd.read_csv(summary_file)

# calculate percentage of students with housing concerns
df["percent_housing_concern"] = df["housing_concern_count"] / df["total_students"] * 100

# add a column for the school name
df["school"] = df["file"].str.replace("761 - ", "", regex=False)
df["school"] = df["school"].str.replace(".xls", "", regex=False)

df = df[["school", "file", "housing_concern_count", "total_students", "percent_housing_concern"]]

df.to_csv("results/final_housing_data.csv", index=False)