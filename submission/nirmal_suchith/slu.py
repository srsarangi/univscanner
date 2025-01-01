from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import csv
import re
from bs4 import BeautifulSoup
import time

def slu_faculty():
    # Set up Selenium WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    base_url = "https://www.slu.edu"
    faculty_url = f"{base_url}/science-and-engineering/academics/computer-science/faculty-and-staff/index.php"
    driver.get(faculty_url)
    driver.implicitly_wait(10)

    # Parse the faculty page for profile links
    soup = BeautifulSoup(driver.page_source, "html.parser")
    profile_links = soup.select("ul > li > a")  # Select links inside <ul> elements

    # File setup for output
    txt_filename = "slu_faculty.txt"
    csv_filename = "slu_faculty.csv"

    txt_file = open(txt_filename, "w", encoding="utf-8")
    csv_file = open(csv_filename, "w", newline='', encoding="utf-8")
    csvwriter = csv.writer(csv_file)

    # Write CSV header
    csvwriter.writerow(["University", "Country", "Name", "Email", "Website", "Research Areas"])

    # University and country information
    university = "Saint Louis University, CS"
    country = "USA"

    # Keywords for filtering relevant faculty
    keyword_list = [
        'embedded systems', 'embedded software', 'hardware systems',
        'system architecture', 'IoT', 'real-time systems',
        'operating systems', 'system programming', 'system software',
        'distributed systems', 'kernel', 'machine learning', 'deep learning', 'artificial intelligence'
    ]

    # Process each professor's profile
    for link in profile_links:
        try:
            # Extract profile link and navigate to it
            relative_url = link['href']
            profile_url = base_url + relative_url if relative_url.startswith("/") else relative_url
            driver.get(profile_url)
            driver.implicitly_wait(10)
            profile_soup = BeautifulSoup(driver.page_source, "html.parser")

            # Extract professor's name
            name_tag = profile_soup.find("h1")
            name = name_tag.get_text(strip=True) if name_tag else "Not Found"

            # Extract professor's email
            email_tag = profile_soup.find("a", href=re.compile(r"^mailto:"))
            email = email_tag.get_text(strip=True) if email_tag else "Not Found"

            # Extract research areas
            research_section = profile_soup.find("ul")
            research_text = ", ".join(li.get_text(strip=True) for li in research_section.find_all("li")) if research_section else "Not Found"

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
    slu_faculty()
