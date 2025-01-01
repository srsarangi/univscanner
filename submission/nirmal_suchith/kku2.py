from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import csv
import re
from bs4 import BeautifulSoup
import time

def extract_kku_faculty():
    # Set up Selenium WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    base_url = "https://gear.kku.ac.th/index.php/staff?lang=en"
    driver.get(base_url)
    driver.implicitly_wait(10)

    # Parse the page source
    soup = BeautifulSoup(driver.page_source, "html.parser")

    # Locate the table rows containing faculty data
    faculty_rows = soup.find_all("tr")

    # File setup for output
    txt_filename = "kku2_faculty.txt"
    csv_filename = "kku2_faculty.csv"

    txt_file = open(txt_filename, "w", encoding="utf-8")
    csv_file = open(csv_filename, "w", newline='', encoding="utf-8")
    csvwriter = csv.writer(csv_file)

    # Write CSV header
    csvwriter.writerow(["University", "Country", "Name", "Email", "Website", "Research Areas"])

    # University and country information
    university = "Khon Kaen University"
    country = "Thailand"

    # Keywords for filtering relevant faculty
    keyword_list = [
        'embedded systems', 'embedded software', 'hardware systems',
        'system architecture', 'IoT', 'real-time systems',
        'operating systems', 'system programming', 'system software',
        'distributed systems', 'kernel', 'machine learning', 'deep learning', 'artificial intelligence'
    ]

    # Process each professor's data
    for row in faculty_rows:
        try:
            # Extract the name and website
            name_tag = row.find("a")
            name = name_tag.get_text(strip=True) if name_tag else "Not Found"
            website = name_tag["href"] if name_tag else "Not Found"

            # Extract the research areas
            research_text = row.find("td", style=re.compile("vertical-align: middle;")).get_text(separator=" ").strip()

            # Extract the email
            email_tag = row.find("i", class_="fa fa-envelope crytmail")
            email = f"{email_tag['data-name']}@kku.ac.th" if email_tag else "Not Found"

            # Check if research matches any keywords
            if any(re.search(keyword, research_text, re.IGNORECASE) for keyword in keyword_list):
                # Save the relevant professor's details
                txt_file.write(f"Name: {name}\nEmail: {email}\nWebsite: {website}\nUniversity: {university}\nCountry: {country}\nResearch Areas: {research_text}\n\n")
                csvwriter.writerow([university, country, name, email, website, research_text])

        except Exception as e:
            print(f"Error processing a row: {e}")

    # Close files and driver
    txt_file.close()
    csv_file.close()
    driver.quit()

    print("Data extraction complete")

if __name__ == "__main__":
    extract_kku_faculty()
