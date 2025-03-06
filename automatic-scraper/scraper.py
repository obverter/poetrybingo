# To add a new cell, type ''
# To add a new markdown cell, type ' [markdown]'

# sourcery skip: for-index-underscore
import pandas as pd
import requests
from datetime import datetime
from bs4 import BeautifulSoup
import bs4
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
import gzip
import shutil
from concurrent.futures import ThreadPoolExecutor
import time

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
    logger.info(f"BeautifulSoup4 Version: {bs4.__version__}")
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
    calendar: str
    clock: str

class TMZScraper:
    def __init__(self, base_url: str = "https://www.tmz.com", max_articles: int = 50, delay: float = 1.0):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        self.parent_dir = Path(__file__).parent.parent
        self.max_retries = 3
        self.retry_delay = 5  # seconds
        self.max_articles = max_articles
        self.request_delay = delay
        self.temp_file = self.parent_dir / "temp_headlines.csv"
        logger.info(f"Initialized TMZScraper with base_url: {base_url}, max_articles: {max_articles}, delay: {delay}s")

    def fetch_page(self) -> BeautifulSoup:
        """Fetch and parse the TMZ homepage with retries."""
        for attempt in range(self.max_retries):
            try:
                logger.info(f"Fetching TMZ homepage (attempt {attempt + 1}/{self.max_retries})...")
                response = self.session.get(self.base_url, timeout=10)
                response.raise_for_status()
                logger.debug(f"Response status code: {response.status_code}")
                return BeautifulSoup(response.text, "html.parser")
            except requests.RequestException as e:
                if attempt < self.max_retries - 1:
                    logger.warning(f"Attempt {attempt + 1} failed: {e}")
                    time.sleep(self.retry_delay)
                    continue
                logger.error(f"Failed to fetch TMZ homepage after {self.max_retries} attempts: {e}")
                logger.error(f"Response content: {getattr(e.response, 'text', 'No response content')}")
                raise

    def get_headlines(self, doc: BeautifulSoup) -> List[str]:
        """Extract headlines from the page."""
        raw_titles = doc.select("header > a > h2")
        if not raw_titles:
            logger.warning("No headlines found. The website structure might have changed.")
            logger.debug("Page content: %s", doc.prettify()[:1000])
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
            # Clean up the timestamp text
            timestamp_text = timestamp_text.strip()
            
            # Handle different timestamp formats
            try:
                # Try the original format first
                dt = datetime.strptime(timestamp_text, "%m/%d/%Y %I:%M %p")
            except ValueError:
                # Try alternative format without AM/PM
                dt = datetime.strptime(timestamp_text, "%m/%d/%Y %H:%M")
            
            return {
                "calendar": dt.strftime("%m/%d/%Y"),
                "clock": dt.strftime("%I:%M %p"),
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

    def validate_article(self, article: Article) -> bool:
        """Validate article data before saving."""
        try:
            # Check required fields
            if not article.headline or not article.timestamp:
                return False
            
            # Validate timestamp format
            datetime.fromisoformat(article.timestamp.replace("Z", "+00:00"))
            
            # Validate date components
            if not (1 <= article.month <= 12 and 1 <= article.day <= 31 and 
                   0 <= article.hour <= 23 and 0 <= article.minute <= 59):
                return False
            
            return True
        except Exception as e:
            logger.warning(f"Article validation failed: {e}")
            return False

    def save_temp_data(self, articles: List[Article]):
        """Save articles to a temporary file for recovery."""
        try:
            if articles:
                temp_df = pd.DataFrame([vars(article) for article in articles])
                temp_df.to_csv(self.temp_file, index=False)
                logger.info(f"Saved {len(articles)} articles to temporary file")
        except Exception as e:
            logger.error(f"Error saving temporary data: {e}")

    def process_articles(self, doc: BeautifulSoup) -> List[Article]:
        """Process all articles from the page."""
        articles = []
        raw_titles = doc.select("header > a > h2")
        timestamps = doc.select("time.published-datetime")

        logger.info(f"Processing {len(raw_titles)} articles")
        for idx, (title, timestamp) in enumerate(zip(raw_titles, timestamps)):
            if idx >= self.max_articles:
                logger.info(f"Reached maximum article limit ({self.max_articles})")
                break

            try:
                headline = title.get_text().strip().replace("\n", " ") + "."
                if headline[-2] in ["'", "!", "?"]:
                    headline = headline[:-1]

                # Extract timestamp from datetime attribute
                timestamp_text = timestamp.get("datetime", "").strip()
                if not timestamp_text:
                    logger.warning(f"No datetime attribute found for article {idx}")
                    continue
                
                # Parse the ISO format timestamp
                dt = datetime.fromisoformat(timestamp_text.replace("Z", "+00:00"))
                time_data = {
                    "calendar": dt.strftime("%m/%d/%Y"),
                    "clock": dt.strftime("%I:%M %p"),
                    "year": dt.year,
                    "month": dt.month,
                    "day": dt.day,
                    "hour": dt.hour,
                    "minute": dt.minute,
                }
                
                tags = self.get_tags(doc, idx + 1)

                article = Article(
                    headline=headline,
                    tags=tags,
                    timestamp=timestamp_text,
                    **time_data
                )

                # Validate article before adding
                if self.validate_article(article):
                    articles.append(article)
                    logger.debug(f"Processed article {idx + 1}: {headline}")
                else:
                    logger.warning(f"Skipping invalid article: {headline}")

                # Add delay between processing articles
                time.sleep(self.request_delay)

            except Exception as e:
                logger.error(f"Error processing article {idx}: {e}")
                logger.error(f"Article HTML: {title}")
                logger.error(f"Timestamp HTML: {timestamp}")
                continue

        return articles

    def compress_file(self, file_path: Path):
        """Compress a file using gzip."""
        try:
            with open(file_path, 'rb') as f_in:
                with gzip.open(f"{file_path}.gz", 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)
            # Remove original file after successful compression
            file_path.unlink()
            logger.info(f"Compressed {file_path}")
        except Exception as e:
            logger.error(f"Error compressing {file_path}: {e}")
            raise

    def save_data(self, articles: List[Article]):
        """Save articles to CSV and JSON files with compression."""
        try:
            # Save temporary data for recovery
            self.save_temp_data(articles)

            current_df = pd.DataFrame([vars(article) for article in articles])
            logger.info(f"Created DataFrame with {len(current_df)} rows")
            
            # Read existing data in chunks to manage memory
            headlines_csv_path = self.parent_dir / "headlines.csv"
            headlines_json_path = self.parent_dir / "headlines.json"
            
            try:
                # Try to read from compressed file first
                if (headlines_csv_path.with_suffix('.csv.gz')).exists():
                    existing_df = pd.read_csv(
                        headlines_csv_path.with_suffix('.csv.gz'),
                        compression='gzip',
                        chunksize=10000  # Process in chunks
                    )
                    # Combine chunks efficiently
                    existing_df = pd.concat(existing_df, ignore_index=True)
                else:
                    existing_df = pd.read_csv(headlines_csv_path, chunksize=10000)
                    existing_df = pd.concat(existing_df, ignore_index=True)
                logger.info(f"Loaded existing data with {len(existing_df)} rows")
                
                # Only append new articles using efficient set operations
                existing_timestamps = set(existing_df['timestamp'])
                new_articles = current_df[~current_df['timestamp'].isin(existing_timestamps)]
                
                if len(new_articles) > 0:
                    logger.info(f"Adding {len(new_articles)} new articles")
                    combined_df = pd.concat([new_articles, existing_df])
                else:
                    logger.info("No new articles to add")
                    combined_df = existing_df
            except FileNotFoundError:
                logger.info("No existing headlines.csv found. Creating new file.")
                combined_df = current_df

            # Sort and deduplicate efficiently
            combined_df = combined_df.sort_values(
                by=["year", "month", "day", "hour", "minute"],
                ascending=[False, False, False, False, False],
                ignore_index=True
            )
            combined_df = combined_df.drop_duplicates(subset=["timestamp"], keep="first", ignore_index=True)
            logger.info(f"Final DataFrame has {len(combined_df)} rows")

            # Save files with compression and memory optimization
            combined_df.to_csv(headlines_csv_path, index=False, compression='gzip')
            combined_df.to_json(headlines_json_path, orient='records', lines=True, compression='gzip')
            
            # Clear memory
            del combined_df
            del existing_df
            del current_df
            import gc
            gc.collect()
            
            # Remove temporary file after successful save
            if self.temp_file.exists():
                self.temp_file.unlink()
            
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
            # Try to recover data from temporary file
            if self.temp_file.exists():
                try:
                    recovered_df = pd.read_csv(self.temp_file)
                    recovered_df.to_csv(self.parent_dir / "recovered_headlines.csv", index=False)
                    logger.info("Recovered data saved to recovered_headlines.csv")
                except Exception as recovery_error:
                    logger.error(f"Failed to recover data: {recovery_error}")
            sys.exit(1)

if __name__ == "__main__":
    scraper = TMZScraper(max_articles=50, delay=1.0)  # Limit to 50 articles with 1 second delay
    scraper.run()
