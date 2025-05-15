import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

# URL of the website to scrape
URL = "http://quotes.toscrape.com/"

def fetch_page(url):
    """Fetch HTML content from the URL."""
    response = requests.get(url)
    response.raise_for_status()
    return response.text

def parse_html(html):
    """Parse the HTML and extract quote, author, and tags."""
    soup = BeautifulSoup(html, "html.parser")
    records = []

    for quote_div in soup.select("div.quote"):
        # Extract quote text
        text = quote_div.select_one("span.text").get_text(strip=True)

        # Extract author name
        author = quote_div.select_one("small.author").get_text(strip=True)

        # Extract all tags for this quote
        tags = [tag.get_text(strip=True) for tag in quote_div.select("div.tags a.tag")]

        # Append the result as a dictionary
        records.append({
            "quote": text,
            "author": author,
            "tags": ";".join(tags)  # Join tags with semicolon
        })

    # Convert to a pandas DataFrame
    return pd.DataFrame(records)

def save_data(df, path="data/raw/quotes_with_tags.csv"):
    """Save the DataFrame to a CSV file."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    df.to_csv(path, index=False)
    print(f"✅ Saved {len(df)} records to {path}")

def main():
    html = fetch_page(URL)
    df = parse_html(html)
    save_data(df)

if __name__ == "__main__":
    main()
