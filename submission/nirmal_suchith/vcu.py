from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import re
from bs4 import BeautifulSoup

def vcu_faculty():
    # Set up Selenium WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    base_url = "https://egr.vcu.edu/directory/"
    driver.get(base_url)

    # Wait for the iframe with faculty directory to load
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "expertfile-embed")))

    # Set up output files
    txt_filename = "vcu_faculty.txt"
    csv_filename = "vcu_faculty.csv"

    with open(txt_filename, "w", encoding="utf-8") as txt_file, \
         open(csv_filename, "w", newline='', encoding="utf-8") as csv_file:

        csvwriter = csv.writer(csv_file)
        # Write CSV header
        csvwriter.writerow(["University", "Country", "Name", "Email", "Website", "Research Areas"])

        # University and country information
        university = "Virginia Commonwealth University, Engineering"
        country = "USA"

        # Keywords for filtering relevant faculty
        keyword_list = [
            'embedded systems', 'embedded software', 'hardware systems',
            'system architecture', 'IoT', 'real-time systems',
            'operating systems', 'system programming', 'system software',
            'distributed systems', 'kernel', 'machine learning', 'deep learning', 'artificial intelligence'
        ]

        # Process faculty data from the current page
        while True:
            soup = BeautifulSoup(driver.page_source, "html.parser")
            faculty_sections = soup.select('div[data-testid="user-tile"]')

            for section in faculty_sections:
                try:
                    # Extract professor's profile link
                    profile_link = section.find('a', class_='no-underline')['href']
                    profile_url = "http://egr.vcu.edu" + profile_link

                    # Extract professor's name
                    name_tag = section.find('h3')
                    name = name_tag.get_text(strip=True) if name_tag else "Not Found"

                    # Extract professor's email
                    email_tag = section.find('span', {'data-testid': re.compile(r'.*-user-email')})
                    email = email_tag.get_text(strip=True) if email_tag else "Not Found"

                    # Extract professor's website
                    website = profile_url

                    # Extract research areas from the topics
                    topics_tag = section.find('div', id='topics')
                    if topics_tag:
                        research_areas = ", ".join([topic.get_text(strip=True) for topic in topics_tag.find_all('span')])
                    else:
                        research_areas = "Not Found"

                    # Check if research areas match any keywords
                    if any(re.search(keyword, research_areas, re.IGNORECASE) for keyword in keyword_list):
                        # Save the relevant professor's details
                        txt_file.write(f"Name: {name}\nEmail: {email}\nWebsite: {website}\nUniversity: {university}\nCountry: {country}\nResearch Areas: {research_areas}\n\n")
                        csvwriter.writerow([university, country, name, email, website, research_areas])

                except Exception as e:
                    print(f"Error processing a professor section: {e}")

            # Try to go to the next page if exists
            pagination_links = soup.select('a.cursor-pointer')  # Selecting all pagination links
            next_page_found = False
            for link in pagination_links:
                if 'href' in link.attrs:
                    next_page_url = link['href']
                    # Check if the next page URL is a valid page number (ignoring the 'next' button)
                    if re.match(r".*page_number=\d+$", next_page_url):
                        # Construct the full URL for the next page
                        full_next_page_url = "https://egr.vcu.edu" + next_page_url
                        driver.get(full_next_page_url)
                        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "expertfile-embed")))
                        next_page_found = True
                        break

            if not next_page_found:
                print("No more pages found. Exiting...")
                break  # No more pages to scrape

    # Close the driver
    driver.quit()
    print("Data extraction complete")

if __name__ == "__main__":
    vcu_faculty()
