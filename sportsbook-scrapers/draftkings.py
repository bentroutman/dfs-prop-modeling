#!/usr/bin/env python
# coding: utf-8

# In[ ]:

# Scrapes data from selected sports from DraftKings to generate expected value (EV) estimates

from selenium import webdriver
def scrape():
    deletedPlayers = []
    from selenium.common.exceptions import NoSuchElementException, TimeoutException, StaleElementReferenceException, NoSuchWindowException
    from smtplib import SMTPDataError
    import pandas as pd
    import time
    import cv2
    import re
    import numpy as np
    import pandas as pd
    import requests

    def scrapeDraftKings(sport):
        from selenium import webdriver
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        from selenium.webdriver.chrome.options import Options
        from selenium.webdriver.chrome.service import Service as ChromeService
        from webdriver_manager.chrome import ChromeDriverManager
        import time
        import pandas as pd
        import re
        from selenium.webdriver.chrome.service import Service
        from selenium.common.exceptions import NoSuchElementException
        
        options = Options()
        options.add_experimental_option("detach", True)

        names = []
        stats = []
        sportsbooks = []
        lines = []
        percentOver = []
        percentUnder = []
        tempOverPrices = []
        tempUnderPrices = []
        overPrices = []
        underPrices = []

        sports = []
        sport1 = sport
        if sport == "MLB":
            sports = ['baseball/mlb']
            sport2 = sport
        elif sport == "OBBALL":
            sports = ['basketball/olympic-basketball-men', 'basketball/olympic-basketball-women']
        elif sport == "WNBA":
            sports = ['basketball/wnba']
        elif sport == "NFL":
            sports = ['football/nfl']
            sport2 = sport
        elif sport == "NHL":
            sports = ['hockey/nhl']
            sport2 = sport
        elif sport == "NBA":
            sports = ['basketball/nba']
            sport2 = sport
        elif sport == "CBB":
            sports = ['basketball/nccab']

        for sport in sports:
            wait = WebDriverWait(driver1, 10)
            time.sleep(0.5)
            if sport == 'baseball/mlb':
                statLinks = ['?category=batter-props&subcategory=hits', '?category=batter-props&subcategory=hits-%2B-runs-%2B-rbis', '?category=batter-props&subcategory=total-bases', '?category=batter-props&subcategory=rbis', '?category=batter-props&subcategory=runs-scored', '?category=batter-props&subcategory=stolen-bases', '?category=batter-props&subcategory=singles', '?category=batter-props&subcategory=doubles', '?category=batter-props&subcategory=walks', '?category=pitcher-props&subcategory=strikeouts-thrown', '?category=pitcher-props&subcategory=outs-recorded', '?category=pitcher-props&subcategory=hits-allowed', '?category=pitcher-props&subcategory=earned-runs-allowed', '?category=pitcher-props&subcategory=walks-allowed']
                tempStats = ['Hits', 'Hits + Runs + RBIs', 'Total Bases', 'RBIs', 'Runs Scored', 'Stolen Bases', 'Singles', 'Doubles', 'Walks', 'Strikeouts Thrown', 'Outs Recorded', 'Hits Allowed', 'Earned Runs Allowed', 'Walks Allowed']
            elif sport == 'basketball/olympic-basketball-men':
                statLinks = ['?category=player-points&subcategory=points', '?category=player-threes&subcategory=threes', '?category=player-combos&subcategory=pts-%2B-reb-%2B-ast', '?category=player-rebounds&subcategory=rebounds', '?category=player-assists&subcategory=assists', '?category=player-defense&subcategory=blocks', '?category=player-steals&subcategory=steals']
                tempStats = ['Points', 'Threes', 'Pts + Reb + Ast', 'Rebounds', 'Assists', 'Blocks', 'Steals']
            elif sport == 'basketball/olympic-basketball-women':
                statLinks = ['?category=player-points&subcategory=points', '?category=player-rebounds&subcategory=rebounds', '?category=player-assists&subcategory=assists']
                tempStats = ['Points', 'Rebounds', 'Assists']
            elif sport == 'basketball/wnba':
                statLinks = ['?category=player-points&subcategory=points', '?category=player-threes&subcategory=threes', '?category=player-combos&subcategory=pts-%2B-reb-%2B-ast', '?category=player-rebounds&subcategory=rebounds', '?category=player-assists&subcategory=assists', '?category=player-defense&subcategory=blocks', '?category=player-steals&subcategory=steals']
                tempStats = ['Points', 'Threes', 'Pts + Reb + Ast', 'Rebounds', 'Assists', 'Blocks', 'Steals']
            elif sport == 'football/nfl':
                statLinks = ['?category=passing-props-&subcategory=pass-yards', '?category=passing-props-&subcategory=pass-tds', '?category=passing-props-&subcategory=pass-attempts', '?category=passing-props-&subcategory=completions', '?category=passing-props-&subcategory=longest-completion', '?category=passing-props-&subcategory=interceptions', '?category=passing-props-&subcategory=pass-%2B-rush-yards', '?category=rushing-props&subcategory=rush-yards', '?category=rushing-props&subcategory=rush-%2B-rec-yards', '?category=rushing-props&subcategory=rush-attempts', '?category=rushing-props&subcategory=longest-rush', '?category=receiving-props&subcategory=receptions', '?category=receiving-props&subcategory=rec-yards', '?category=receiving-props&subcategory=longest-reception', '?category=d%2Fst-props&subcategory=sacks', '?category=d%2Fst-props&subcategory=tackles-%2B-ast', '?category=d%2Fst-props&subcategory=solo-tackles', '?category=d%2Fst-props&subcategory=assists', '?category=d%2Fst-props&subcategory=fg-made', '?category=d%2Fst-props&subcategory=kicking-pts', '?category=d%2Fst-props&subcategory=pat-made']
                tempStats = ['Pass Yards', 'Pass TDs', 'Pass Attempts', 'Completions', 'Longest Completion', 'Interceptions', 'Pass + Rush Yards', 'Rush Yards', 'Rush + Rec Yards', 'Rush Attempts', 'Longest Rush', 'Receptions', 'Rec Yards', 'Longest Reception', 'Sacks', 'Tacles + Ast', 'Solo Tackles', 'Assists', 'FG Made', 'Kicking Pts', 'PAT Made']
            elif sport == 'hockey/nhl':
                statLinks = ['?category=shots-on-goal&subcategory=shots-on-goal', '?category=points&subcategory=points', '?category=blocks&subcategory=blocks', '?category=goalie-saves&subcategory=saves', '?category=player-assists&subcategory=assists']
                tempStats = ['Shots On Goal', 'Points', 'Blocks', 'Goalie Saves', 'Assists']
            elif sport == 'basketball/nba':
                statLinks = ['?category=player-points&subcategory=points', '?category=player-threes&subcategory=threes', '?category=player-combos&subcategory=pts-%2B-reb-%2B-ast', '?category=player-rebounds&subcategory=rebounds', '?category=player-assists&subcategory=assists', '?category=player-defense&subcategory=blocks', '?category=player-steals&subcategory=steals', '?category=player-combos&subcategory=pts-%2B-reb', '?category=player-combos&subcategory=pts-%2B-ast', '?category=player-combos&subcategory=ast-%2B-reb', '?category=player-defense&subcategory=steals-%2B-blocks', '?category=player-defense&subcategory=turnovers']
                tempStats = ['Points', 'Threes', 'Pts + Reb + Ast', 'Rebounds', 'Assists', 'Blocks', 'Steals', 'Pts + Reb', 'Pts + Ast', "Ast + Reb", 'Steals + Blocks', 'Turnovers']
            for link in statLinks:
                try:
                    indexes = []
                    index = 0
                    driver1.get('https://sportsbook.draftkings.com/leagues/' + sport + link + '-o%2Fu')
                    time.sleep(1)
                    if link not in driver1.current_url:
                        driver1.get('https://sportsbook.draftkings.com/leagues/' + sport + link)
                        time.sleep(1)
                    wrappers = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'sportsbook-table')))
                    times = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'sportsbook-event-accordion__date')))
                    if len(wrappers) != len(times):
                        wrappers = wrappers[-len(times):]
                    for wrapper in wrappers:
                        if times[wrappers.index(wrapper)].text:
                            indexes.append(wrappers.index(wrapper))
                    for r in indexes:
                        if "PLAYER" in wrapper.find_element(By.TAG_NAME, "span").text:
                            tempNames = WebDriverWait(wrappers[r], 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'sportsbook-row-name')))
                            tempLines = WebDriverWait(wrappers[r], 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'sportsbook-outcome-cell__line')))
                            tempPrices = WebDriverWait(wrappers[r], 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'sportsbook-odds.american.default-color')))
                            if len(tempPrices) % 2 == 0 and len(tempLines) % 2 == 0:
                                for tempName in tempNames:
                                    names.append(tempName.text)
                                    stats.append(tempStats[statLinks.index(link)])

                                j = 0            
                                while j < len(tempLines):
                                    if j % 2 == 0:
                                        lines.append(tempLines[j].text)
                                    j = j + 1

                                l = 0   

                                while l < len(tempPrices):
                                    if l % 2 == 0:
                                        tempOverPrices.append(tempPrices[l].text)
                                    else:
                                        tempUnderPrices.append(tempPrices[l].text)
                                    l = l + 1
                except (TimeoutException, NoSuchElementException, StaleElementReferenceException):
                    continue

        try:
            for over_price in tempOverPrices:
                if '+' not in over_price:
                    if int(over_price[1:]) == 0:
                        decimalPrice = 100 / 1000 + 1
                    else:
                        decimalPrice = 100 / int(over_price[-3:]) + 1
                    overPrices.append(decimalPrice)
                else:
                    if int(over_price[1:]) == 0:
                        decimalPrice = 1000 / 100 + 1
                    else:
                        decimalPrice = int(over_price[-3:]) / 100 + 1
                    overPrices.append(decimalPrice)
            for under_price in tempUnderPrices:
                if '+' not in under_price:
                    decimalPrice = 100 / int(under_price[1:]) + 1
                    underPrices.append(decimalPrice)
                else:
                    decimalPrice = int(under_price[1:]) / 100 + 1
                    underPrices.append(decimalPrice)
        except ZeroDivisionError:
            pass

        n = 0
        while n < len(names):
            try:
                vig = float(4 / (float(overPrices[n]) + float(underPrices[n])))
                currentPercentUn = float(float(overPrices[n]) * vig)
                currentPercentOv = float(float(underPrices[n]) * vig)
                percentOver.append(currentPercentOv / 4)
                percentUnder.append(currentPercentUn / 4)
                n = n + 1
            except IndexError:
                n = n + 1

        for name in names:
            sportsbooks.append("DraftKings")

        data = {'Name': names, 'Stat': stats, 'Sportsbook': sportsbooks, 'Line': lines, 'Over Price': overPrices, 'Under Price': underPrices, '% Over': percentOver, '% Under': percentUnder}
        try:
            df = pd.DataFrame(data)
            df.to_csv(f"DraftKings Scraper - {sport2}.csv", index=False) # Replace with desired csv location
        except ValueError:
            pass

    # Can include more sports if desired
    sports = ['NFL', 'NHL', 'MLB', 'NBA', 'WNBA']
    for sport in sports:
        scrapeDraftKings(sport)
    time.sleep(1200)

driver1 = webdriver.Chrome()
driver1.set_window_position(-1000, 1100)
driver1.set_window_size(1920, 1080)
while True:
    scrape()


# In[ ]:




