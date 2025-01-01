import requests
from bs4 import BeautifulSoup
import csv

# Define base URL for the faculty page
BASE_URL = "https://csie.asia.edu.tw/en/associate_professors_2"

# Define the keyword list to match research interests
keyword_list = [
    'embedded systems', 'Embedded System', 'embedded software', 'hardware systems',
    'system architecture', 'IoT', 'real-time systems',
    'operating systems', 'Operating System', 'OS', 'system programming', 'system software',
    'distributed systems', 'kernel'
]

# Step 1: Scrape the faculty page
response = requests.get(BASE_URL)
soup = BeautifulSoup(response.text, 'html.parser')

# Step 2: Find all faculty members
faculty_data = []
faculty_members = soup.find_all('div', class_='i-member-item')

for faculty in faculty_members:
    # Extract name
    name_tag = faculty.find('span', class_='i-member-value member-data-value-name')
    name = name_tag.text.strip() if name_tag else 'N/A'

    # Extract email
    email_tag = faculty.find('a', href=lambda href: href and "mailto:" in href)
    email = email_tag.text.strip() if email_tag else 'N/A'

    # Extract research interests
    research_areas_tag = faculty.find('span', class_='i-member-value member-data-value-6')
    research_areas = research_areas_tag.text.strip() if research_areas_tag else 'N/A'

    # Match research interests with keyword list
    matched_interests = [interest for interest in research_areas.split(',') if any(keyword.lower() in interest.lower() for keyword in keyword_list)]

    # Only save data if there is a match
    if matched_interests:
        faculty_data.append({
            'Name': name,
            'Email': email,
            'Research Interests': ', '.join(matched_interests),  # Join matched interests as a string
        })

# Step 3: Save the filtered data to CSV
with open('asia_faculty_filtered.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=['Name', 'Email', 'Research Interests'])
    writer.writeheader()
    writer.writerows(faculty_data)

print("Data extraction completed! Check 'asia_faculty_filtered.csv'.")
