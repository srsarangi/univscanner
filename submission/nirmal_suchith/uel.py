from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
import csv
import re
from bs4 import BeautifulSoup
import time

def uel_faculty():
    # Set up Selenium WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    base_url = "https://www.uel.ac.uk"
    faculty_directory_url = f"{base_url}/about/our-schools/school-architecture-computing-engineering"
    driver.get(faculty_directory_url)
    driver.implicitly_wait(10)

    # Handle cookies pop-up
    try:
        accept_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Accept')]")
        accept_button.click()
        time.sleep(2)  # Wait for the cookies dialog to close
    except Exception as e:
        print(f"Error handling cookies: {e}")

    # Click to expand the "Department of Computer Science and Digital Technologies" section
    try:
        dept_section = driver.find_element(By.ID, "accordionHeading-2")
        dept_section.click()
        time.sleep(3)  # Wait for the section to load
    except Exception as e:
        print(f"Error clicking department section: {e}")
        driver.quit()
        return

    # Parse the expanded section for profile links
    soup = BeautifulSoup(driver.page_source, "html.parser")
    profile_links = soup.select('.coh-style-inline-link.dark-link')

    # File setup for output
    txt_filename = "uel_faculty.txt"
    csv_filename = "uel_faculty.csv"

    txt_file = open(txt_filename, "w", encoding="utf-8")
    csv_file = open(csv_filename, "w", newline='', encoding="utf-8")
    csvwriter = csv.writer(csv_file)

    # Write CSV header
    csvwriter.writerow(["University", "Country", "Name", "Email", "Website", "Research Areas"])

    # University and country information
    university = "University of East London, CS"
    country = "UK"

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
            profile_url = base_url + relative_url
            driver.get(profile_url)
            driver.implicitly_wait(10)
            profile_soup = BeautifulSoup(driver.page_source, "html.parser")

            # Extract professor's name
            name_tag = profile_soup.find("h1", class_="coh-style-header-1-small")
            name = name_tag.get_text(strip=True) if name_tag else "Not Found"

            # Extract professor's email
            email_tag = profile_soup.find("a", href=re.compile(r"^mailto:"))
            email = email_tag.get_text(strip=True) if email_tag else "Not Found"

            # Extract research areas
            research_tag = profile_soup.find("div", class_="rich-txt-custom")
            research_text = research_tag.get_text(strip=True) if research_tag else "Not Found"

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
    uel_faculty()
