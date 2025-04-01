from typing import List, Dict
from pydantic import BaseModel


class PathConfig(BaseModel):
    path: str
    selectors: List[str]


class WebsiteConfig(BaseModel):
    domain: str
    paths: List[PathConfig]


class Config(BaseModel):
    websites: List[WebsiteConfig]


WEBSITE_CONFIGS = [
    WebsiteConfig(
        domain="scale.com",
        paths=[
            PathConfig(
                path="customers",
                selectors=[
                    "#__next > main > div > div > div > section.ρd__all.ρd__section.ρqbiq8 > div > div > div > div > ul > li > div > img",
                    "#__next > main > div > div > div > section.ρd__all.ρd__section.ρvt7K6 > div > div > div > div > a > div.ρd__all.ρd__div.ρcDpFy > img",
                ],
            )
        ],
    ),
    WebsiteConfig(
        domain="webflow.com",
        paths=[
            PathConfig(
                path="customers?page=1000000",  # Paging on this site is "additive" so we can avoid it this way
                selectors=["img.customers-hero_logo", "img.customers_logos"],
            )
        ],
    ),
    WebsiteConfig(
        domain="www.11x.ai",
        paths=[
            PathConfig(path="", selectors=["div.logo3_wrapper img"]),
            # PathConfig(path="customers") # Linked on the homepage, but returns 404 currently
        ],
    ),
]

config = Config(websites=WEBSITE_CONFIGS)
