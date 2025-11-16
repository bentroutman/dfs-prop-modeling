#!/usr/bin/env python
# coding: utf-8

# In[ ]:

# Scrapes all desired lines from Underdog's site using Selenium and exports as a csv file

from selenium import webdriver
def scrape():
    deletedPlayers = []
    from selenium.common.exceptions import NoSuchElementException, TimeoutException, StaleElementReferenceException, NoSuchWindowException
    import pandas as pd
    import pyautogui
    import time
    import win32api, win32con
    import pytesseract as tess
    tess.pytesseract.tesseract_cmd = r'C:\Tesseract-OCR\tesseract.exe' # Replace with actual tesseract location
    import cv2
    import re
    import numpy as np
    import pandas as pd
    import requests

    def scrapeUnderdog(sport):
        from selenium import webdriver
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        from selenium.webdriver.chrome.options import Options
        from selenium.common.exceptions import NoSuchElementException, WebDriverException, TimeoutException, ElementClickInterceptedException
        from selenium.webdriver.common.action_chains import ActionChains
        import time
        import pandas as pd
        from webdriver_manager.chrome import ChromeDriverManager
        from selenium.webdriver.chrome.service import Service


        email = "enter Underdog email"
        password = "enter Underdog password"

        sports = []
        if sport == "SOCCER":
            sports = ['/soccer', '/fifa', '/wsoccer']
        elif sport == "ESPORTS":
            sports = ['/esports', '/lol', '/cs']
        elif sport == "MLB":
            sports = ['/mlb']
            sport2 = sport
        elif sport == "WNBA":
            sports = ['/wnba']
        elif sport == "OBBALL":
            sports = ['/olympic_basketball']
        elif sport == "Euroleague":
            sports = ['/basketball']
            sport2 = 'Euroleague'
        elif sport == "GOLF":
            sports = ['/pga']
        elif sport == "NFL":
            sports = ['/nfl']
            sport2 = sport
        elif sport == "CFB":
            sports = ['/cfb']
        elif sport == "NHL":
            sports = ['/nhl']
            sport2 = sport
        elif sport == "NBA":
            sports = ['/nba']
            sport2 = sport
        elif sport == "CBB":
            sports = ['/cbb']

        
        if len(sports) >= 1:
            links = ['https://underdogfantasy.com/pick-em/higher-lower/pre-game']
            for link in links:
                try:
                    driver1.get(link)
                except TimeoutException:
                    pass
                except WebDriverException:
                    pass
                except UnboundLocalError:
                    pass

                # Log in
                try:
                    wait = WebDriverWait(driver1, 15)
                except UnboundLocalError:
                    pass
                time.sleep(2)
                try:
                    if "login" in driver1.current_url:
                        try:
                            field = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'styles__field__OeiFa')))
                            field.send_keys(email)
                        except TimeoutException:
                            return

                        field = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/div/div[2]/div[2]/div[1]/form/div[2]/label/div[2]/input')))
                        field.send_keys(password)

                        button1 = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]/div/div/div[2]/div[2]/div[1]/form/button')))
                        button1.click()

                    try:
                        wait.until(EC.url_to_be('https://underdogfantasy.com/pick-em/higher-lower/all/home'))
                    except TimeoutException:
                        return
                except UnboundLocalError:
                    pass

            names = []
            times = []
            stats = []
            lines = []
            sportsList = []
            oversOrUnders = []
            payouts = []

            try:
                for sport in sports:
                    featNames = []
                    featLines = []
                    featStats = []
                    m = 0
                    time.sleep(0.5)
                    featureds = driver1.find_elements(By.CLASS_NAME, 'common-styles__infoSection__xZKpx.styles__infoSection__kLv_4')
                    for featured in featureds:
                        nameLines = featured.find_elements(By.CLASS_NAME, 'common-styles__header__sqrtO.styles__header__t36aQ')
                        if len(nameLines) == 2:
                            name = nameLines[0].text
                            line = nameLines[1].text
                            featNames.append(name)
                            featLines.append(line)
                        matchupStats = featured.find_elements(By.CLASS_NAME, 'common-styles__text__uoKPL.styles__text__HG_4q')
                        if len(matchupStats) == 2:
                            stat = matchupStats[1].text
                            featStats.append(stat)
                        if m % 2 == 1:
                            try:
                                button = driver1.find_element(By.XPATH, '//*[@id="root"]/div/div[1]/div[2]/div[2]/div/div[1]/div/button[2]')
                                button.click()
                            except NoSuchElementException:
                                pass
                            except ElementClickInterceptedException:
                                pass
                            time.sleep(0.5)
                        m += 1
                    try:
                        driver1.get('https://underdogfantasy.com/pick-em/higher-lower/pre-game' + sport)
                        time.sleep(7)
                        if sport in driver1.current_url:
                            # Click on "More picks" buttons
                            time.sleep(0.5)
                            buttons = driver1.find_elements(By.CLASS_NAME, "styles__toggleSpan__PUBDQ")
                            clicked_buttons = set()
                            actions = ActionChains(driver1)
                            for button3 in buttons:
                                if "More picks" in button3.text and button3 not in clicked_buttons:
                                    try:
                                        actions.move_to_element(button3).perform()
                                        time.sleep(0.1)
                                        button3.click()
                                        clicked_buttons.add(button3)
                                    except ElementClickInterceptedException:
                                        driver1.execute_script("arguments[0].scrollIntoView(true);", button3)
                                        time.sleep(0.1)
                                        try:
                                            button3.click()
                                            clicked_buttons.add(button3)
                                        except ElementClickInterceptedException:
                                            driver1.execute_script("arguments[0].click();", button3)
                                            clicked_buttons.add(button3)

                            time.sleep(0.1)
                            non_featureds = []
                            if "/golf" in sport or "/pga" in sport or "/olympic_golf" in sport:
                                non_featureds = driver1.find_elements(By.CLASS_NAME, 'styles__playerListCol__boy4v')
                            else:
                                non_featureds = driver1.find_elements(By.CLASS_NAME, 'styles__accordion__bInXb')
                            for non_featured in non_featureds:
                                cells = non_featured.find_elements(By.CLASS_NAME, "styles__overUnderCell__KgzNn")
                                for cell in cells:
                                    try:
                                        name_element = cell.find_element(By.CLASS_NAME, 'styles__playerName__Coe_G')
                                        name = name_element.text
                                        name = unidecode(name)
                                        matchup_element = cell.find_element(By.CLASS_NAME, 'styles__matchInfoText__kQU88')
                                        matchup = matchup_element.text
                                        pattern = re.compile(r'(\d{1,2}:\d{2}(?:AM|PM|am|pm))')
                                        match = pattern.search(matchup)
                                        if match:
                                            tempTime = match.group()
                                        else:
                                            continue
                                    except NoSuchElementException:
                                        continue
                                    cells2 = cell.find_elements(By.CLASS_NAME, "styles__overUnderListCell__tbRod")
                                    for cell2 in cells2:
                                        text_content = cell2.text
                                        if "Higher" in text_content and "Lower" in text_content:
                                            cells3 = cell2.find_elements(By.CLASS_NAME, "styles__statLine__K1NYh")
                                            for cell3 in cells3:
                                                prop_elements = cell3.find_elements(By.XPATH, "./div")
                                                if len(prop_elements) == 2:
                                                    prop_line = prop_elements[0].text.strip()
                                                    stat_line = prop_elements[1].text.strip()
                                                    match = re.search(r'\d+(\.\d+)?', prop_line)
                                                    if match:
                                                        split_index = match.end()
                                                        line = prop_line[:split_index].strip()
                                                        stat = prop_line[split_index:].strip() + ' ' + stat_line

                                                        if name:
                                                            names.append(name)
                                                            times.append(tempTime)
                                                            lines.append(line)
                                                            stats.append(stat)
                                                            sportsList.append(sport)
                                                            names.append(name)
                                                            times.append(tempTime)
                                                            lines.append(line)
                                                            stats.append(stat)
                                                            sportsList.append(sport)
                                            cells4 = cell2.find_elements(By.CLASS_NAME, "styles__pickEmButton__OS_iW")
                                            for cell4 in cells4:
                                                if "Higher" in cell4.text:
                                                    try:
                                                        element = cell4.find_element(By.CLASS_NAME, "styles__payoutMultiplierWrapper__sfh5n")
                                                        payout = element.text
                                                    except NoSuchElementException:
                                                        payout = "1x"
                                                    payouts.append(payout)
                                                    oversOrUnders.append("Higher")
                                                elif "Lower" in cell4.text:
                                                    try:
                                                        element = cell4.find_element(By.CLASS_NAME, "styles__payoutMultiplierWrapper__sfh5n")
                                                        payout = element.text
                                                    except NoSuchElementException:
                                                        payout = "1x"
                                                    payouts.append(payout)
                                                    oversOrUnders.append("Lower")
                                        elif "Higher" in text_content:
                                            try:
                                                element = cell2.find_element(By.CLASS_NAME, "styles__payoutMultiplierWrapper__sfh5n")
                                                payout = element.text
                                            except NoSuchElementException:
                                                payout = "1x"
                                            cells3 = cell2.find_elements(By.CLASS_NAME, "styles__statLine__K1NYh")
                                            for cell3 in cells3:
                                                prop_elements = cell3.find_elements(By.XPATH, "./div")
                                                if len(prop_elements) == 2:
                                                    prop_line = prop_elements[0].text.strip()
                                                    stat_line = prop_elements[1].text.strip()

                                                    match = re.search(r'\d+(\.\d+)?(?=\s+[a-zA-Z])', prop_line)
                                                    if match:
                                                        split_index = match.end()
                                                        line = prop_line[:split_index].strip()
                                                        stat = prop_line[split_index:].strip() + ' ' + stat_line

                                                        if name:
                                                            names.append(name)
                                                            times.append(tempTime)
                                                            lines.append(line)
                                                            stats.append(stat)
                                                            sportsList.append(sport)
                                                            oversOrUnders.append("Higher")
                                                            payouts.append(payout)
                                        elif "Lower" in text_content:
                                            try:
                                                element = cell2.find_element(By.CLASS_NAME, "styles__payoutMultiplierWrapper__sfh5n")
                                                payout = element.text
                                            except NoSuchElementException:
                                                payout = "1x"
                                            cells3 = cell2.find_elements(By.CLASS_NAME, "styles__statLine__K1NYh")
                                            for cell3 in cells3:
                                                prop_elements = cell3.find_elements(By.XPATH, "./div")
                                                if len(prop_elements) == 2:
                                                    prop_line = prop_elements[0].text.strip()
                                                    stat_line = prop_elements[1].text.strip()

                                                    match = re.search(r'\d+(\.\d+)?(?=\s+[a-zA-Z])', prop_line)
                                                    if match:
                                                        split_index = match.end()
                                                        line = prop_line[:split_index].strip()
                                                        stat = prop_line[split_index:].strip() + ' ' + stat_line

                                                        if name:
                                                            names.append(name)
                                                            times.append(tempTime)
                                                            lines.append(line)
                                                            stats.append(stat)
                                                            sportsList.append(sport)
                                                            oversOrUnders.append("Lower")
                                                            payouts.append(payout)
                    except StaleElementReferenceException:
                        continue

                newNames, newTimes, newLines, newStats, newSportsList, newOversOrUnders, newPayouts = [], [], [], [], [], [], []

                def create_temp_name(full_name):
                    try:
                        first_name, last_name = full_name.split()
                        temp_name = f"{first_name[0]}. {last_name}"
                        return temp_name
                    except ValueError:
                        return full_name

                temp_names = [create_temp_name(name) for name in names]
                feat_dict = {name: (featStats[i], featLines[i]) for i, name in enumerate(featNames)}

                for l in range(len(temp_names)):
                    matched = False
                    for k in range(len(featNames)):
                        try:
                            if featNames[k] == temp_names[l] and featStats[k] == stats[l][:-1] and float(featLines[k]) == float(lines[l]):
                                matched = True
                                break
                        except ValueError:
                            pass
                    if not matched:
                        if "LoL: " in names[l] and sportsList[l] == "/esports":
                            new_name = names[l].replace("LoL: ", "")
                            new_sport = "/lol"
                        elif "Dota: " in names[l] and sportsList[l] == "/esports":
                            new_name = names[l].replace("Dota: ", "")
                            new_sport = "/dota"
                        elif "CS: " in names[l] and sportsList[l] == "/esports":
                            new_name = names[l].replace("CS: ", "")
                            new_sport = "/cs2"
                        elif "Val: " in names[l] and sportsList[l] == "/esports":
                            new_name = names[l].replace("Val: ", "")
                            new_sport = "/val"
                        elif "CoD: " in names[l] and sportsList[l] == "/esports":
                            new_name = names[l].replace("CoD: ", "")
                            new_sport = "/cod"
                        else:
                            new_name = names[l]
                            new_sport = sportsList[l]
                        newNames.append(new_name)
                        newTimes.append(times[l])
                        newLines.append(lines[l])
                        newStats.append(stats[l][:-1])
                        newSportsList.append(new_sport)
                        try:
                            newOversOrUnders.append(oversOrUnders[l])
                        except IndexError:
                            newOversOrUnders.append("")
                        try:
                            newPayouts.append(payouts[l])
                        except IndexError:
                            pass


                data = {'Name': newNames, 'Time': newTimes, 'Line': newLines, 'Stat': newStats, 'Sport': newSportsList, 'Higher/Lower': newOversOrUnders, 'Payout': newPayouts}
                if len(names) == len(stats) == len(lines):
                    df = pd.DataFrame(data)
                    df.to_csv(f"C:\\Underdog Scraper - {sport2}.csv", index=False) # Replace with desried csv location
                else:
                    print("No data collected or incomplete data, not creating CSV.")

            except UnboundLocalError:
                pass

    # Works for additional sports, but I chose to limit it to sports with semi-regular opportunities identified by the model
    sports = ['NBA', 'NFL', 'NBA', 'NHL', 'NBA', 'SOCCER', 'ESPORTS']
    for sport in sports:
        scrapeUnderdog(sport)

driver1 = webdriver.Chrome()
driver1.set_window_position(-1000, 1100)
driver1.set_window_size(1920, 1080)
while True:
    scrape()

