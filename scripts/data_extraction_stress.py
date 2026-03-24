import os
import pandas as pd
import csv

DATA_DIR = "results/data"
OUTPUT_FILE = "results/carver_cluster_stress.csv"

results = []

for file in os.listdir(DATA_DIR):

    if file.endswith(".xls") and (
    "Sylvan Hills Middle School" in file or
    "Carver High School" in file):

        path = os.path.join(DATA_DIR, file)

        try:

            df = pd.read_excel(
                path,
                sheet_name="Survey Results",
                header=None
            )

            school_work_count = int(str(df.iloc[465, 15]).replace(",", ""))
            peer_problems_count = int(str(df.iloc[466, 15]).replace(",", ""))
            social_media_count = int(str(df.iloc[467, 15]).replace(",", ""))
            family_reasons_count = int(str(df.iloc[468, 15]).replace(",", ""))
            bullied_count = int(str(df.iloc[469, 15]).replace(",", ""))
            school_grades_count = int(str(df.iloc[470, 15]).replace(",", ""))
            partner_problems_count = int(str(df.iloc[471, 15]).replace(",", ""))
            covid_count = int(str(df.iloc[472, 15]).replace(",", ""))
            housing_count = int(str(df.iloc[473, 15]).replace(",", ""))
            other_count = int(str(df.iloc[474, 15]).replace(",", ""))
            none_count = int(str(df.iloc[475, 15]).replace(",", ""))
            total_students = int(str(df.iloc[476, 15]).replace(",", ""))

            results.append([
                file,
                school_work_count,
                peer_problems_count,
                social_media_count,
                family_reasons_count,
                bullied_count,
                school_grades_count,
                partner_problems_count,
                covid_count,
                housing_count,
                other_count,
                none_count,
                total_students
            ])

        except Exception as e:

            print("Error processing:", file, e)

with open(OUTPUT_FILE, "w", newline="") as f:

    writer = csv.writer(f)

    writer.writerow([
        "file",
        "school_work_count",
        "peer_problems_count",
        "social_media_count",
        "family_reasons_count",
        "bully_count",
        "school_grades_count",
        "partner_problems_count",
        "covid_count",
        "housing_count",
        "other_count",
        "none_count",
        "total_students"
    ])

    writer.writerows(results)

print("Extraction complete.")