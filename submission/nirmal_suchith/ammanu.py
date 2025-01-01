import requests
from bs4 import BeautifulSoup
import csv

# Define base URL for the academic staff page
BASE_URL = "https://fit.ammanu.edu.jo/academic-staff/"

# Define the keyword list to match research interests
keyword_list = [
    'embedded systems', 'Embedded System', 'embedded software', 'hardware systems',
    'system architecture', 'IoT', 'real-time systems',
    'operating systems', 'Operating System', 'OS', 'system programming', 'system software',
    'distributed systems', 'kernel'
]

# Step 1: Scrape faculty profile links
response = requests.get(BASE_URL)
soup = BeautifulSoup(response.text, 'html.parser')

# Extract faculty profile links
profile_links = []
faculty_cards = soup.find_all('a', class_='cardlink')
for card in faculty_cards:
    link = card.get('href')
    if link:
        profile_links.append(link)

# Step 2: Visit each profile and extract relevant data
faculty_data = []

for profile_url in profile_links:
    profile_response = requests.get(profile_url)
    profile_soup = BeautifulSoup(profile_response.text, 'html.parser')

    # Extract name
    name = profile_soup.find('h1', class_='heading8 profileh').text.strip()

    # Extract email
    email = profile_soup.find('a', href=lambda href: href and "mailto:" in href).text.strip()

    # Extract research interests (courses taught section)
    courses_section = profile_soup.find('ul', id='courses')
    research_interests = [li.text.strip() for li in courses_section.find_all('li')] if courses_section else []

    # Match research interests with keyword list
    matched_interests = [interest for interest in research_interests if any(keyword.lower() in interest.lower() for keyword in keyword_list)]

    # Only save data if there is a match
    if matched_interests:
        faculty_data.append({
            'Name': name,
            'Email': email,
            'Research Interests': ', '.join(matched_interests),  # Join matched interests as a string
        })

# Step 3: Save the filtered data to CSV
with open('ammanu_filtered.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=['Name', 'Email', 'Research Interests'])
    writer.writeheader()
    writer.writerows(faculty_data)

print("Data extraction completed! Check 'ammanu_filtered.csv'.")
