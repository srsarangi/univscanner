from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import csv
import re
from bs4 import BeautifulSoup

def texas_tech():
    # Set up Selenium WebDriver (using Chrome in this case)
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    url = "https://www.depts.ttu.edu/cs/faculty/"  # Faculty page URL
    driver.get(url)  # Load the page

    # Give the page some time to load the JavaScript content
    driver.implicitly_wait(10)

    # Parse the page content using BeautifulSoup
    soup = BeautifulSoup(driver.page_source, "html.parser")

    # File setup for output
    # filename = "texas_tech_faculty.txt"
    # f = open(filename, "w")

    # excel_filename = "texas_tech_faculty.csv"
    # f2 = open(excel_filename, "w", newline='', encoding="utf-8")
    # csvwriter = csv.writer(f2)

    # Set the university name and country
    u_name = "Texas Tech University"
    country = "USA"
    profs = []
    
    # Research keywords for embedded systems or operating systems
    keyword_list = [
        'embedded systems', 'Embedded System', 'embedded software', 'hardware systems',
        'system architecture', 'IoT', 'real-time systems',
        'operating systems', 'Operating System', 'OS', 'system programming', 'system software',
        'distributed systems', 'kernel'
    ]

    # Extracting all faculty profiles (divs with class 'bio-panel')
    faculty_profiles = soup.find_all('div', class_='bio-panel')

    for profile in faculty_profiles:
        # Extracting name and profile link
        name_tag = profile.find('a', class_='bio-panel-info-name')
        name = name_tag.get_text(strip=True) if name_tag else "Not Found"
        profile_link = name_tag['href'] if name_tag else None

        # Extracting email
        email_tag = profile.find('span', class_='bio-panel-info-email')
        email = email_tag.get_text(strip=True) if email_tag else "Not Found"

        # Open the individual faculty page to extract research interests
        if profile_link:
            driver.get(f"https://www.depts.ttu.edu{profile_link}")  # Open individual profile
            driver.implicitly_wait(10)
            profile_soup = BeautifulSoup(driver.page_source, "html.parser")
            
            # Extracting research interests
            research_interests = ""
            research_tag = profile_soup.find('ul', class_='default-list')
            if research_tag:
                research_interests = ", ".join([li.get_text(strip=True) for li in research_tag.find_all('li')])

            # Check if any research interest matches our criteria
            flag = False
            for keyword in keyword_list:
                if re.search(keyword, research_interests, re.IGNORECASE):
                    flag = True
                    break

            # If keyword matches, write to files
            if flag:
                # f.write(f"Name: {name}\nEmail: {email}\nUniversity: {u_name}\nResearch Areas: {research_interests}\n\n")
                # csvwriter.writerow([u_name, country, name, email, research_interests])
                profs.append([u_name, country, name, email, url])
    
    # Close the files
    # f.close()
    # f2.close()

    # Close the WebDriver
    driver.quit()

    print("Texas Tech University data extraction complete")
    return profs

if __name__ == '__main__':
    texas_tech()
