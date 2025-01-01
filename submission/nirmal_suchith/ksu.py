from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import csv
import re
from bs4 import BeautifulSoup

def ksu_faculty():
    # Set up Selenium WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    base_url = "https://www.cs.ksu.edu"
    faculty_directory_url = f"{base_url}/about/people/faculty/"
    driver.get(faculty_directory_url)
    driver.implicitly_wait(10)

    # Parse the main faculty directory page to extract sections for professors
    soup = BeautifulSoup(driver.page_source, "html.parser")
    professor_rows = soup.select('table[data-table-id="d54e44"] tbody tr')

    # File setup for output
    txt_filename = "ksu_faculty.txt"
    csv_filename = "ksu_faculty.csv"

    txt_file = open(txt_filename, "w", encoding="utf-8")
    csv_file = open(csv_filename, "w", newline='', encoding="utf-8")
    csvwriter = csv.writer(csv_file)

    # Write CSV header
    csvwriter.writerow(["University", "Country", "Name", "Email", "Website", "Research Areas"])

    # University and country information
    university = "Kansas State University, CS"
    country = "USA"

    # Keywords for filtering relevant faculty
    keyword_list = [
        'embedded systems', 'embedded software', 'hardware systems',
        'system architecture', 'IoT', 'real-time systems',
        'operating systems', 'system programming', 'system software',
        'distributed systems', 'kernel', 'machine learning', 'deep learning', 'artificial intelligence'
    ]

    # Process each professor's section
    for row in professor_rows:
        try:
            # Extract the professor's profile link
            profile_relative_url = row.find('a')['href']
            profile_url = base_url + profile_relative_url

            # Visit the professor's profile page
            driver.get(profile_url)
            driver.implicitly_wait(10)
            profile_soup = BeautifulSoup(driver.page_source, "html.parser")

            # Extract professor's name
            name_tag = profile_soup.find("h1")
            name = name_tag.get_text(strip=True).split("|")[0] if name_tag else "Not Found"

            # Extract professor's email
            email_tag = profile_soup.find("a", href=re.compile(r"mailto:"))
            email = email_tag.get_text(strip=True) if email_tag else "Not Found"

            # Extract professor's website
            website_tag = profile_soup.find("a", href=re.compile(r"http.*"))
            website = website_tag['href'] if website_tag else "Not Found"

            # Extract research areas
            research_tag = profile_soup.find("h5", string="Research")
            research_text = ""
            if research_tag:
                research_p_tag = research_tag.find_next('p')
                if research_p_tag:
                    research_text = research_p_tag.get_text(strip=True)

            # Check if research matches any keywords
            if any(re.search(keyword, research_text, re.IGNORECASE) for keyword in keyword_list):
                # Save the relevant professor's details
                txt_file.write(f"Name: {name}\nEmail: {email}\nWebsite: {website}\nUniversity: {university}\nCountry: {country}\nResearch Areas: {research_text}\n\n")
                csvwriter.writerow([university, country, name, email, website, research_text])

        except Exception as e:
            print(f"Error processing a professor section: {e}")

    # Close files and driver
    txt_file.close()
    csv_file.close()
    driver.quit()

    print("Data extraction complete")

if __name__ == "__main__":
    ksu_faculty()
