from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import csv
import re
from bs4 import BeautifulSoup

def tudublin_faculty():
    # Set up Selenium WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    base_url = "https://www.tudublin.ie"
    faculty_directory_url = f"{base_url}/explore/faculties-and-schools/computing-digital-data/school-of-computer-science/people/academic-staff/"
    driver.get(faculty_directory_url)

    # File setup for output
    txt_filename = "tudublin_faculty.txt"
    csv_filename = "tudublin_faculty.csv"

    with open(txt_filename, "w", encoding="utf-8") as txt_file, open(csv_filename, "w", newline='', encoding="utf-8") as csv_file:
        csvwriter = csv.writer(csv_file)

        # Write CSV header
        csvwriter.writerow(["University", "Country", "Name", "Email", "Website", "Research Areas"])

        # University and country information
        university = "Technological University Dublin, School of Computer Science"
        country = "Ireland"

        # Keywords for filtering relevant faculty
        keyword_list = [
            'embedded systems', 'embedded software', 'hardware systems',
            'system architecture', 'IoT', 'real-time systems',
            'operating systems', 'system programming', 'system software',
            'distributed systems', 'kernel', 'machine learning', 'deep learning', 'artificial intelligence'
        ]

        # Loop through each page
        while True:
            # Wait for the faculty sections to load
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "content-carousel__inner")))

            # Parse the current page
            soup = BeautifulSoup(driver.page_source, "html.parser")
            professor_sections = soup.select(".content-carousel__inner")

            # Process each professor's section
            for section in professor_sections:
                try:
                    # Extract the professor's profile link
                    profile_relative_url = section.find("a")["href"]
                    profile_url = base_url + profile_relative_url

                    # Visit the professor's profile page
                    driver.get(profile_url)
                    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "component__title")))
                    profile_soup = BeautifulSoup(driver.page_source, "html.parser")

                    # Extract professor's name
                    name_tag = profile_soup.find("h2", class_="component__title")
                    name = name_tag.get_text(strip=True) if name_tag else "Not Found"

                    # Extract professor's email
                    email_tag = profile_soup.find("a", href=re.compile(r"mailto:"))
                    email = email_tag.get_text(strip=True) if email_tag else "Not Found"

                    # Extract research areas
                    research_tags = profile_soup.select('ul li span')
                    research_list = [tag.get_text(strip=True) for tag in research_tags]
                    research_text = ", ".join(research_list) if research_list else "Not Found"

                    # Check if research matches any keywords
                    if any(re.search(keyword, research_text, re.IGNORECASE) for keyword in keyword_list):
                        # Save the relevant professor's details
                        txt_file.write(f"Name: {name}\nEmail: {email}\nWebsite: {profile_url}\nUniversity: {university}\nCountry: {country}\nResearch Areas: {research_text}\n\n")
                        csvwriter.writerow([university, country, name, email, profile_url, research_text])

                except Exception as e:
                    print(f"Error processing a professor section: {e}")

            # Check for the next page
            next_page = soup.find("a", text=">")
            if next_page:
                next_page_url = base_url + next_page["href"]
                driver.get(next_page_url)
            else:
                break

    # Close the driver
    driver.quit()

    print("Data extraction complete")

if __name__ == "__main__":
    tudublin_faculty()
