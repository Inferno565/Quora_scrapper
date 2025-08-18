# Quora Scraper

A Python-based scraper for collecting questions and answers from Quora using a valid user session.

> **Note:** This project is still under development and may contain bugs.

## Responsible Use

- This scraper is intended **only for analyzing content on certain subjects via Quora**  
- It is **not meant to violate Quora's Terms of Service** or use the data for commercial purposes  
- Users should **respect Quora’s policies** and avoid misuse of scraped data

---

## Features (MVP)

- Scrape Quora questions and answers by topic
- Navigate related questions using a keyword for broader data collection
- Uses your Quora login session for access

---

## Prerequisites

- Python 3.x installed
- Required Python libraries: `selenium`, `pandas`, etc.
- Chrome browser with a Quora account

---

## Setup

### 1. Export Quora Cookies

- Install the [Get cookies.txt Chrome extension](https://chromewebstore.google.com/detail/cclelndahbckbenkjhflpdbgdldlbecc?utm_source=item-share-cb)
- Log in to Quora and export cookies as `cookies.json`
- Save `cookies.json` in the same directory as `scrape.py`

### 2. Configure Scraper

- Open `scrape.py`
- Set the **start URL** (line 87):

start_url = "https://www.quora.com/Enter-any-topic-of-your-choice"

Set the keyword to that of your choice (line 79) for related questions
## Running the Scraper

When you run the scraper:

- **Loads your Quora session from cookies**  
- **Scrapes questions and answers for the given topic and keyword**  

> **Note:** Make sure your cookies are valid. Expired cookies will prevent access.

---
