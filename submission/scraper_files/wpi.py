from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import csv
import re
from bs4 import BeautifulSoup
import time

def wpi_faculty():
    # Set up Selenium WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    base_url = "https://www.wpi.edu"
    faculty_directory_url = f"{base_url}/academics/departments/computer-science/faculty-staff"
    driver.get(faculty_directory_url)
    driver.implicitly_wait(10)

    # Parse the main faculty page
    soup = BeautifulSoup(driver.page_source, "html.parser")
    faculty_links = soup.select(".dw__name .dw__name_link")  # Selector for profile links

    # File setup for output
    # txt_filename = "wpi_faculty.txt"
    # csv_filename = "wpi_faculty.csv"

    # txt_file = open(txt_filename, "w", encoding="utf-8")
    # csv_file = open(csv_filename, "w", newline='', encoding="utf-8")
    # csvwriter = csv.writer(csv_file)

    # # Write CSV header
    # csvwriter.writerow(["University", "Country", "Name", "Email", "Website", "Research Areas"])

    # University and country information
    university = "Worcester Polytechnic Institute"
    country = "USA"
    profs = []

    # Keywords for filtering relevant faculty
    keyword_list = [
        'embedded systems', 'embedded software', 'hardware systems',
        'system architecture', 'IoT', 'real-time systems',
        'operating systems', 'system programming', 'system software',
        'distributed systems', 'kernel', 'machine learning', 'deep learning', 'artificial intelligence',
        'Networks', 'Mobile Adhoc networks', 'Wireless sensor Networks', 'Routing Algorithms', 'IPv6'
    ]

    # Process each faculty profile
    for link in faculty_links:
        try:
            # Extract profile link and navigate to it
            relative_url = link['href'].strip()
            profile_url = f"{base_url}{relative_url}"
            driver.get(profile_url)
            driver.implicitly_wait(10)
            profile_soup = BeautifulSoup(driver.page_source, "html.parser")

            # Extract professor's name
            name_tag = profile_soup.select_one(".staff__personal-info h2.no-margin")
            name = name_tag.get_text(strip=True) if name_tag else "Not Found"

            # Extract professor's email
            email_tag = profile_soup.select_one(".region-contact .field-item")
            email = email_tag.get_text(strip=True) if email_tag else "Not Found"

            # Extract research areas
            research_tags = profile_soup.select(
                ".field--name-field-research-interests .field__item span"
            )
            research_areas = ", ".join(tag.get_text(strip=True) for tag in research_tags) if research_tags else "Not Found"

            # Website link is the profile link
            website = profile_url

            # Check if research matches any keywords
            if any(re.search(keyword, research_areas, re.IGNORECASE) for keyword in keyword_list):
                # Save the relevant professor's details
                # txt_file.write(f"Name: {name}\nEmail: {email}\nWebsite: {website}\nUniversity: {university}\nCountry: {country}\nResearch Areas: {research_areas}\n\n")
                # csvwriter.writerow([university, country, name, email, website, research_areas])
                profs.append([university, country, name, email, website])

        except Exception as e:
            print(f"Error processing a profile: {e}")

    # Close files and driver
    # txt_file.close()
    # csv_file.close()
    driver.quit()

    print("Worchester Polytechnic Institute data extraction complete")
    return profs

if __name__ == "__main__":
    wpi_faculty()
