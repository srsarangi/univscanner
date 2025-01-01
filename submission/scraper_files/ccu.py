from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import csv
import re
from bs4 import BeautifulSoup

def ccu_faculty():
    # Set up Selenium WebDriver
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    base_url = "https://www.cs.ccu.edu.tw"
    faculty_directory_url = "https://cs.ccu.edu.tw/p/404-1094-6502.php?Lang=en"
    driver.get(faculty_directory_url)
    driver.implicitly_wait(10)

    # Parse the faculty page to extract sections for professors
    soup = BeautifulSoup(driver.page_source, "html.parser")
    professor_sections = soup.find_all('div', class_='col-sm-20 col-xs-30')

    # File setup for output
    # txt_filename = "ccu_faculty.txt"
    # csv_filename = "ccu_faculty.csv"

    # txt_file = open(txt_filename, "w", encoding="utf-8")
    # csv_file = open(csv_filename, "w", newline='', encoding="utf-8")
    # csvwriter = csv.writer(csv_file)

    # # Write CSV header
    # csvwriter.writerow(["University", "Country", "Name", "Email", "Website", "Research Areas"])

    # University and country information
    university = "National Chung Cheng University, CS"
    country = "Taiwan"
    profs = []

    # Keywords for filtering relevant faculty
    keyword_list = [
        'embedded systems', 'embedded software', 'hardware systems',
        'system architecture', 'IoT', 'real-time systems',
        'operating systems', 'system programming', 'system software',
        'distributed systems', 'kernel', 'machine learning', 'deep learning', 'artificial intelligence'
    ]

    # Process each professor's section
    for section in professor_sections:
        try:
            # Extract the professor's name
            name_tag = section.find('a', href=re.compile(r"^https://www.cs.ccu.edu.tw/~"))
            name = name_tag.get_text(strip=True) if name_tag else "Not Found"
            
            # Extract professor's website (which is the same as the name link)
            website = name_tag['href'] if name_tag else "Not Found"
            
            # Extract professor's email
            email_tag = section.find('a', href=re.compile(r"mailto:"))
            email = email_tag.get_text(strip=True).replace("(at)", "@") if email_tag else "Not Found"
            
            # Extract research areas (expertise)
            expertise_tag = section.find('li', string=re.compile("Expertise"))
            expertise_text = expertise_tag.find_next('li').get_text(strip=True) if expertise_tag else "Not Found"

            # Check if research matches any keywords
            if any(re.search(keyword, expertise_text, re.IGNORECASE) for keyword in keyword_list):
                # Save the relevant professor's details
                # txt_file.write(f"Name: {name}\nEmail: {email}\nWebsite: {website}\nUniversity: {university}\nCountry: {country}\nResearch Areas: {expertise_text}\n\n")
                # csvwriter.writerow([university, country, name, email, website, expertise_text])
                profs.append([university, country, name, email, website])

        except Exception as e:
            print(f"Error processing a professor section: {e}")

    # Close files and driver
    # txt_file.close()
    # csv_file.close()
    driver.quit()

    print("CCU Data extraction complete")
    return profs

if __name__ == "__main__":
    ccu_faculty()
