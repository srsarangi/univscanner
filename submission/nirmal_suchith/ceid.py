from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import csv
import re
from bs4 import BeautifulSoup

def extract_ceid_faculty():
    # Set up Selenium WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    base_url = "https://www.ceid.upatras.gr/en/staff/faculty/"
    driver.get(base_url)
    driver.implicitly_wait(10)

    # Parse the main faculty directory page to extract sections for professors
    soup = BeautifulSoup(driver.page_source, "html.parser")
    faculty_sections = soup.select('.gdlr-core-personnel-list')

    # File setup for output
    txt_filename = "ceid_faculty.txt"
    csv_filename = "ceid_faculty.csv"

    txt_file = open(txt_filename, "w", encoding="utf-8")
    csv_file = open(csv_filename, "w", newline='', encoding="utf-8")
    csvwriter = csv.writer(csv_file)

    # Write CSV header
    csvwriter.writerow(["University", "Country", "Name", "Email", "Website", "Research Areas"])

    # University and country information
    university = "University of Patras, CEID"
    country = "Greece"

    # Keywords for filtering relevant faculty
    keyword_list = [
        'embedded systems', 'embedded software', 'hardware systems',
        'system architecture', 'IoT', 'real-time systems',
        'operating systems', 'system programming', 'system software',
        'distributed systems', 'kernel', 'machine learning', 'deep learning', 'artificial intelligence'
    ]

    # Process each professor's section
    for section in faculty_sections:
        try:
            # Extract profile link
            profile_tag = section.find('a', href=True)
            profile_url = profile_tag['href'] if profile_tag else None

            if not profile_url:
                continue

            # Visit the professor's profile page
            driver.get(profile_url)
            driver.implicitly_wait(10)
            profile_soup = BeautifulSoup(driver.page_source, "html.parser")

            # Extract professor's name
            name_tag = profile_soup.find("h3", class_="gdlr-core-title-item-title gdlr-core-skin-title")
            name = name_tag.get_text(strip=True) if name_tag else "Not Found"

            # Extract professor's email
            email_tag = profile_soup.find("div", class_="kingster-personnel-info-list kingster-type-email")
            email = email_tag.get_text(strip=True) if email_tag else "Not Found"

            # Extract research areas
            research_tag = profile_soup.find("div", class_="field-item even")
            research_text = research_tag.get_text(strip=True) if research_tag else "Not Found"

            # Check if research matches any keywords
            if not any(re.search(keyword, research_text, re.IGNORECASE) for keyword in keyword_list):
                continue  # Skip if no matching keywords

            # Save the relevant professor's details
            txt_file.write(f"Name: {name}\nEmail: {email}\nWebsite: {profile_url}\nUniversity: {university}\nCountry: {country}\nResearch Areas: {research_text}\n\n")
            csvwriter.writerow([university, country, name, email, profile_url, research_text])

        except Exception as e:
            print(f"Error processing a professor's profile: {e}")

    # Close files and driver
    txt_file.close()
    csv_file.close()
    driver.quit()

    print("Data extraction complete")

if __name__ == "__main__":
    extract_ceid_faculty()
