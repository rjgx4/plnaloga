import requests
import logging
import argparse
import json

from bs4 import BeautifulSoup
from typing import List
from urllib.parse import urljoin
from pydantic import BaseModel
from config import config, WebsiteConfig

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class LogoResult(BaseModel):
    url: str
    alt_text: str
    inferred_name: str | None = None


def fetch_page(url: str) -> BeautifulSoup:
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return BeautifulSoup(response.text, "html.parser")


def extract_logos(soup: BeautifulSoup, selectors: List[str], base_url: str) -> List[LogoResult]:
    logos = []

    for selector in selectors:
        for img in soup.select(selector):
            src = img.get("src")
            if src:
                absolute_url = urljoin(base_url, src)
                alt_text = img.get("alt", "")
                logo_result = LogoResult(url=absolute_url, alt_text=alt_text)
                logos.append(logo_result)

    return logos


def scrape_logos(website_config: WebsiteConfig) -> List[LogoResult]:
    found_logos = []
    base_url = f"https://{website_config.domain}"

    for path_config in website_config.paths:
        url = urljoin(base_url, path_config.path)
        try:
            soup = fetch_page(url)
            page_logos = extract_logos(soup, path_config.selectors, url)

            for logo in page_logos:
                found_logos.append(logo)

        except requests.RequestException as e:
            logger.error(f"Error scraping {url}: {str(e)}")
            continue

    return found_logos


def to_json_file(logos: List[LogoResult], filename: str):
    with open("data/" + filename, "w") as f:
        json.dump([logo.model_dump() for logo in logos], f, indent=2)


def main(infer_names: bool = False):
    for website in config.websites:
        logos = scrape_logos(website)
        logger.info(f"\nFound {len(logos)} logos for {website.domain}:")
        for logo in logos:
            logger.info(f"{logo.url} (alt: {logo.alt_text})")
            if infer_names:
                from ml import infer_logo_name

                inferred_name = infer_logo_name(logo)
                logger.info(f"Inferred name: {inferred_name} for {logo.url}")
                logo.inferred_name = inferred_name

        to_json_file(logos, f"{website.domain}.json")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--infer-names",
        action="store_true",
        help="Enable logo name inference using a local visual LLM",
    )
    args = parser.parse_args()

    main(infer_names=args.infer_names)
