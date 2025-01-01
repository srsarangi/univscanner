from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import csv
import re
import time

def extract_konkuk_faculty():
    # Setup Selenium WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    url = "https://ctl.konkuk.ac.kr/en/14576/subview.do"
    driver.get(url)
    driver.implicitly_wait(10)
    
    # Parse the main page content
    soup = BeautifulSoup(driver.page_source, "html.parser")
    
    # File setup for output
    # filename = "konkuk_faculty.txt"
    # f = open(filename, "w", encoding="utf-8")
    
    # csv_filename = "konkuk_faculty.csv"
    # f_csv = open(csv_filename, "w", newline='', encoding="utf-8")
    # csv_writer = csv.writer(f_csv)
    # csv_writer.writerow(["Name", "Email", "Research Areas", "Website", "University", "Country"])
    
    # University information
    university = "Konkuk University"
    country = "South Korea"
    profs = []

    # Research keywords
    keyword_list = [
        'embedded systems', 'Embedded System', 'embedded software', 'hardware systems',
        'system architecture', 'IoT', 'real-time systems',
        'operating systems', 'Operating System', 'OS', 'system programming', 'system software',
        'distributed systems', 'kernel'
    ]

    # Extract faculty profiles
    profiles = soup.find_all('div', class_='row')

    for profile in profiles:
        # Extract name
        name_tag = profile.find('div', class_='name')
        name = name_tag.strong.text.strip() if name_tag else "Not Found"
        
        # Extract email
        email_tag = profile.find('dl', class_='ico5')
        email = email_tag.dd.text.strip() if email_tag else "Not Found"
        
        # Extract research areas
        research_tag = profile.find('dl', class_='ico2')
        research_areas = research_tag.dd.text.strip() if research_tag else "Not Found"
        
        # Extract website link
        website_tag = profile.find('li', class_='homepage')
        website_link = website_tag.a['href'] if website_tag and website_tag.a else "Not Found"
        
        # Check if any keyword matches
        flag = any(re.search(keyword, research_areas, re.IGNORECASE) for keyword in keyword_list)

        # Write to files if keywords match
        if flag:
            # f.write(f"Name: {name}\nEmail: {email}\nResearch Areas: {research_areas}\nWebsite: {website_link}\nUniversity: {university}\nCountry: {country}\n\n")
            # csv_writer.writerow([name, email, research_areas, website_link, university, country])
            profs.append([university, country, name, email, website_link])

    # Close files and driver
    # f.close()
    # f_csv.close()
    driver.quit()
    print("Konkuk University data extraction complete.")
    return profs

if __name__ == '__main__':
    extract_konkuk_faculty()
