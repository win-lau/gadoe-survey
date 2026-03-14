import os
import csv
import requests
import pandas as pd
import re
from io import BytesIO
from playwright.sync_api import sync_playwright


# setup and define variables
URL = "https://apps.gadoe.org/GSHSSurveyResults/Pages/default.aspx"

KEYWORD = "housing"
SHEET_NAME = "Survey Results"

RESULT_DIR = "results"
KEEP_DIR = f"{RESULT_DIR}/data"

os.makedirs(KEEP_DIR, exist_ok=True)


# function to scrape excel links from the website
def get_excel_links(year, system):

    links = []

    with sync_playwright() as p:

        browser = p.chromium.launch(headless=False, slow_mo=400)
        page = browser.new_page()

        page.goto(URL)

        # open tree nodes
        page.get_by_role("link", name=year).click()
        page.locator("text=School-Level Results").locator("xpath=preceding::img[1]").click()
        page.wait_for_selector("text=System School")
        page.locator(f"text=System School: {system}").locator("xpath=preceding::img[1]").click()

        page.wait_for_timeout(2000)

        system_node = page.locator(f"text=System School: {system}").first
        nodes = system_node.locator("xpath=following::*").all()

        for node in nodes:

            text = node.inner_text()

            if text.startswith("System School:"):
                break

            if ".xls" in text or ".xlsx" in text:

                href = node.get_attribute("href")

                if href:
                    match = re.search(r"window.open\('([^']+)'", href)
                    if match:
                        links.append(match.group(1))

        browser.close()

    return links


# function to download and process excel files, looking for keyword matches
def process_files(urls):

    kept, ignored, mentions = [], [], []

    for url in urls:

        filename = url.split("/")[-1]
        print("Checking:", filename)

        try:

            r = requests.get(url)
            df = pd.read_excel(BytesIO(r.content), sheet_name=SHEET_NAME, dtype=str)

            found = False

            for col in df.columns:

                matches = df[col].str.contains(KEYWORD, case=False, na=False)

                if matches.any():

                    found = True
                    rows = df[matches]

                    for idx, val in rows[col].items():
                        mentions.append([filename, SHEET_NAME, idx, col, val])

            if found:

                save_path = os.path.join(KEEP_DIR, filename)

                with open(save_path, "wb") as f:
                    f.write(r.content)

                kept.append(filename)
                print("Saved:", filename)

            else:
                ignored.append(filename)

        except Exception as e:

            print("Error processing:", filename, e)
            ignored.append(filename)

    return kept, ignored, mentions


# function to write results to CSV files
def write_csv(file, rows, header):

    with open(file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(rows)


# execute pipeline (edit parameters as needed)
if __name__ == "__main__":

    links = get_excel_links("2024", "Atlanta Public Schools")

    kept, ignored, mentions = process_files(links)

    write_csv(f"{RESULT_DIR}/kept_files.csv", [[k] for k in kept], ["file_name"])
    write_csv(f"{RESULT_DIR}/ignored_files.csv", [[i] for i in ignored], ["file_name"])
    write_csv(
        f"{RESULT_DIR}/housing_mentions.csv",
        mentions,
        ["file", "sheet", "row", "column", "matched_text"]
    )

    print("Pipeline complete.")