import requests
from bs4 import BeautifulSoup
import csv
import re

def extract_data_from_cuchd():
    url = "https://www.cuchd.in/uie/ece-engg/faculty-list.php"  # Faculty page URL
    response = requests.get(url)  # Send a GET request to fetch the page content
    
    if response.status_code != 200:
        print("Failed to retrieve the page")
        return
    
    # Parse the page content using BeautifulSoup
    soup = BeautifulSoup(response.text, "html.parser")

    # File setup for output
    filename = "cuchd_faculty.txt"
    f = open(filename, "w")
    
    excel_filename = "cuchd_faculty.csv"
    f2 = open(excel_filename, "w", newline='', encoding="utf-8")
    csvwriter = csv.writer(f2)

    # Set the university name and country
    u_name = "Chandigarh University"
    country = "India"
    
    # Research keywords for embedded systems or operating systems
    keyword_list = [
        'embedded systems', 'Embedded System', 'embedded software', 'hardware systems',
        'system architecture', 'IoT', 'real-time systems',
        'operating systems', 'Operating System', 'OS', 'system programming', 'system software',
        'distributed systems', 'kernel'
    ]
    
    # Extract faculty information from the table
    faculty_table = soup.find('table', {'id': 'customers'})
    rows = faculty_table.find_all('tr')[1:]  # Skip the header row

    for row in rows:
        columns = row.find_all('td')
        
        # Extracting name, specialization (research area)
        name = columns[0].get_text(strip=True) if len(columns) > 0 else "Not Found"
        specialization = columns[2].get_text(strip=True) if len(columns) > 2 else "Not Found"
        
        # Check if any research interest matches our criteria
        flag = False
        for keyword in keyword_list:
            if re.search(keyword, specialization, re.IGNORECASE):
                flag = True
                break
        
        # If keyword matches, write to files
        if flag:
            f.write(f"Name: {name}\nUniversity: {u_name}\nResearch Areas: {specialization}\n\n")
            csvwriter.writerow([u_name, country, name, specialization])
    
    # Close the files
    f.close()
    f2.close()

    print("Data extraction complete")

if __name__ == '__main__':
    extract_data_from_cuchd()
