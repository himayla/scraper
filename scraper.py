# A scraper for the articles of https://prisonerschronicle.net for the Nikki

from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import json

def scrape_article(article):
    """ Function extracts the title and text of page and returns it in a dictionary. """
    article.click()

    page = driver.page_source
    soup = BeautifulSoup(page, "html.parser")

    title = soup.find("article").find("h1", class_="heading").get_text()
    text_selector = soup.find("article").find("section", class_="content").find_all("p")

    text = ""
    for txt in text_selector:
        text += txt.get_text()

    return {title: text}

def write_out(results):
    """ Write out results to a json file. """
    with open("results.json", "w") as f:
        json.dump(results, f) 

if __name__ == "__main__":
    driver = webdriver.Chrome() # Change to browser of choice

    driver.get("https://prisonerschronicle.net") # Change to website of choice
    
    results = []

    try:
        while True:
            next_page = driver.find_element(By.CLASS_NAME, "next")
            if next_page == None: 
                write_out(results)
                driver.close()

            articles = driver.find_elements(By.CLASS_NAME, "btn__link")

            for article in articles:
                results.append(scrape_article(article))
                driver.back()
            
            next_page.click()
    
    except KeyboardInterrupt:
        write_out(results)
        driver.close()