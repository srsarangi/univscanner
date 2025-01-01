from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import csv
import re
from bs4 import BeautifulSoup

def albany_faculty():
    # Set up Selenium WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    base_url = "https://www.albany.edu"
    faculty_url = f"{base_url}/computer-science/faculty-staff"
    driver.get(faculty_url)
    driver.implicitly_wait(10)

    # Parse the faculty page
    soup = BeautifulSoup(driver.page_source, "html.parser")
    faculty_sections = soup.select('.faculty-member.views-row')

    # File setup for output
    txt_filename = "albany_faculty_filtered.txt"
    csv_filename = "albany_faculty_filtered.csv"

    txt_file = open(txt_filename, "w", encoding="utf-8")
    csv_file = open(csv_filename, "w", newline='', encoding="utf-8")
    csvwriter = csv.writer(csv_file)

    # Write CSV header
    csvwriter.writerow(["University", "Country", "Name", "Email", "Website", "Research Areas"])

    # University and country information
    university = "University at Albany, Department of Computer Science"
    country = "USA"

    # Keywords for filtering relevant faculty
    keyword_list = [
        'embedded systems', 'embedded software', 'IoT', 'real-time systems',
        'operating systems', 'system programming', 'kernel', 'distributed systems',
        'software testing', 'software engineering', 'software evolution',
        'computer science education'
    ]

    # Process each professor's section
    for section in faculty_sections:
        try:
            # Extract professor's name
            name_tag = section.select_one(".views-field-title .field-content")
            name = name_tag.get_text(strip=True) if name_tag else "Not Found"

            # Extract professor's email
            email_tag = section.select_one(".views-field-field-email a")
            email = email_tag['href'].replace('mailto:', '').strip() if email_tag else "Not Found"

            # Extract research areas
            research_tag = section.select_one(".views-field-field-display-summary-of-about .field-content")
            research = research_tag.get_text(strip=True).replace("Research Interests: ", "") if research_tag else "Not Found"

            # Extract professor's website link
            website_tag = section.select_one(".views-field-field-personal-website a")
            website = website_tag['href'] if website_tag else "Not Found"

            # Check if research matches any keywords
            if any(re.search(keyword, research, re.IGNORECASE) for keyword in keyword_list):
                # Save the relevant professor's details
                txt_file.write(f"Name: {name}\nEmail: {email}\nWebsite: {website}\nUniversity: {university}\nCountry: {country}\nResearch Areas: {research}\n\n")
                csvwriter.writerow([university, country, name, email, website, research])

        except Exception as e:
            print(f"Error processing a professor section: {e}")

    # Close files and driver
    txt_file.close()
    csv_file.close()
    driver.quit()

    print("Data extraction complete")

if __name__ == "__main__":
    albany_faculty()
