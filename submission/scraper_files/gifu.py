import requests
from bs4 import BeautifulSoup
import re
import csv

def gifu_university_faculty():
    # Set the base URL and the faculty directory URL
    base_url = "https://www.eng.gifu-u.ac.jp"
    faculty_directory_url = f"{base_url}/jyouhou/e/staff.html"
    
    # Send a GET request to the faculty directory page
    response = requests.get(faculty_directory_url)
    soup = BeautifulSoup(response.content, "html.parser")

    # Find the table containing faculty information
    table = soup.find("table", {"border": "1", "cellpadding": "2", "cellspacing": "0"})
    rows = table.find_all("tr")[1:]  # Skip the header row

    # File setup for output
    # txt_filename = "gifu_university_faculty.txt"
    # csv_filename = "gifu_university_faculty.csv"

    # txt_file = open(txt_filename, "w", encoding="utf-8")
    # csv_file = open(csv_filename, "w", newline='', encoding="utf-8")
    # csvwriter = csv.writer(csv_file)

    # # Write CSV header
    # csvwriter.writerow(["University", "Country", "Name", "Email", "Website", "Research Areas"])

    # University and country information
    university = "Gifu University, Engineering Faculty"
    country = "Japan"
    profs = []

    # Keywords for filtering relevant faculty
    keyword_list = [
        'embedded systems', 'embedded software', 'hardware systems',
        'system architecture', 'IoT', 'real-time systems',
        'operating systems', 'system programming', 'system software',
        'distributed systems', 'kernel', 'machine learning', 'deep learning', 'artificial intelligence'
    ]

    # Process each row to extract faculty details
    for row in rows:
        try:
            # Extract professor's name
            name_tag = row.find_all("td")[1].find("a")
            name = name_tag.get_text(strip=True) if name_tag else "Not Found"
            profile_url = base_url + name_tag['href'] if name_tag else "Not Found"

            # Extract email
            email_tag = row.find_all("td")[3]
            email = email_tag.get_text(strip=True) if email_tag else "Not Found"

            # Extract website
            website_tag = row.find_all("td")[4].find("a")
            website = website_tag['href'] if website_tag else "Not Found"

            # Extract research areas
            research_area_tag = row.find_all("td")[5]
            research_area = research_area_tag.get_text(strip=True) if research_area_tag else "Not Found"

            # Check if research matches any keywords
            if any(re.search(keyword, research_area, re.IGNORECASE) for keyword in keyword_list):
                # Save the relevant professor's details to the text and CSV files
                # txt_file.write(f"Name: {name}\nEmail: {email}\nWebsite: {website}\nUniversity: {university}\nCountry: {country}\nResearch Areas: {research_area}\n\n")
                # csvwriter.writerow([university, country, name, email, website, research_area])
                profs.append([university, country, name, email, website])

        except Exception as e:
            print(f"Error processing a professor section: {e}")

    # Close files
    # txt_file.close()
    # csv_file.close()

    print("Gifu University faculty data extraction complete")
    return profs

if __name__ == "__main__":
    gifu_university_faculty()
