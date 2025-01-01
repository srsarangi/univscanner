from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import csv
import re
from bs4 import BeautifulSoup

def extract_cnu_faculty():
    # Set up Selenium WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    url = "https://eng.cnu.ac.kr/eng_en/department/computerconverge.do"
    driver.get(url)
    driver.implicitly_wait(10)

    # Parse the page content using BeautifulSoup
    soup = BeautifulSoup(driver.page_source, "html.parser")

    # File setup for output
    filename = "cnu_faculty.txt"
    with open(filename, "w", encoding="utf-8") as f:
        excel_filename = "cnu_faculty.csv"
        with open(excel_filename, "w", newline='', encoding="utf-8") as f2:
            csvwriter = csv.writer(f2)

            # Headers for CSV
            csvwriter.writerow(["University", "Country", "Name", "Phone", "Research Areas", "Website"])

            # University and country
            u_name = "Chungnam National University"
            country = "South Korea"

            # Keywords to search
            keyword_list = [
                'embedded systems', 'Embedded System', 'embedded software', 'hardware systems',
                'system architecture', 'IoT', 'real-time systems',
                'operating systems', 'Operating System', 'OS', 'system programming', 'system software',
                'distributed systems', 'kernel'
            ]

            # Extract table rows containing faculty information
            rows = soup.select("tbody > tr")

            for row in rows:
                # Extract name
                name = row.select_one("td:nth-child(1)").get_text(strip=True)

                # Extract position (not used here but available)
                position = row.select_one("td:nth-child(2)").get_text(strip=True)

                # Extract research/major areas
                research_areas = row.select_one("td:nth-child(3)").get_text(strip=True)

                # Extract phone number
                phone = row.select_one("td:nth-child(4)").get_text(strip=True)

                # Check if any keyword matches the research areas
                flag = any(re.search(keyword, research_areas, re.IGNORECASE) for keyword in keyword_list)

                # Write to files if a keyword matches
                if flag:
                    f.write(f"Name: {name}\nPhone: {phone}\nUniversity: {u_name}\nResearch Areas: {research_areas}\n\n")
                    csvwriter.writerow([u_name, country, name, phone, research_areas, url])

    # Close the WebDriver
    driver.quit()

    print("Data extraction complete")

if __name__ == '__main__':
    extract_cnu_faculty()
