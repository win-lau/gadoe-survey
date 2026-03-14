import os
import pandas as pd
import csv

DATA_DIR = "results/data"
OUTPUT_FILE = "results/summary_housing.csv"

results = []

for file in os.listdir(DATA_DIR):

    if file.endswith(".xls"):

        path = os.path.join(DATA_DIR, file)

        try:

            df = pd.read_excel(
                path,
                sheet_name="Survey Results",
                header=None
            )

            housing_count = int(str(df.iloc[473, 15]).replace(",", ""))
            total_students = int(str(df.iloc[476, 15]).replace(",", ""))

            results.append([
                file,
                housing_count,
                total_students
            ])

        except Exception as e:

            print("Error processing:", file, e)

with open(OUTPUT_FILE, "w", newline="") as f:

    writer = csv.writer(f)

    writer.writerow([
        "file",
        "housing_concern_count",
        "total_students"
    ])

    writer.writerows(results)

print("Extraction complete.")