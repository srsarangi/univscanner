from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import csv
import re
from bs4 import BeautifulSoup
import time

def scrape_clarku_faculty():
    # Set up Selenium WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    base_url = "https://www.clarku.edu"
    faculty_directory_url = f"{base_url}/departments/computer-science/people/"
    driver.get(faculty_directory_url)
    driver.implicitly_wait(10)

    # Parse the main page for faculty profile links
    soup = BeautifulSoup(driver.page_source, "html.parser")
    faculty_blocks = soup.find_all("li", class_="faculty-listing__list__block")

    # File setup for output
    # txt_filename = "clarku_faculty.txt"
    # csv_filename = "clarku_faculty.csv"

    # txt_file = open(txt_filename, "w", encoding="utf-8")
    # csv_file = open(csv_filename, "w", newline='', encoding="utf-8")
    # csvwriter = csv.writer(csv_file)

    # Write CSV header
    # csvwriter.writerow(["University", "Country", "Name", "Email", "Website", "Research Areas"])

    # University and country information
    university = "Clark University, Computer Science"
    country = "USA"
    professors = []
    # Keywords for filtering relevant faculty
    keyword_list = [
        'embedded systems', 'embedded software', 'hardware systems',
        'system architecture', 'IoT', 'real-time systems',
        'operating systems', 'system programming', 'system software',
        'distributed systems', 'kernel', 'machine learning', 'deep learning', 'artificial intelligence'
    ]

    # Process each faculty block
    for block in faculty_blocks:
        try:
            profile_link = block.find("a", href=True)["href"]
            profile_url = profile_link if profile_link.startswith("http") else base_url + profile_link
            driver.get(profile_url)
            driver.implicitly_wait(10)
            profile_soup = BeautifulSoup(driver.page_source, "html.parser")

            # Extract professor's name
            name_tag = profile_soup.find("h1", class_="subbio__content--name")
            name = name_tag.get_text(strip=True) if name_tag else "Not Found"

            # Extract professor's email
            email_tag = profile_soup.find("a", href=re.compile(r"^mailto:"))
            email = email_tag.get_text(strip=True) if email_tag else "Not Found"

            # Extract research areas
            research_tag = profile_soup.find("p", class_="subbio__bookmark__interests--copy")
            research_text = research_tag.get_text(strip=True) if research_tag else "Not Found"

            # Website link is the profile link
            website = profile_url

            # Check if research matches any keywords
            if any(re.search(keyword, research_text, re.IGNORECASE) for keyword in keyword_list):
                # Save the relevant professor's details
                # txt_file.write(f"Name: {name}\nEmail: {email}\nWebsite: {website}\nUniversity: {university}\nCountry: {country}\nResearch Areas: {research_text}\n\n")
                # csvwriter.writerow([university, country, name, email, website, research_text])
                professors.append([university, country, name, email, website])

        except Exception as e:
            print(f"Error processing a profile: {e}")

    # Close files and driver
    # txt_file.close()
    # csv_file.close()
    driver.quit()
    print("Finished scraping Clark University faculty.")
    return professors


if __name__ == "__main__":
    scrape_clarku_faculty()
