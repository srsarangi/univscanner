import requests
from bs4 import BeautifulSoup
import csv
import re

def buet_faculty_scraper():
    # Base URL and Faculty Members Page
    base_url = "https://name.buet.ac.bd"
    faculty_url = f"{base_url}/faculty-members"

    # Output file setup
    output_filename = "buet_faculty.csv"
    with open(output_filename, "w", newline='', encoding="utf-8") as file:
        csvwriter = csv.writer(file)
        csvwriter.writerow(["Name", "Email", "Research Areas", "Profile Link"])

        # Keywords for filtering research areas
        keyword_list = [
            'embedded systems', 'Embedded System', 'embedded software', 'hardware systems',
            'system architecture', 'IoT', 'real-time systems',
            'operating systems', 'Operating System', 'OS', 'system programming', 'system software',
            'distributed systems', 'kernel'
        ]

        # Fetch and parse the main faculty page
        response = requests.get(faculty_url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        # Locate all faculty profile links
        faculty_blocks = soup.find_all('div', class_='col-12 col-md-3 team-block text-left team-style-1 sm-margin-ten-bottom mb-5')

        for block in faculty_blocks:
            # Extract the profile link
            profile_link_tag = block.find('div', class_='text-extra-small text-uppercase text-medium-gray alt-font').find('a', href=True)
            if profile_link_tag:
                profile_url = profile_link_tag['href']

                # Fetch and parse the individual profile page
                profile_response = requests.get(profile_url)
                profile_response.raise_for_status()
                profile_soup = BeautifulSoup(profile_response.text, "html.parser")

                # Extract name
                name_tag = profile_soup.find('h1', class_='text-extra-dark-gray font-weight-600 mb-0')
                name = name_tag.get_text(strip=True) if name_tag else "Not Found"

                # Extract email
                email_tag = profile_soup.find('a', href=re.compile(r"mailto:"))
                email = email_tag.get_text(strip=True) if email_tag else "Not Found"

                # Extract research areas
                research_list = profile_soup.find('ul', class_='p-md-0 list-style-1 ml-3')
                research_areas = ", ".join([li.get_text(strip=True) for li in research_list.find_all('li')]) if research_list else "Not Found"

                # Check if research areas match any keywords
                match_found = any(re.search(keyword, research_areas, re.IGNORECASE) for keyword in keyword_list)

                if match_found:
                    csvwriter.writerow([name, email, research_areas, profile_url])

    print(f"Data extraction complete. Saved to {output_filename}")

if __name__ == '__main__':
    buet_faculty_scraper()
