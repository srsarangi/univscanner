from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import csv
import re
from bs4 import BeautifulSoup

def nsu_ece_faculty():
    # Set up Selenium WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    
    # Base URL for the faculty directory and pagination
    base_url = "https://ece.northsouth.edu/people/type/faculty/"
    
    # File setup for output
    txt_filename = "nsu_ece_faculty.txt"
    csv_filename = "nsu_ece_faculty.csv"

    txt_file = open(txt_filename, "w", encoding="utf-8")
    csv_file = open(csv_filename, "w", newline='', encoding="utf-8")
    csvwriter = csv.writer(csv_file)

    # Write CSV header
    csvwriter.writerow(["University", "Country", "Name", "Email", "Website", "Research Areas"])

    # University and country information
    university = "North South University, ECE"
    country = "Bangladesh"

    # Keywords for filtering relevant faculty (case-insensitive)
    keyword_list = [
        'embedded systems', 'embedded software', 'hardware systems',
        'system architecture', 'IoT', 'real-time systems',
        'operating systems', 'system programming', 'system software',
        'distributed systems', 'kernel', 'machine learning', 'deep learning', 'artificial intelligence'
    ]

    # Loop through the first 7 pages
    for page_num in range(1, 8):
        page_url = f"{base_url}?page={page_num}"
        driver.get(page_url)
        driver.implicitly_wait(10)

        # Parse the current page to extract faculty sections
        soup = BeautifulSoup(driver.page_source, "html.parser")
        faculty_rows = soup.select('tbody tr')

        # Process each professor's row
        for row in faculty_rows:
            try:
                # Extract professor's name
                name_tag = row.find('td', class_='faculty-name').find('strong')
                name = name_tag.get_text(strip=True) if name_tag else "Not Found"

                # Extract professor's email
                email_tag = row.find('td', class_='faculty-name').find(text=re.compile(r'@'))
                email = email_tag.strip() if email_tag else "Not Found"

                # Extract professor's website
                website_tag = row.find('td', class_='faculty-name').find('a', href=re.compile(r'https?://'))
                website = website_tag['href'] if website_tag else "Not Found"

                # Extract research areas
                research_area_tags = row.find_all('td')[2].find_all('a')
                research_areas = ", ".join([tag.get_text(strip=True) for tag in research_area_tags]) if research_area_tags else "Not Found"

                # Check if research areas match any of the keywords (case-insensitive)
                if any(re.search(keyword, research_areas, re.IGNORECASE) for keyword in keyword_list):
                    # Save the relevant professor's details
                    txt_file.write(f"Name: {name}\nEmail: {email}\nWebsite: {website}\nUniversity: {university}\nCountry: {country}\nResearch Areas: {research_areas}\n\n")
                    csvwriter.writerow([university, country, name, email, website, research_areas])

            except Exception as e:
                print(f"Error processing a professor's row on page {page_num}: {e}")

    # Close files and driver
    txt_file.close()
    csv_file.close()
    driver.quit()

    print("Data extraction complete")

if __name__ == "__main__":
    nsu_ece_faculty()
