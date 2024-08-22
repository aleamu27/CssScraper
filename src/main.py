import requests
from bs4 import BeautifulSoup
import csv
from urllib.parse import urlparse, urlunparse
import re


def validate_url(url):
    parsed = urlparse(url)
    if not parsed.scheme:
        return urlunparse(('https', *parsed[1:]))
    return url


def scrape_website(url, selector):
    url = validate_url(url)
    print(f"Attempting to scrape: {url}")

    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"An error occurred while fetching the URL: {e}")
        return None

    soup = BeautifulSoup(response.text, 'html.parser')
    elements = soup.select(selector)

    print(f"Found {len(elements)} elements matching the selector.")

    # Extract text and filter for integers over 3 digits
    data = []
    for element in elements:
        text = element.get_text(strip=True)
        print(f"Raw text: {text}")
        numbers = re.findall(r'\b\d{4,}\b', text)
        if numbers:
            data.extend(numbers)
        else:
            data.append(text)  # Include non-numeric text as well

    print(f"Extracted {len(data)} items after filtering.")
    return data


def save_to_csv(data, filename):
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Scraped Data'])  # Header
        for item in data:
            writer.writerow([item])


def main():
    url = input("Enter the URL of the website you want to scrape: ")
    selector = input("Enter the CSS selector for the elements you want to scrape: ")
    output_file = input("Enter the name of the output CSV file: ")

    scraped_data = scrape_website(url, selector)

    if scraped_data:
        save_to_csv(scraped_data, output_file)
        print(f"{len(scraped_data)} items have been scraped and saved to {output_file}")
    else:
        print("No data was scraped.")


if __name__ == "__main__":
    main()
