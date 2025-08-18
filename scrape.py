# READ NOTE BEOFRE RUNNING 

import json
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException

options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
# options.add_argument("--headless")  

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)


driver.get("https://www.quora.com/")
time.sleep(3)

with open("cookies.json", "r") as f:
    cookies = json.load(f)

for cookie in cookies:
    cookie.pop("sameSite", None)
    try:
        driver.add_cookie(cookie)
    except:
        pass

driver.refresh()
time.sleep(5)


def scrape_answers(url):
    driver.get(url)
    time.sleep(5)
    
    # Interact with the dropdown to select "Answers"
    try:
        # Click the dropdown button
        dropdown_button = driver.find_element(By.XPATH, '//*[@id="mainContent"]/div[3]/div/div[1]/div/div/button')
        dropdown_button.click()
        time.sleep(2)
        
        # Find and click the "Answers" option using the new XPath
        answers_option = driver.find_element(By.XPATH, '//*[@id="mainContent"]/div[3]/div/div[1]/div/div[2]/div/div[1]/div/div/div[2]')
        answers_option.click()
        time.sleep(3)
    except NoSuchElementException:
        print("Dropdown or 'Answers' option not found, continuing without selection.")
    except Exception as e:
        print(f"Error interacting with dropdown: {e}")


    # scroll dynamically until no new answers are loaded
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.find_element(By.TAG_NAME, "body").send_keys(Keys.END)
        time.sleep(2)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    # expand all "Read more"
    read_more_buttons = driver.find_elements(By.XPATH, '//span[contains(@class, "qt_read_more")]')
    for btn in read_more_buttons:
        try:
            driver.execute_script("arguments[0].click();", btn)
            time.sleep(0.3)
        except:
            pass

    # extract answers
    answers_list = []
    answers = driver.find_elements(By.XPATH, '//div[contains(@class, "spacing_log_answer_content")]')
    for i, answer in enumerate(answers, 1):
        text = answer.text.strip()
        if text:
            answers_list.append({"Question URL": url, "Answer No": i, "Text": text})

    return answers_list


def get_related_links_from_container():
    related_urls = []
    try:
        container = driver.find_element(By.XPATH, '//*[@id="mainContent"]/div[7]/div')
        links = container.find_elements(By.TAG_NAME, "a")
        for link in links:
            url = link.get_attribute("href")
            title = link.text.lower()
            if "Your-choice-keyword" in title and url not in visited_urls:
                related_urls.append(url)
    except Exception as e:
        print("No related container found or error:", e)

    return list(set(related_urls))


start_url = "https://www.quora.com/Enter-topic-of-fyour-choice"
queue = [start_url]
visited_urls = set()
all_answers = []

max_levels = 10
current_level = 0

while queue and current_level < max_levels:
    current_url = queue.pop(0)
    if current_url in visited_urls:
        continue

    print(f"Scraping: {current_url}")
    
    # If the URL contains "unanswered", skip scraping answers
    if "unanswered" in current_url.lower():
        print("Skipping answers for unanswered question.")
        visited_urls.add(current_url)
        try:
            new_links = get_related_links_from_container()
            queue.extend(new_links)
        except Exception as e:
            print(f"Error getting related links for {current_url}: {e}")
        continue # Move to the next URL in the queue
    
    try:
        scraped_answers = scrape_answers(current_url)
        all_answers.extend(scraped_answers)
        visited_urls.add(current_url)

        # get related links
        new_links = get_related_links_from_container()
        queue.extend(new_links)
    except Exception as e:
        print(f"Error scraping {current_url}: {e}")

    if not queue:  # move to next level if queue is empty
        current_level += 1

df = pd.DataFrame(all_answers)
df.to_csv("answers.csv", index=False, encoding="utf-8-sig")
print(f"Saved {len(all_answers)} answers to answers.csv")

driver.quit()