import json
import logging
import os
import subprocess
import sys
from logging import getLogger
import time
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright
import random

'''
This script is used to scrape the news from fool website and check if the value of the recommendations 
'''
 
logger = getLogger("fool_check.py")
logging.basicConfig(
    stream=sys.stdout,  # uncomment this line to redirect output to console
    format="%(message)s",
    level=logging.DEBUG,
)
url_pre ="https://www.fool.ca/recent-headlines/page/"

load_dotenv()
 
def main():
    with sync_playwright() as playwright:
        playwright_version = (
            str(subprocess.getoutput("playwright --version")).strip().split(" ")[1]
        )

        logger.info(f"Initiating ")
        browser = playwright.chromium.launch(headless=False)
        page = browser.new_page()
        for i in range(1, 1001):
            for_sleep = random.random()/2
            get_headlines(page, i)
            logger.info(f"Page {i} done")
            time.sleep(for_sleep)
        # get_headlines(page, page_numbmer=1)

def get_headlines(page, page_numbmer=1):
    try:            

        url = url_pre + str(page_numbmer)
        page.goto(url)
        hide_pop1(page)
        hide_pop2(page)
        main_element = page.query_selector('main')
        if main_element:
            lines = []
            links = main_element.query_selector_all('a')
            link_details = []
            for link in links:
                linkclass = link.get_attribute('class')
                if linkclass and 'page-numbers' in linkclass:
                    continue
                title = link.query_selector('h3')
                time = link.query_selector('time')
                if title and time:
                    link_details.append((title.text_content(), time.text_content(), link.get_attribute('href')))
                else:
                        #link_details.append((None, None, link.get_attribute('href')))
                    logger.error(f"Title or time not found for link {link.get_attribute('href')}")
                #link_details = [(link.query_selector('h3').text_content(), link.query_selector('time').text_content(), link.get_attribute('href')) 
                #        for link in links if link.get_attribute('href')] # (title, time, url) for each link
            for link in link_details:
                lines.append("\t".join(link))
            
            output_file = f'data/fool_page{page_numbmer}.csv'
                
            with open(output_file, 'w') as f:
                f.write("\n".join(lines))
    except Exception as ex:
        logger.error(str(ex))

def hide_pop2(page):
    if (page.is_visible(".modal-content")):
        page.get_by_text("x", exact=True).click()

def hide_pop1(page):
    if (page.is_visible("#onetrust-banner-sdk")):
        page.get_by_text("Got it").click()
 
 
if __name__ == "__main__":
    main()




