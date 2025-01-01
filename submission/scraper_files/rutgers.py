from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import csv
import re
from bs4 import BeautifulSoup

def rutgers_faculty():
    # Set up Selenium WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    url = "https://cs.camden.rutgers.edu/faculty-staff/"
    driver.get(url)
    driver.implicitly_wait(10)

    # Parse the main faculty page to extract links to individual profiles
    soup = BeautifulSoup(driver.page_source, "html.parser")
    faculty_links = [
        a['href'] for a in soup.select('.su-column-inner a[href]')
        if "faculty-staff" in a['href'] or "rutgers.edu" in a['href']
    ]

    # File setup for output
    # txt_filename = "rutgers_faculty.txt"
    # csv_filename = "rutgers_faculty.csv"

    # txt_file = open(txt_filename, "w", encoding="utf-8")
    # csv_file = open(csv_filename, "w", newline='', encoding="utf-8")
    # csvwriter = csv.writer(csv_file)

    # # Write CSV header
    # csvwriter.writerow(["University", "Country", "Name", "Email", "Website", "Research Areas"])

    # University and country information
    university = "Rutgers University, Camden"
    country = "USA"
    profs = []

    # Keywords for filtering relevant faculty
    keyword_list = [
        'embedded systems', 'embedded software', 'hardware systems',
        'system architecture', 'IoT', 'real-time systems',
        'operating systems', 'system programming', 'system software',
        'distributed systems', 'kernel', 'machine learning', 'deep learning', 'artificial intelligence'
    ]

    # A set to track processed profiles and avoid duplicates
    processed_profiles = set()

    # Loop through each profile link
    for link in faculty_links:
        try:
            if link in processed_profiles:
                continue  # Skip already processed links

            # Add to the processed set
            processed_profiles.add(link)

            # Load the faculty profile page
            driver.get(link)
            driver.implicitly_wait(10)
            profile_soup = BeautifulSoup(driver.page_source, "html.parser")

            # Extract professor's name
            name_tag = profile_soup.find("h1", class_="page-title")
            name = name_tag.get_text(strip=True) if name_tag else "Not Found"

            # Extract professor's email
            email_tag = profile_soup.find("a", href=re.compile(r"^mailto:"))
            email = email_tag.get_text(strip=True) if email_tag else "Not Found"

            # Extract professor's website
            website_tag = profile_soup.find("a", href=re.compile(r"^(http|https)://"))
            website = website_tag['href'] if website_tag else "Not Found"

            # Extract research interests
            research_tag = profile_soup.find("p", class_="featured")
            research_text = research_tag.get_text(strip=True).replace("Research Interests: ", "") if research_tag else "Not Found"

            # Check if research matches any keywords
            if any(re.search(keyword, research_text, re.IGNORECASE) for keyword in keyword_list):
                # Save the relevant professor's details
                # txt_file.write(f"Name: {name}\nEmail: {email}\nWebsite: {website}\nUniversity: {university}\nCountry: {country}\nResearch Areas: {research_text}\n\n")
                # csvwriter.writerow([university, country, name, email, website, research_text])
                profs.append([university, country, name, email, website])

        except Exception as e:
            print(f"Error processing {link}: {e}")

    # Close files and driver
    # txt_file.close()
    # csv_file.close()
    driver.quit()
    print("Rutgers University, Camden data extraction complete")
    return profs

if __name__ == "__main__":
    rutgers_faculty()
