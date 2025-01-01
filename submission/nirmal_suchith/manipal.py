from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import csv
import re

def manipal_faculty():
    # Set up Selenium WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    base_url = "https://www.manipal.edu"
    faculty_directory_url = f"{base_url}/mit/department-faculty/department-list/computer-science-and-engineering.html"
    driver.get(faculty_directory_url)
    driver.implicitly_wait(10)

    # Parse the faculty directory page to extract profile links
    soup = BeautifulSoup(driver.page_source, "html.parser")
    faculty_sections = soup.select('.col-lg-3.col-md-3.col-sm-6.col-xs-12 .leadership-wrap a')

    # File setup for output
    txt_filename = "manipal_faculty.txt"
    csv_filename = "manipal_faculty.csv"
    txt_file = open(txt_filename, "w", encoding="utf-8")
    csv_file = open(csv_filename, "w", newline='', encoding="utf-8")
    csvwriter = csv.writer(csv_file)
    csvwriter.writerow(["University", "Country", "Name", "Email", "Website", "Research Areas"])

    # University and country information
    university = "Manipal Institute of Technology, CS"
    country = "India"

    # Keywords for filtering relevant faculty
    keyword_list = [
        'embedded systems', 'embedded software', 'hardware systems',
        'system architecture', 'IoT', 'real-time systems',
        'operating systems', 'system programming', 'system software',
        'distributed systems', 'kernel', 'machine learning', 'deep learning', 'artificial intelligence'
    ]

    for faculty in faculty_sections:
        try:
            # Extract faculty profile link and visit it
            profile_relative_url = faculty['href']
            profile_url = base_url + profile_relative_url
            driver.get(profile_url)
            driver.implicitly_wait(10)

            # Parse faculty profile page
            profile_soup = BeautifulSoup(driver.page_source, "html.parser")

            # Extract professor's name
            name_div = profile_soup.find("div", class_="title-wrap-left")
            name = name_div.find("h2").get_text(strip=True) if name_div else "Not Found"

            # Extract professor's email
            email_div = profile_soup.find("div", class_="email")
            email_tag = email_div.find("a", href=re.compile(r"mailto:")) if email_div else None
            email = email_tag.get_text(strip=True) if email_tag else "Not Found"

            # Click on Expertise tab
            try:
                # Locate the tab and click it
                expertise_tab = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, 'a[href="#expertise"]'))
                )
                expertise_tab.click()

                # Wait for the Expertise content to load
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, "expertise"))
                )
            except Exception as e:
                print(f"Error clicking Expertise tab for {name}: {e}")
                continue

            # Parse the Expertise content
            expertise_soup = BeautifulSoup(driver.page_source, "html.parser")
            expertise_div = expertise_soup.select_one("#expertise")
            areas_of_interest = expertise_div.get_text(strip=True) if expertise_div else "Not Found"

            # Check if research matches any keywords
            if any(re.search(keyword, areas_of_interest, re.IGNORECASE) for keyword in keyword_list):
                # Save the relevant professor's details
                txt_file.write(f"Name: {name}\nEmail: {email}\nWebsite: {profile_url}\nUniversity: {university}\nCountry: {country}\nResearch Areas: {areas_of_interest}\n\n")
                csvwriter.writerow([university, country, name, email, profile_url, areas_of_interest])

        except Exception as e:
            print(f"Error processing faculty profile: {e}")

    # Close files and driver
    txt_file.close()
    csv_file.close()
    driver.quit()
    print("Data extraction complete")

if __name__ == "__main__":
    manipal_faculty()
