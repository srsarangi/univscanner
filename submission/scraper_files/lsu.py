from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import csv
import re
from bs4 import BeautifulSoup

def lsu_faculty_scraper():
    # Set up Selenium WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    base_url = "https://www.lsu.edu"
    faculty_directory_url = f"{base_url}/eng/cse/people/faculty/index.php"
    driver.get(faculty_directory_url)
    driver.implicitly_wait(10)

    # Parse the main faculty directory page
    soup = BeautifulSoup(driver.page_source, "html.parser")
    faculty_sections = soup.select('.col-md-3')

    # File setup for output
    # txt_filename = "lsu_faculty.txt"
    # csv_filename = "lsu_faculty.csv"

    # txt_file = open(txt_filename, "w", encoding="utf-8")
    # csv_file = open(csv_filename, "w", newline='', encoding="utf-8")
    # csvwriter = csv.writer(csv_file)

    # # Write CSV header
    # csvwriter.writerow(["University", "Country", "Name", "Email", "Website", "Research Areas"])

    # University and country information
    university = "Louisiana State University, CSE"
    country = "USA"
    professors = []

    # Keywords for filtering relevant faculty
    keyword_list = [
        'embedded systems', 'embedded software', 'hardware systems',
        'system architecture', 'IoT', 'real-time systems',
        'operating systems', 'system programming', 'system software',
        'distributed systems', 'kernel', 'machine learning', 'deep learning', 'artificial intelligence'
    ]

    # Process each faculty section
    for section in faculty_sections:
        try:
            # Extract the professor's profile link
            profile_relative_url = section.find('a', href=True)['href']
            profile_url = base_url + profile_relative_url

            # Visit the professor's profile page
            driver.get(profile_url)
            driver.implicitly_wait(10)
            profile_soup = BeautifulSoup(driver.page_source, "html.parser")

            # Extract professor's name
            name_tag = profile_soup.find("h1")
            name = name_tag.get_text(strip=True) if name_tag else "Not Found"

            # Extract professor's email
            email_tag = profile_soup.find("a", href=re.compile(r"mailto:"))
            email = email_tag.get_text(strip=True) if email_tag else "Not Found"

            # Extract professor's website
            website_tag = profile_soup.find("a", href=re.compile(r"http.*"))
            website = website_tag['href'] if website_tag else profile_url

            # Extract research interests
            research_section = profile_soup.find("h2", text="Research Interests")
            research_text = "Not Found"
            if research_section:
                next_p = research_section.find_next_sibling("p")
                research_text = next_p.get_text(strip=True) if next_p else "Not Found"

            # Check if research matches any keywords
            if any(re.search(keyword, research_text, re.IGNORECASE) for keyword in keyword_list):
                # Save the relevant professor's details
                # txt_file.write(f"Name: {name}\nEmail: {email}\nWebsite: {website}\nUniversity: {university}\nCountry: {country}\nResearch Areas: {research_text}\n\n")
                # csvwriter.writerow([university, country, name, email, website, research_text])
                professors.append([university, country, name, email, website])

        except Exception as e:
            print(f"Error processing a faculty section: {e}")

    # Close files and driver
    # txt_file.close()
    # csv_file.close()
    driver.quit()
    print("Louisiana State University, CSE data extraction complete")
    return professors

if __name__ == "__main__":
    lsu_faculty_scraper()
