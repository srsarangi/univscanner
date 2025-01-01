from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import csv
import re
from bs4 import BeautifulSoup
import time

def rhodes_faculty():
    # Set up Selenium WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    url = "https://www.cs.rhodes.edu/people/faculty.html"
    driver.get(url)
    driver.implicitly_wait(10)

    # Parse the page content with BeautifulSoup
    soup = BeautifulSoup(driver.page_source, "html.parser")
    faculty_sections = soup.find_all('div', class_="col-lg-6 mt-4")

    # Output file setup
    txt_filename = "rhodes_faculty.txt"
    csv_filename = "rhodes_faculty.csv"
    
    txt_file = open(txt_filename, "w", encoding="utf-8")
    csv_file = open(csv_filename, "w", newline='', encoding="utf-8")
    csvwriter = csv.writer(csv_file)

    # Write CSV header
    csvwriter.writerow(["University", "Country", "Name", "Email", "Website", "Research Areas"])

    # University and country information
    university = "Rhodes College"
    country = "USA"

    # Keywords for filtering relevant faculty
    keyword_list = [
        'embedded systems', 'embedded software', 'hardware systems',
        'system architecture', 'IoT', 'real-time systems',
        'operating systems', 'system programming', 'system software',
        'distributed systems', 'kernel', 'machine learning', 'deep learning', 'artificial intelligence',
        'quantum computing'
    ]

    # Process each faculty section
    for section in faculty_sections:
        try:
            # Extract faculty name
            name_tag = section.find("h4")
            name = name_tag.get_text(strip=True) if name_tag else "Not Found"

            # Extract research interests
            research_tag = section.find("p", text=re.compile("Research interests"))
            research_areas = research_tag.get_text(strip=True).replace("Research interests: ", "") if research_tag else "Not Found"

            # Extract email
            email = "Not Found"
            contact_tag = section.find("p")
            if contact_tag:
                email_tag = contact_tag.find("a", href=re.compile("mailto:"))
                if email_tag:
                    email = email_tag["href"].replace("mailto:", "")

            # Extract website
            website = "Not Found"
            if contact_tag:
                website_tag = contact_tag.find("a", href=re.compile("https://"))
                if website_tag:
                    website = website_tag["href"]

            # Check if research matches any keywords
            if any(re.search(keyword, research_areas, re.IGNORECASE) for keyword in keyword_list):
                # Save the relevant faculty details
                txt_file.write(f"Name: {name}\nEmail: {email}\nWebsite: {website}\nUniversity: {university}\nCountry: {country}\nResearch Areas: {research_areas}\n\n")
                csvwriter.writerow([university, country, name, email, website, research_areas])

        except Exception as e:
            print(f"Error processing a faculty section: {e}")

    # Close files and driver
    txt_file.close()
    csv_file.close()
    driver.quit()

    print("Data extraction complete.")

if __name__ == "__main__":
    rhodes_faculty()
