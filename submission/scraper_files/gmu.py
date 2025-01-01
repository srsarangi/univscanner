from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import csv
import re
from bs4 import BeautifulSoup
import time

def gmu_faculty():
    # Set up Selenium WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    base_url = "https://cec.gmu.edu"
    faculty_directory_url = f"{base_url}/about/meet-our-faculty/computer-science-faculty"
    driver.get(faculty_directory_url)
    driver.implicitly_wait(10)

    # File setup for output
    # txt_filename = "gmu_faculty.txt"
    # csv_filename = "gmu_faculty.csv"

    # txt_file = open(txt_filename, "w", encoding="utf-8")
    # csv_file = open(csv_filename, "w", newline='', encoding="utf-8")
    # csvwriter = csv.writer(csv_file)

    # # Write CSV header
    # csvwriter.writerow(["University", "Country", "Name", "Email", "Website", "Research Areas"])

    # University and country information
    university = "George Mason University, CS"
    country = "United States"
    profs = []

    # Keywords for filtering relevant faculty
    keyword_list = [
        'embedded systems', 'embedded software', 'hardware systems',
        'system architecture', 'IoT', 'real-time systems',
        'operating systems', 'system programming', 'system software',
        'distributed systems', 'kernel', 'machine learning', 'deep learning', 'artificial intelligence'
    ]

    # Loop through pages
    page_number = 0
    while True:
        # Load the page and get the faculty sections
        current_url = f"{faculty_directory_url}?page={page_number}"
        driver.get(current_url)
        driver.implicitly_wait(10)
        soup = BeautifulSoup(driver.page_source, "html.parser")
        professor_sections = soup.find_all('div', class_='view-profile-wrapper')

        # If there are no faculty sections, break the loop
        if not professor_sections:
            break

        # Process each professor's section
        for section in professor_sections:
            try:
                # Extract the professor's profile link
                name_tag = section.find('div', class_='view-profile-title').find('a')
                profile_relative_url = name_tag['href']
                profile_url = base_url + profile_relative_url

                # Visit the professor's profile page
                driver.get(profile_url)
                driver.implicitly_wait(10)
                profile_soup = BeautifulSoup(driver.page_source, "html.parser")

                # Extract professor's name
                name = name_tag.get_text(strip=True) if name_tag else "Not Found"

                # Extract professor's research areas
                bio_tag = section.find('div', class_='view-profile-bio')
                research_text = bio_tag.get_text(strip=True).replace("Research Interest:", "").strip() if bio_tag else "Not Found"

                # Extract professor's email
                email_tag = profile_soup.find('a', href=re.compile(r"mailto:"))
                email = email_tag.get_text(strip=True) if email_tag else "Not Found"

                # Extract professor's website (Profile link)
                website = profile_url  # Profile URL is the website link

                # Check if research matches any keywords
                if any(re.search(keyword, research_text, re.IGNORECASE) for keyword in keyword_list):
                    # Save the relevant professor's details
                    # txt_file.write(f"Name: {name}\nEmail: {email}\nWebsite: {website}\nUniversity: {university}\nCountry: {country}\nResearch Areas: {research_text}\n\n")
                    # csvwriter.writerow([university, country, name, email, website, research_text])
                    profs.append([university, country, name, email, website])

            except Exception as e:
                print(f"Error processing a professor section: {e}")

        # Increment to go to the next page
        page_number += 1
        time.sleep(2)  # To prevent hitting the website too quickly

    # Close files and driver
    # txt_file.close()
    # csv_file.close()
    driver.quit()

    print("GMU Data extraction complete")
    return profs

if __name__ == "__main__":
    gmu_faculty()
