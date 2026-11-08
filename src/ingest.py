import json
import os
from datetime import date
from pathlib import Path

import requests
from dotenv import load_dotenv

load_dotenv()  # reads your .env file

APP_ID = os.getenv("ADZUNA_APP_ID")
APP_KEY = os.getenv("ADZUNA_APP_KEY")
BASE_URL = "https://api.adzuna.com/v1/api/jobs/us/search/1"


def fetch_jobs(search_term: str) -> dict:
    """Call the Adzuna API and return the JSON response."""
    params = {
        "app_id": APP_ID,
        "app_key": APP_KEY,
        "what": search_term,
        "results_per_page": 50,
    }
    print("APP_ID:", APP_ID, "APP_KEY set:", bool(APP_KEY))
    response = requests.get(BASE_URL, params=params, timeout=10)
    response.raise_for_status()  # raises an error for 4xx/5xx responses
    return response.json()


def save_raw(data: dict) -> Path:
    """Save the response to data/raw/jobs_YYYY-MM-DD.json and return the path."""
    folder = Path("data") / "raw"
    folder.mkdir(parents=True, exist_ok=True)

    file_path = folder / f"jobs_{date.today()}.json"

    with open(file_path, "w") as f:
        json.dump(data, f, indent=2)

    return file_path


if __name__ == "__main__":
    jobs = fetch_jobs("data engineer")
    path = save_raw(jobs)
    print(f"Saved {len(jobs['results'])} jobs to {path}")