from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import csv
import re
import time

def extract_uet_faculty():
    # Setup Selenium WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    url = "https://nwl.uet.edu.pk/department-of-computer-science-engineering/449-2/"
    driver.get(url)
    driver.implicitly_wait(10)
    
    # Parse the main page content
    soup = BeautifulSoup(driver.page_source, "html.parser")
    
    # File setup for output
    filename = "uet_faculty.txt"
    f = open(filename, "w", encoding="utf-8")
    
    csv_filename = "uet_faculty.csv"
    f_csv = open(csv_filename, "w", newline='', encoding="utf-8")
    csv_writer = csv.writer(f_csv)
    csv_writer.writerow(["Name", "Email", "Research Areas", "University", "Country"])

    # University information
    university = "University of Engineering and Technology"
    country = "Pakistan"

    # Research keywords
    keyword_list = [
        'embedded systems', 'Embedded System', 'embedded software', 'hardware systems',
        'system architecture', 'IoT', 'real-time systems',
        'operating systems', 'Operating System', 'OS', 'system programming', 'system software',
        'distributed systems', 'kernel'
    ]

    # Extract all faculty profiles
    profiles = soup.find_all('div', class_='col-md-3 col-sm-6 main0')
    print(profiles)
    print("dfgl kfngd")

    for profile in profiles:
        # Navigate to individual faculty profile pages
        profile_link_tag = profile.find('a', href=True)
        profile_url = profile_link_tag['href'] if profile_link_tag else None
        print(profile_url)

        if profile_url:
            driver.get(profile_url)
            time.sleep(2)  # Allow time for the page to load
            profile_soup = BeautifulSoup(driver.page_source, "html.parser")

            # Extract name
            name_tag = profile_soup.find('h3')
            name = name_tag.text.strip() if name_tag else "Not Found"

            # Extract email
            email_tag = profile_soup.find('span', text=re.compile('@'))
            email = email_tag.text.strip() if email_tag else "Not Found"

            # Extract research interests
            research_interests = []
            research_section = profile_soup.find('div', id='research_interest_list')
            if research_section:
                research_interests = [li.text.strip() for li in research_section.find_all('li')]

            research_text = ", ".join(research_interests)

            # Check if any keyword matches
            flag = any(re.search(keyword, research_text, re.IGNORECASE) for keyword in keyword_list)

            # Write to files if keywords match
            if flag:
                f.write(f"Name: {name}\nEmail: {email}\nResearch Areas: {research_text}\nUniversity: {university}\nCountry: {country}\n\n")
                csv_writer.writerow([name, email, research_text, university, country])

    # Close files and driver
    f.close()
    f_csv.close()
    driver.quit()
    print("Data extraction complete.")

if __name__ == '__main__':
    extract_uet_faculty()
