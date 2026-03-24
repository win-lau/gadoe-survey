import os
import pandas as pd
import csv

summary_file = "results/summary_housing_carver_tsa.csv"
df = pd.read_csv(summary_file)

# calculate percentage of students with housing concerns
df["percent_housing_concern"] = df["housing_concern_count"] / df["total_students"] * 100

# add a column for the school name
df["school"] = df["file"].str.replace("2022_761 - ", "", regex=False)
df["school"] = df["school"].str.replace("2023_761 - ", "", regex=False)
df["school"] = df["school"].str.replace("2024_761 - ", "", regex=False)
df["school"] = df["school"].str.replace(".xls", "", regex=False)
df["school"] = df["school"].str.replace("G.W. ", "", regex=False)

# add a column for the year
df["year"] = df["file"].str.extract(r"(\d{4})").astype(int)

df = df[["year", "school", "file", "housing_concern_count", "total_students", "percent_housing_concern"]]

df = df.sort_values(["school", "year"])

df.to_csv("results/final_housing_data_carver_tsa.csv", index=False)