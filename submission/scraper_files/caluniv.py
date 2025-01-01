from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import csv
import re
from bs4 import BeautifulSoup

def calcutta_university():
    # Setup Selenium WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    url = "https://www.caluniv.ac.in/academic/Compsc.html"
    driver.get(url)
    driver.implicitly_wait(10)
    
    # Parse the page source with BeautifulSoup
    soup = BeautifulSoup(driver.page_source, "html.parser")

    # Prepare output files
    # txt_filename = "calcutta_faculty.txt"
    # csv_filename = "calcutta_faculty.csv"
    # f_txt = open(txt_filename, "w", encoding="utf-8")
    # f_csv = open(csv_filename, "w", newline='', encoding="utf-8")
    # csvwriter = csv.writer(f_csv)

    # Write headers in the CSV file
    # csvwriter.writerow(["University", "Country", "Name", "Email", "Research Area"])
    professors = []
    # University and country details
    university_name = "University of Calcutta"
    country = "India"

    # Keywords for filtering faculty based on research areas
    keywords = [
        "embedded systems", "Embedded System", "embedded software", "hardware systems",
        "system architecture", "IoT", "real-time systems", "operating systems",
        "Operating System", "OS", "system programming", "system software",
        "distributed systems", "kernel", "network security", "data mining",
        "image processing", "quantum computing"
    ]

    # Locate the faculty table
    table = soup.find("table", class_="table table-bordered")
    rows = table.find_all("tr")[1:]  # Skip the header row

    for row in rows:
        cols = row.find_all("td")
        if len(cols) < 4:
            continue

        # Extract faculty details
        name = cols[0].get_text(strip=True).split("\n")[0]
        email = re.findall(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", cols[3].get_text(strip=True))
        email = email[0] if email else "Not Found"
        research_area = cols[2].get_text(strip=True)

        # Check if any research area matches the keywords
        if any(re.search(keyword, research_area, re.IGNORECASE) for keyword in keywords):
            # Write to text file
            # f_txt.write(f"Name: {name}\nEmail: {email}\nUniversity: {university_name}\nResearch Areas: {research_area}\n\n")
            # Write to CSV file
            # csvwriter.writerow([university_name, country, name, email, research_area])
            professors.append([university_name, country, name, email, url])

    # Close the files and browser
    # f_txt.close()
    # f_csv.close()
    driver.quit()

    print("Calcutta University Faculty Scraped Successfully!")
    return professors

if __name__ == "__main__":
    calcutta_university()
