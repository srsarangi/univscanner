from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import csv
import re
from bs4 import BeautifulSoup

def dortmund_faculty():
    # Set up Selenium WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    base_url = "https://cs.tu-dortmund.de/en/fakultaet/professuren/"
    driver.get(base_url)
    driver.implicitly_wait(10)

    # Parse the main faculty directory page to extract professor links
    soup = BeautifulSoup(driver.page_source, "html.parser")
    professor_links = [
        link.get("href")
        for link in soup.select('a.tile.tile-link.tile--thirds')
        if link.get("href")
    ]

    # File setup for output
    # txt_filename = "dortmund_faculty.txt"
    # csv_filename = "dortmund_faculty.csv"

    # txt_file = open(txt_filename, "w", encoding="utf-8")
    # csv_file = open(csv_filename, "w", newline='', encoding="utf-8")
    # csvwriter = csv.writer(csv_file)

    # # Write CSV header
    # csvwriter.writerow(["University", "Country", "Name", "Email", "Website", "Research Areas"])

    # University and country information
    university = "TU Dortmund University"
    country = "Germany"

    # Keywords for filtering relevant faculty
    keyword_list = [
        'embedded systems', 'embedded software', 'hardware systems',
        'system architecture', 'IoT', 'real-time systems',
        'operating systems', 'system programming', 'system software',
        'distributed systems', 'kernel', 'machine learning', 'deep learning', 'artificial intelligence'
    ]

    professors = []
    # Process each professor's profile
    for profile_url in professor_links:
        try:
            driver.get(profile_url)
            driver.implicitly_wait(10)
            profile_soup = BeautifulSoup(driver.page_source, "html.parser")

            # Extract professor's name
            name_tag = profile_soup.select_one('.frame-container .frame-inner header h1')
            name = name_tag.get_text(strip=True) if name_tag else "Not Found"

            # Extract professor's email
            email_tag = profile_soup.select_one('.contact-info a[href^="mailto:"]')
            email = email_tag.get_text(strip=True) if email_tag else "Not Found"

            # Extract research areas
            research_tags = profile_soup.select('.list-unordered .list-unordered__item')
            research_list = [tag.get_text(strip=True) for tag in research_tags]
            research_text = ", ".join(research_list) if research_list else "Not Found"

            # Extract professor's website (the profile link itself)
            website = profile_url

            # Check if research matches any keywords
            if any(re.search(keyword, research_text, re.IGNORECASE) for keyword in keyword_list):
                # Save the relevant professor's details
                # txt_file.write(f"Name: {name}\nEmail: {email}\nWebsite: {website}\nUniversity: {university}\nCountry: {country}\nResearch Areas: {research_text}\n\n")
                # csvwriter.writerow([university, country, name, email, website, research_text])
                professors.append([university, country, name, email, website])


        except Exception as e:
            print(f"Error processing professor at {profile_url}: {e}")

    # Close files and driver
    # txt_file.close()
    # csv_file.close()
    driver.quit()

    print("TU Dortmund University faculty extraction complete.")
    return professors

if __name__ == "__main__":
    dortmund_faculty()
