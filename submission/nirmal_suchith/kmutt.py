from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import csv
import re
from bs4 import BeautifulSoup
import time

def kmutt_faculty():
    # Set up Selenium WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    base_url = "https://www.cpe.kmutt.ac.th"
    faculty_directory_url = f"{base_url}/en/staff/"
    driver.get(faculty_directory_url)
    driver.implicitly_wait(10)

    # Handle cookies popup
    try:
        accept_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Accept All')]")
        accept_button.click()
        time.sleep(2)  # Wait for the cookies dialog to close
    except Exception as e:
        print(f"Cookies popup not handled: {e}")

    # Parse the main page for profile links
    soup = BeautifulSoup(driver.page_source, "html.parser")
    profile_divs = soup.find_all('div', class_="team-member")

    # File setup for output
    txt_filename = "kmutt_faculty.txt"
    csv_filename = "kmutt_faculty.csv"

    txt_file = open(txt_filename, "w", encoding="utf-8")
    csv_file = open(csv_filename, "w", newline='', encoding="utf-8")
    csvwriter = csv.writer(csv_file)

    # Write CSV header
    csvwriter.writerow(["University", "Country", "Name", "Email", "Website", "Research Areas"])

    # University and country information
    university = "King Mongkut's University of Technology Thonburi, CPE"
    country = "Thailand"

    # Keywords for filtering relevant faculty
    keyword_list = [
        'embedded systems', 'embedded software', 'hardware systems',
        'system architecture', 'IoT', 'real-time systems',
        'operating systems', 'system programming', 'system software',
        'distributed systems', 'kernel', 'machine learning', 'deep learning', 'artificial intelligence',
        'quantum computing'
    ]

    # Process each professor's profile
    for div in profile_divs:
        try:
            # Extract profile link
            profile_link_tag = div.find("a")
            if not profile_link_tag:
                continue
            relative_url = profile_link_tag["href"]
            profile_url = base_url + relative_url

            # Navigate to the professor's profile page
            driver.get(profile_url)
            driver.implicitly_wait(10)
            profile_soup = BeautifulSoup(driver.page_source, "html.parser")

            # Extract professor's name
            name_tag = profile_soup.find("h2", class_="pb-10 m-0")
            name = name_tag.get_text(strip=True) if name_tag else "Not Found"

            # Extract professor's email
            email_tag = profile_soup.find("td", text="Email:")
            email = email_tag.find_next_sibling("td").get_text(strip=True) if email_tag else "Not Found"

            # Extract research areas
            research_section = profile_soup.find("ul", class_="interested")
            research_areas = ", ".join([li.get_text(strip=True) for li in research_section.find_all("li")]) if research_section else "Not Found"

            # Website link is the profile link
            website = profile_url

            # Check if research matches any keywords
            if any(re.search(keyword, research_areas, re.IGNORECASE) for keyword in keyword_list):
                # Save the relevant professor's details
                txt_file.write(f"Name: {name}\nEmail: {email}\nWebsite: {website}\nUniversity: {university}\nCountry: {country}\nResearch Areas: {research_areas}\n\n")
                csvwriter.writerow([university, country, name, email, website, research_areas])

        except Exception as e:
            print(f"Error processing a profile: {e}")

    # Close files and driver
    txt_file.close()
    csv_file.close()
    driver.quit()

    print("Data extraction complete")

if __name__ == "__main__":
    kmutt_faculty()
