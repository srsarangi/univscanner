from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import csv
import re
from bs4 import BeautifulSoup
import time

def uop_faculty():
    # Set up Selenium WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    base_url = "http://www.uop.edu.pk"
    faculty_directory_url = f"{base_url}/departments/?q=Department-of-Computer-Science&r=Teaching-Faculty"
    driver.get(faculty_directory_url)
    driver.implicitly_wait(10)

    # Parse the main faculty page
    soup = BeautifulSoup(driver.page_source, "html.parser")
    faculty_links = soup.select("li h4 a")  # Selector for profile links

    # File setup for output
    txt_filename = "uop_faculty.txt"
    csv_filename = "uop_faculty.csv"

    txt_file = open(txt_filename, "w", encoding="utf-8")
    csv_file = open(csv_filename, "w", newline='', encoding="utf-8")
    csvwriter = csv.writer(csv_file)

    # Write CSV header
    csvwriter.writerow(["University", "Country", "Name", "Email", "Website", "Research Areas"])

    # University and country information
    university = "University of Peshawar"
    country = "Pakistan"

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
            profile_url = relative_url if relative_url.startswith("http") else f"{base_url}{relative_url}"
            driver.get(profile_url)
            driver.implicitly_wait(10)
            profile_soup = BeautifulSoup(driver.page_source, "html.parser")

            # Extract professor's name
            name_tag = profile_soup.find("h2", id="main-title")
            name = name_tag.get_text(strip=True) if name_tag else "Not Found"

            # Extract professor's email
            email_tag = profile_soup.find("li", class_="email-team")
            email = email_tag.get_text(strip=True) if email_tag else "Not Found"

            # Extract research areas
            research_tag = profile_soup.find("h5", style="color:#039; ")
            research_text = research_tag.find("span").get_text(strip=True) if research_tag and research_tag.find("span") else "Not Found"

            # Website link is the profile link
            website = profile_url

            # Check if research matches any keywords
            if any(re.search(keyword, research_text, re.IGNORECASE) for keyword in keyword_list):
                # Save the relevant professor's details
                txt_file.write(f"Name: {name}\nEmail: {email}\nWebsite: {website}\nUniversity: {university}\nCountry: {country}\nResearch Areas: {research_text}\n\n")
                csvwriter.writerow([university, country, name, email, website, research_text])

        except Exception as e:
            print(f"Error processing a profile: {e}")

    # Close files and driver
    txt_file.close()
    csv_file.close()
    driver.quit()

    print("Data extraction complete")

if __name__ == "__main__":
    uop_faculty()
