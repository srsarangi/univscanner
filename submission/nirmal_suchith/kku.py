import requests
import csv
import re
from bs4 import BeautifulSoup
import ssl


class SSLAdapter(requests.adapters.HTTPAdapter):
    def __init__(self, **kwargs):
        self.context = ssl.create_default_context()
        self.context.options |= ssl.OP_LEGACY_SERVER_CONNECT
        super().__init__(**kwargs)

    def init_poolmanager(self, *args, **kwargs):
        kwargs['ssl_context'] = self.context
        return super().init_poolmanager(*args, **kwargs)


# Keywords to filter professors
keyword_list = [
    'embedded systems', 'Embedded System', 'embedded software', 'hardware systems',
    'system architecture', 'IoT', 'real-time systems',
    'operating systems', 'Operating System', 'OS', 'system programming', 'system software',
    'distributed systems', 'kernel'
]


def scrape_kku():
    session = requests.Session()
    session.mount("https://", SSLAdapter())

    url = "https://cs.kku.edu.sa/en/node/1411"

    try:
        r = session.get(url)
        r.raise_for_status()
        print("Page fetched successfully.")
    except requests.exceptions.RequestException as e:
        print("An error occurred:", e)
        return

    soup = BeautifulSoup(r.text, "html.parser")

    # Open CSV file for writing
    filename = "kku_filtered_faculty.csv"
    with open(filename, "w", newline='', encoding="utf-8") as f:
        csvwriter = csv.writer(f)
        csvwriter.writerow(["Name", "Email", "Research Area"])

        # Locate the table
        table = soup.find('table', style="width: 7.2e+2pt;border: none;border-collapse:collapse;")
        if not table:
            print("Faculty table not found.")
            return

        rows = table.find_all('tr')
        for row in rows:
            # Extract relevant <td> elements
            cells = row.find_all('td')
            if len(cells) < 5:  # Ensure there are enough columns
                continue

            # Extract name
            name_tag = cells[1].find('span', style="color:black;")
            name = name_tag.get_text(strip=True) if name_tag else "Name Not Found"

            # Extract research area
            research_tag = cells[3].find('span', style=re.compile("color:black;"))
            research_area = research_tag.get_text(strip=True) if research_tag else "Research Area Not Found"

            # Extract email
            email_tag = cells[4].find('span', style=re.compile("color:black;"))
            email = email_tag.get_text(strip=True) if email_tag else "Email Not Found"

            # Check if research area matches any keyword
            if any(keyword.lower() in research_area.lower() for keyword in keyword_list):
                csvwriter.writerow([name, email, research_area])

    print(f"Filtered data saved to {filename}")


if __name__ == '__main__':
    scrape_kku()
