from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import csv
import re
from bs4 import BeautifulSoup

def syracuse_faculty():
    # Set up Selenium WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    url = "https://ecs.syracuse.edu/faculty-staff/?category=electrical-engineering-and-computer-science&people="
    driver.get(url)
    driver.implicitly_wait(10)

    # Parse the main faculty directory page to extract profile links
    soup = BeautifulSoup(driver.page_source, "html.parser")
    faculty_links = [
        a['href'] for a in soup.select('.ecs-profile .profile-name a')
        if "ecs.syracuse.edu" in a['href']
    ]

    # File setup for output
    # txt_filename = "syracuse_faculty.txt"
    # csv_filename = "syracuse_faculty.csv"

    # txt_file = open(txt_filename, "w", encoding="utf-8")
    # csv_file = open(csv_filename, "w", newline='', encoding="utf-8")
    # csvwriter = csv.writer(csv_file)

    # # Write CSV header
    # csvwriter.writerow(["University", "Country", "Name", "Email", "Website", "Research Areas"])

    # University and country information
    university = "Syracuse University, ECS"
    country = "USA"

    # Keywords for filtering relevant faculty
    keyword_list = [
        'embedded systems', 'embedded software', 'hardware systems',
        'system architecture', 'IoT', 'real-time systems',
        'operating systems', 'system programming', 'system software',
        'distributed systems', 'kernel', 'machine learning', 'deep learning', 'artificial intelligence'
    ]

    profs = []

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
            name_tag = profile_soup.find("h1", class_="title")
            name = name_tag.get_text(strip=True) if name_tag else "Not Found"

            # Extract professor's email
            email_tag = profile_soup.find("h4", text=re.compile(r".+@.+"))
            email = email_tag.get_text(strip=True) if email_tag else "Not Found"

            # Extract research areas
            research_header = profile_soup.find("p", text="Areas of Expertise:")
            research_list = (
                [li.get_text(strip=True) for li in research_header.find_next_siblings("ul")[0].find_all("li")]
                if research_header else []
            )
            research_text = ", ".join(research_list) if research_list else "Not Found"

            # Check if research matches any keywords
            if any(re.search(keyword, research_text, re.IGNORECASE) for keyword in keyword_list):
                # Save the relevant professor's details
                # txt_file.write(f"Name: {name}\nEmail: {email}\nWebsite: {link}\nUniversity: {university}\nCountry: {country}\nResearch Areas: {research_text}\n\n")
                # csvwriter.writerow([university, country, name, email, link, research_text])
                profs.append([university, country, name, email, link])

        except Exception as e:
            print(f"Error processing {link}: {e}")

    # Close files and driver
    # txt_file.close()
    # csv_file.close()
    driver.quit()

    print("Syracuse University ECS Data extraction complete")
    return profs

if __name__ == "__main__":
    syracuse_faculty()
