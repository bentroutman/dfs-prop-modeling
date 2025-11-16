#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# Scrapes data from Pinnacle sportsbook to use to create expected value estimations

from selenium import webdriver
def scrape():
    deletedPlayers = []
    from selenium.common.exceptions import NoSuchElementException, TimeoutException, StaleElementReferenceException, NoSuchWindowException
    from selenium.webdriver.common.by import By
    from smtplib import SMTPDataError
    import pandas as pd
    import pyautogui
    import time
    import win32api, win32con
    import pytesseract as tess
    tess.pytesseract.tesseract_cmd = r'C:\Tesseract-OCR\tesseract.exe' # Replace with tesseract location
    import cv2
    import re
    import numpy as np
    import pandas as pd
    import requests
    from unidecode import unidecode

    def scrapePinnacle(sport):
        names = []
        stats = []
        lines = []
        overPrices = []
        underPrices = []
        sportsbooks = []
        overPercentages = []
        underPercentages = []
        added_players = set()

        sportLinks = []
        if sport == "MLB":
            sportLinks = ['https://www.pinnacle.com/en/baseball/mlb/matchups/#period:0']
        elif sport == "NBA":
            sportLinks = ['https://www.pinnacle.com/en/basketball/nba/matchups/#period:0']
        elif sport == "NFL":
            sportLinks = ['https://www.pinnacle.com/en/football/nfl/matchups/#period:0']
        elif sport == "NHL":
            sportLinks = ['https://www.pinnacle.com/en/hockey/nhl/matchups/#period:0']
        elif sport == "Euroleague":
            sportLinks = ['https://www.pinnacle.com/en/basketball/europe-euroleague/matchups/#all']

        for sportLink in sportLinks:
            driver1.get(sportLink)
            time.sleep(3)
            elements = driver1.find_elements(By.XPATH, '//div[contains(@class, "row-u9F3b9WCM3") and contains(@class, "row-k9ktBvvTsJ")]//div[contains(@class, "metadata-ANkHTQFSEA")]//a')

            links = []
            for e in elements:
                propLink = e.get_attribute('href') + "#player-props"
                links.append(propLink)

            for link in links:
                driver1.get(link)
                time.sleep(2)
                if "player-props" in driver1.current_url:
                    try:
                        parent_elements = driver1.find_elements(By.XPATH, '//div[contains(@class, "marketGroup-")]')
                        for parent in parent_elements:
                            try:
                                title_element = parent.find_element(By.XPATH, './/span[contains(@class, "titleText-")]')
                                label_elements = parent.find_elements(By.XPATH, './/span[contains(@class, "label-GT4CkXEOFj")]')
                                price_elements = parent.find_elements(By.XPATH, './/span[contains(@class, "price-r5BU0ynJha")]')
                                if title_element and len(label_elements) >= 2 and len(price_elements) >= 2:
                                    title_text = title_element.text
                                    pattern = r"^([\w\s\.\'\-]+)\s\(([^)]+)\)(?:\s*\(must start\))?$"
                                    match = re.match(pattern, title_text)

                                    if match:
                                        name = unidecode(match.group(1).strip())  # Convert to English characters
                                        stat = match.group(2).strip()
                                        player_stat_id = (name, stat)

                                        if player_stat_id not in added_players:
                                            over_label_text = label_elements[0].text
                                            under_label_text = label_elements[1].text

                                            # Check for "Yes" or "No" and set to 0.5
                                            over_label_value = 0.5 if over_label_text == "Yes" else None
                                            if not over_label_value:
                                                over_label_match = re.search(r"\b(\d+(\.\d+)?)\b", over_label_text)
                                                over_label_value = float(over_label_match.group(1)) if over_label_match else None

                                            under_label_value = 0.5 if under_label_text == "No" else None
                                            if not under_label_value:
                                                under_label_match = re.search(r"\b(\d+(\.\d+)?)\b", under_label_text)
                                                under_label_value = float(under_label_match.group(1)) if under_label_match else None

                                            if over_label_value and under_label_value:
                                                line = over_label_value
                                                over_price = price_elements[0].text
                                                under_price = price_elements[1].text

                                                if line and over_price and under_price:
                                                    names.append(name)
                                                    stats.append(stat)
                                                    lines.append(line)
                                                    overPrices.append(over_price)
                                                    underPrices.append(under_price)
                                                    sportsbooks.append("Pinnacle")
                                                    added_players.add(player_stat_id)

                            except StaleElementReferenceException:
                                pass
                    except StaleElementReferenceException:
                        pass
                else:
                    pass
                    
        j = 0
        while j < len(names):
            vig = float(4 / (float(overPrices[j]) + float(underPrices[j])))
            currentPercentUn = float(float(overPrices[j]) * vig)
            currentPercentOv = float(float(underPrices[j]) * vig)
            overPercentages.append(currentPercentOv / 4)
            underPercentages.append(currentPercentUn / 4)
            j = j + 1                

        data = {
            'Name': names,
            'Stat': stats,
            'Sportsbook': sportsbooks,
            'Line': lines,
            'Over Price': overPrices,
            'Under Price': underPrices,
            '% Over': overPercentages,
            '% Under': underPercentages
        }
        
        df = pd.DataFrame(data)
        df.to_csv(f"C:\\Pinnacle Scraper - {sport}.csv", index=False) # Replace with desired file location

    # Can add more sports if desired
    sports = ['NBA', 'NFL', 'NBA']
    for sport in sports:
        scrapePinnacle(sport)

driver1 = webdriver.Chrome()
driver1.set_window_position(-1000, 1100)
while True:
    scrape()


# In[ ]:




