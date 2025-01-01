from bs4 import BeautifulSoup
import requests
import csv

# Set the target URL
url = "https://www.uni-marburg.de/en/fb12/research-groups"

# Send a GET request to the page
response = requests.get(url)
response.raise_for_status()  # Check if the request was successful

# Parse the HTML content with BeautifulSoup
soup = BeautifulSoup(response.text, "html.parser")

# Set the university and country information
university_name = "University of Marburg"
country = "Germany"

# Keywords to filter research areas
keywords = [
    'embedded systems', 'embedded software', 'operating systems',
    'real-time systems', 'IoT', 'distributed systems',
    'system programming', 'system software', 'kernel'
]

# Prepare output files
output_file = "unimarburg_filtered_faculty.csv"
with open(output_file, mode='w', newline='', encoding='utf-8') as file:
    csvwriter = csv.writer(file)
    # Write the header
    csvwriter.writerow(["University", "Country", "Professor Name", "Email", "Website Link", "Research Keywords"])
    
    # Locate the relevant table rows in the HTML
    rows = soup.find_all('tr')  # Find all <tr> elements (each professor is inside a <tr>)

    for row in rows:
        # Extract professor name
        name_tag = row.find('strong')
        if name_tag:
            prof_name = name_tag.get_text(strip=True)
        else:
            continue  # Skip rows without a professor's name
        
        # Extract email
        email_tag = row.find('a', class_='email')
        email = email_tag.get('href', '').replace('mailto:', '') if email_tag else "Not provided"
        
        # Extract website link
        research_area_tag = row.find('a', class_='state-published internal')
        website_link = research_area_tag.get('href') if research_area_tag else "Not provided"
        
        # Extract and filter research keywords
        matching_keywords = []
        research_list = row.find_all('li')  # Research points are in <li> tags
        for research_item in research_list:
            text = research_item.get_text(strip=True).lower()
            if any(keyword in text for keyword in keywords):
                matching_keywords.append(text)
        
        # Write data only if matching keywords are found
        if matching_keywords:
            csvwriter.writerow([
                university_name, country, prof_name, email, website_link,
                ', '.join(matching_keywords)  # Join keywords into a single string
            ])

print(f"Filtered data saved to {output_file}")
