from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import csv
import re
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By

def gust_faculty():
    # Set up Selenium WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    base_url = "https://www.gust.edu.kw"
    faculty_directory_url = f"{base_url}/cas-csd/faculty-staff"
    driver.get(faculty_directory_url)
    driver.implicitly_wait(10)

    # Parse the main faculty directory page to extract sections for professors
    soup = BeautifulSoup(driver.page_source, "html.parser")
    professor_sections = soup.select('.directoryList_row__6SHzc')

    # File setup for output
    txt_filename = "gust_faculty.txt"
    csv_filename = "gust_faculty.csv"

    txt_file = open(txt_filename, "w", encoding="utf-8")
    csv_file = open(csv_filename, "w", newline='', encoding="utf-8")
    csvwriter = csv.writer(csv_file)

    # Write CSV header
    csvwriter.writerow(["University", "Country", "Name", "Email", "Website", "Research Areas"])

    # University and country information
    university = "Gulf University for Science and Technology"
    country = "Kuwait"

    # Keywords for filtering relevant faculty
    keyword_list = [
        'embedded systems', 'embedded software', 'hardware systems',
        'system architecture', 'IoT', 'real-time systems',
        'operating systems', 'system programming', 'system software',
        'distributed systems', 'kernel', 'machine learning', 'deep learning', 'artificial intelligence'
    ]

    # Process each professor's section
    for section in professor_sections:
        try:
            # Extract the professor's profile link
            profile_relative_url = section.find('a', class_='directoryList_personLink__GH1oz')['href']
            profile_url = base_url + profile_relative_url
            print("Processing profile:", profile_url)

            # Visit the professor's profile page
            driver.get(profile_url)
            driver.implicitly_wait(10)
            profile_soup = BeautifulSoup(driver.page_source, "html.parser")

            # Extract professor's name
            name_tag = profile_soup.find("h3", class_="person_personName__kusZ5")
            name = name_tag.get_text(strip=True) if name_tag else "Not Found"

            # Extract professor's email
            email_tag = profile_soup.find("span", class_="person_contactLabel__DcdTc")
            email_parts = email_tag.get_text(strip=True).split('@') if email_tag else ["Not Found"]
            email = email_parts[0] + "@" + email_parts[1] if len(email_parts) > 1 else "Not Found"

            # Navigate to 'Teaching' tab to get research areas
            teaching_button = driver.find_element(By.XPATH, '//button[contains(text(), "Teaching")]')
            teaching_button.click()
            driver.implicitly_wait(10)
            profile_soup = BeautifulSoup(driver.page_source, "html.parser")

            # Extract research areas from the Teaching tab
            research_tags = profile_soup.find_all('td', class_='table_cell__tMGaj')
            research_list = [tag.get_text(strip=True) for tag in research_tags]
            research_text = ", ".join(research_list) if research_list else "Not Found"

            # Check if research matches any keywords
            if any(re.search(keyword, research_text, re.IGNORECASE) for keyword in keyword_list):
                # Save the relevant professor's details
                txt_file.write(f"Name: {name}\nEmail: {email}\nWebsite: {profile_url}\nUniversity: {university}\nCountry: {country}\nResearch Areas: {research_text}\n\n")
                csvwriter.writerow([university, country, name, email, profile_url, research_text])

        except Exception as e:
            print(f"Error processing a professor section: {e}")

    # Close files and driver
    txt_file.close()
    csv_file.close()
    driver.quit()

    print("Data extraction complete")

if __name__ == "__main__":
    gust_faculty()
