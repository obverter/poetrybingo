# To add a new cell, type ''
# To add a new markdown cell, type ' [markdown]'

# sourcery skip: for-index-underscore
import pandas as pd
import requests
from datetime import datetime
from bs4 import BeautifulSoup
import json
import os
import sys
from typing import List, Dict, Any
from dataclasses import dataclass
import logging
from pathlib import Path
import platform
import traceback
import numpy as np

# Configure logging
log_dir = Path(__file__).parent.parent / "logs"
log_dir.mkdir(exist_ok=True)

# Set up file handler for detailed logging
log_file = log_dir / f"scraper_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
file_handler = logging.FileHandler(log_file)
file_handler.setLevel(logging.DEBUG)

# Set up console handler for important messages
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Create formatters and add them to the handlers
file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console_formatter = logging.Formatter('%(levelname)s: %(message)s')
file_handler.setFormatter(file_formatter)
console_handler.setFormatter(console_formatter)

# Get the logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(file_handler)
logger.addHandler(console_handler)

def log_system_info():
    """Log system information for debugging."""
    logger.info("System Information:")
    logger.info(f"Python Version: {sys.version}")
    logger.info(f"Platform: {platform.platform()}")
    logger.info(f"NumPy Version: {np.__version__}")
    logger.info(f"Pandas Version: {pd.__version__}")
    logger.info(f"Requests Version: {requests.__version__}")
    logger.info(f"BeautifulSoup4 Version: {BeautifulSoup.__version__}")
    logger.info(f"Working Directory: {os.getcwd()}")
    logger.info(f"Script Location: {Path(__file__).absolute()}")

@dataclass
class Article:
    headline: str
    tags: List[str]
    timestamp: str
    year: int
    month: int
    day: int
    hour: int
    minute: int

class TMZScraper:
    def __init__(self, base_url: str = "https://www.tmz.com"):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        self.parent_dir = Path(__file__).parent.parent
        logger.info(f"Initialized TMZScraper with base_url: {base_url}")

    def fetch_page(self) -> BeautifulSoup:
        """Fetch and parse the TMZ homepage."""
        try:
            logger.info("Fetching TMZ homepage...")
            response = self.session.get(self.base_url)
            response.raise_for_status()
            logger.debug(f"Response status code: {response.status_code}")
            return BeautifulSoup(response.text, "html.parser")
        except requests.RequestException as e:
            logger.error(f"Failed to fetch TMZ homepage: {e}")
            logger.error(f"Response content: {getattr(e.response, 'text', 'No response content')}")
            raise

    def get_headlines(self, doc: BeautifulSoup) -> List[str]:
        """Extract headlines from the page."""
        raw_titles = doc.select("header > a > h2")
        if not raw_titles:
            logger.warning("No headlines found. The website structure might have changed.")
            logger.debug("Page content: %s", doc.prettify()[:1000])  # Log first 1000 chars of page
            return []

        headlines = []
        valid_punct = ["'", "!", "?"]
        for title in raw_titles:
            headline = title.get_text().strip().replace("\n", " ") + "."
            if headline[-2] in valid_punct:
                headline = headline[:-1]
            headlines.append(headline)
        logger.info(f"Found {len(headlines)} headlines")
        return headlines

    def get_tags(self, doc: BeautifulSoup, position: int) -> List[str]:
        """Get tags for a specific article position."""
        tags = doc.select("section.tag-cloud > ul > a")
        tag_list = []
        for tag in tags:
            try:
                data = json.loads(tag["data-context"])
                if data["pos"] == position:
                    tag_list.append(tag.text.strip())
            except (json.JSONDecodeError, KeyError) as e:
                logger.warning(f"Error parsing tag data: {e}")
                logger.debug(f"Tag HTML: {tag}")
        return tag_list

    def parse_timestamp(self, timestamp_text: str) -> Dict[str, Any]:
        """Parse timestamp into its components."""
        try:
            timestamp = timestamp_text.split("PT")[-20:]
            timestamp = timestamp[0][-20:].strip()
            dt = datetime.strptime(timestamp, "%m/%d/%Y %I:%M %p")
            return {
                "calendar": timestamp[:9],
                "clock": timestamp[-8:].strip(),
                "year": dt.year,
                "month": dt.month,
                "day": dt.day,
                "hour": dt.hour,
                "minute": dt.minute,
            }
        except ValueError as e:
            logger.error(f"Error parsing timestamp: {e}")
            logger.error(f"Timestamp text: {timestamp_text}")
            raise

    def process_articles(self, doc: BeautifulSoup) -> List[Article]:
        """Process all articles from the page."""
        articles = []
        raw_titles = doc.select("header > a > h2")
        timestamps = doc.select(".article")

        logger.info(f"Processing {len(raw_titles)} articles")
        for idx, (title, timestamp) in enumerate(zip(raw_titles, timestamps)):
            try:
                headline = title.get_text().strip().replace("\n", " ") + "."
                if headline[-2] in ["'", "!", "?"]:
                    headline = headline[:-1]

                timestamp_text = timestamp.text.split("PT")[-20:]
                timestamp_text = timestamp_text[0][-20:].strip()
                
                time_data = self.parse_timestamp(timestamp_text)
                tags = self.get_tags(doc, idx + 1)

                article = Article(
                    headline=headline,
                    tags=tags,
                    timestamp=timestamp_text,
                    **time_data
                )
                articles.append(article)
                logger.debug(f"Processed article {idx + 1}: {headline}")
            except Exception as e:
                logger.error(f"Error processing article {idx}: {e}")
                logger.error(f"Article HTML: {title}")
                logger.error(f"Timestamp HTML: {timestamp}")
                continue

        return articles

    def save_data(self, articles: List[Article]):
        """Save articles to CSV and JSON files."""
        try:
            current_df = pd.DataFrame([vars(article) for article in articles])
            logger.info(f"Created DataFrame with {len(current_df)} rows")
            
            # Read existing data
            headlines_csv_path = self.parent_dir / "headlines.csv"
            try:
                existing_df = pd.read_csv(headlines_csv_path, index_col="Unnamed: 0")
                logger.info(f"Loaded existing data with {len(existing_df)} rows")
            except FileNotFoundError:
                logger.info("No existing headlines.csv found. Creating new file.")
                existing_df = pd.DataFrame(columns=current_df.columns)

            # Combine and deduplicate
            combined_df = pd.concat([current_df, existing_df])
            combined_df = combined_df.sort_values(
                by=["year", "month", "day", "hour", "minute"],
                ascending=[False, False, False, False, False],
                ignore_index=True
            )
            combined_df = combined_df.drop_duplicates(subset=["timestamp"], keep="first", ignore_index=True)
            logger.info(f"Final DataFrame has {len(combined_df)} rows")

            # Save files
            combined_df.to_csv(headlines_csv_path)
            combined_df.to_json(self.parent_dir / "headlines.json")
            logger.info(f"Successfully updated headlines in {headlines_csv_path}")
            
        except Exception as e:
            logger.error(f"Error saving data: {e}")
            logger.error(f"Traceback: {traceback.format_exc()}")
            raise

    def run(self):
        """Main execution method."""
        try:
            log_system_info()
            logger.info("Starting scraper...")
            doc = self.fetch_page()
            articles = self.process_articles(doc)
            self.save_data(articles)
            logger.info("Scraper completed successfully")
        except Exception as e:
            logger.error(f"Scraper failed: {e}")
            logger.error(f"Traceback: {traceback.format_exc()}")
            sys.exit(1)

if __name__ == "__main__":
    scraper = TMZScraper()
    scraper.run()
