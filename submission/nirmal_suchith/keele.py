import requests
from bs4 import BeautifulSoup
import csv
import re

def keele_university():
    base_url = "https://www.keele.ac.uk"  # Base URL for the university site
    url = f"{base_url}/scm/staff/"  # Faculty page URL
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    # File setup for output
    filename = "keele_university_faculty.txt"
    f = open(filename, "w")

    excel_filename = "keele_university_faculty.csv"
    f2 = open(excel_filename, "w", newline='', encoding="utf-8")
    csvwriter = csv.writer(f2)

    # Set the university name and country
    u_name = "Keele University"
    country = "UK"
    
    # Research keywords for embedded systems or operating systems
    keyword_list = [
        'embedded systems', 'Embedded System', 'embedded software', 'hardware systems',
        'system architecture', 'IoT', 'real-time systems',
        'operating systems', 'Operating System', 'OS', 'system programming', 'system software',
        'distributed systems', 'kernel'
    ]

    # Extracting all faculty profiles (divs with class 'staff-card')
    staff_profiles = soup.find_all('div', class_='staff-card')

    for profile in staff_profiles:
        # Extracting name and profile link
        name_tag = profile.find('strong')
        name = name_tag.get_text(strip=True) if name_tag else "Not Found"
        profile_link = profile.find('a')['href'] if profile.find('a') else None

        # Extracting email
        email_tag = profile.find('a', href=re.compile("mailto:"))
        email = email_tag.get_text(strip=True) if email_tag else "Not Found"

        # Open the individual faculty page to extract research interests
        if profile_link:
            # Ensure the profile link is correctly formatted
            if profile_link.startswith('http') or profile_link.startswith('https'):
                profile_url = profile_link  # Use the link directly if it's a full URL
            else:
                profile_url = f"{base_url}{profile_link}"  # Prepend the base URL

            profile_response = requests.get(profile_url)
            profile_soup = BeautifulSoup(profile_response.text, "html.parser")
            
            # Extracting research interests
            research_interests = ""
            research_tag = profile_soup.find('div', class_='tab__pane', id="research-themes")
            if research_tag:
                research_interests = ", ".join([li.get_text(strip=True) for li in research_tag.find_all('li')])

            # Check if any research interest matches our criteria
            flag = False
            for keyword in keyword_list:
                if re.search(keyword, research_interests, re.IGNORECASE):
                    flag = True
                    break

            # If keyword matches, write to files
            if flag:
                f.write(f"Name: {name}\nEmail: {email}\nUniversity: {u_name}\nResearch Areas: {research_interests}\n\n")
                csvwriter.writerow([u_name, country, name, email, research_interests])

    # Close the files
    f.close()
    f2.close()

    print("Data extraction complete")

if __name__ == '__main__':
    keele_university()
