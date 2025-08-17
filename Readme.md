Quora Scraper

A Python-based scraper for collecting questions and answers from Quora using a valid user session.

Note: This project is still under development and may contain bugs.

Features(MVP)

Scrape Quora questions and answers by topic.

Navigate related questions using a keyword for broader data collection.

Uses your Quora login session for access.

Prerequisites

Python 3.x installed

Required Python libraries: selenium, pandas, etc.

Chrome browser with a Quora account

Setup

Export Quora Cookies

Install the Get cookies.txt Chrome extension.

Log in to Quora and export cookies as cookies.json.

Save cookies.json in the same directory as scrape.py.

Configure Scraper

Open scrape.py.

Set the start URL (line 87):

start_url = "https://www.quora.com/Enter-any-topic-of-your-choice"


Set the keyword (line 79) for related questions:

keyword = "YourKeywordHere"

Running the Scraper
python scrape.py


Loads your Quora session from cookies.

Scrapes questions and answers for the given topic and keyword.

Note: Make sure your cookies are valid. Expired cookies will prevent access.
