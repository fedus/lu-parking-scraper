import schedule

from typing import Iterable, Type
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from datetime import datetime
from time import sleep

from .models import Base, ParkingUsage, UsageDetail, BikeUsage
from .exceptions import ConfigException
from .parkings import get_parking
from .bikes import get_bikes
from .config import config

db_url = config.get("DB_URL", None)

if not db_url:
    raise ConfigException("Missing environment variable: DB_URL. Aborting.")

engine = create_engine(db_url, echo=int(config.get("ECHO_SQL", 1)))

def scrape_parkings(scraped_at: datetime):
    return map(lambda raw_usage: ParkingUsage(
        scraped_at=scraped_at,
        name=raw_usage.get("name"),
        city=raw_usage.get("city"),
        total=raw_usage.get("total"),
        used=raw_usage.get("used"),
        free=raw_usage.get("free"),
        detail=UsageDetail(
            disabled=raw_usage.get("free-detail").get("disabled") if "free-detail" in raw_usage else None,
            ev=raw_usage.get("free-detail").get("ev") if "free-detail" in raw_usage else None,
            general=raw_usage.get("free-detail").get("general") if "free-detail" in raw_usage else None
        )
    ), get_parking())

def scrape_bikes(scraped_at: datetime):
    return map(lambda raw_usage: BikeUsage(
        scraped_at=scraped_at,
        **raw_usage
    ), get_bikes())

def persist(usage: Iterable[Type[Base]]):
    print("Persisting ...")

    with Session(engine) as session:
        session.add_all(usage)
        session.commit()

def scrape_and_persist():
    try:
        scraped_at = datetime.now()

        print(f"Scraping at {scraped_at} ...")

        persist(scrape_parkings(scraped_at))
        persist(scrape_bikes(scraped_at))
    except Exception as e:
        print(f"Caught exception: {e}")

scrape_interval = config.get("SCRAPE_INTERVAL_MIN", 10)

print(f"Scraping every {scrape_interval} minutes.")

scrape_and_persist()

schedule.every(scrape_interval).minutes.do(scrape_and_persist)

while True:
    schedule.run_pending()
    sleep(1)
