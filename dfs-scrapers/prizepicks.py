#!/usr/bin/env python
# coding: utf-8

# In[ ]:

# Scrapes data from all sports offered on PrizePicks using the API and PyAutoGUI

from selenium import webdriver
import time
def scrape():
    deletedPlayers = []
    from selenium.common.exceptions import NoSuchElementException, TimeoutException, StaleElementReferenceException, NoSuchWindowException
    from smtplib import SMTPDataError
    import pandas as pd
    import pyautogui
    import time
    import win32api, win32con
    import pytesseract as tess
    tess.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    import cv2
    import re
    import numpy as np
    import pandas as pd
    import requests
    import pyperclip
    from pyperclip import PyperclipWindowsException
        
    def get_screen_image(save_path=None):
        screenshot = pyautogui.screenshot()
        # Convert the screenshot from RGB to BGR format
        screen_np = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
        if save_path:
            cv2.imwrite(save_path, screen_np)
        return screen_np

    def match_template(screen, template, threshold=0.8, min_distance=5):
        result = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
        locations = np.where(result >= threshold)
        matches = []
        for pt in zip(*locations[::-1]):
            x, y = pt
            too_close = False
            
            # Check if the new match is too close to existing matches
            for match in matches:
                match_x, match_y, _ = match
                distance = np.sqrt((x - match_x)**2 + (y - match_y)**2)
                if distance < min_distance:
                    too_close = True
                    break
            if not too_close:
                matches.append((x, y, result[y, x]))
        return matches

    
    def clean_text(text):
        # Remove any second decimal point and everything after it
        text = re.sub(r'(\d+\.\d).*', r'\1', text)
        
        # Handle common pattern mistakes
        text = re.sub(r'(\d+)\.\.+5(?:\.0)?', r'\1.5', text)
        text = re.sub(r'\.0$', '', text)
        
        # Remove trailing decimals and strip whitespace
        text = text.rstrip('.').strip()
        return text

    def preprocess_image(image, enhance=True):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        if enhance:
            adjusted = cv2.convertScaleAbs(gray, alpha=1.5, beta=20)  # Adjust contrast and brightness
            blurred = cv2.GaussianBlur(adjusted, (5, 5), 0)
            _, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            kernel = np.ones((2, 2), np.uint8)
            morph = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
            return morph
        else:
            return gray

    def preprocess_stat_image(image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

        # Use dilation to make text thicker
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
        dilated = cv2.dilate(thresh, kernel, iterations=1)

        return dilated

    def extract_text(image):
        custom_config = r'--oem 3 --psm 7 -c tessedit_char_whitelist=0123456789.'
        text = tess.image_to_string(image, config=custom_config)
        return text

    def extract_player_text(image):
        custom_config = r'--oem 3 --psm 6'
        text = tess.image_to_string(image, config=custom_config)
        return text

    def round_to_nearest_half(value):
        return round(value * 4) / 4
    
    def check_image_in_screenshot(screenshot_path, template_path, threshold=0.85):
        screenshot = cv2.imread(screenshot_path)
        template = cv2.imread(template_path)

        # Convert both images to grayscale
        screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
        template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)

        w, h = template_gray.shape[::-1]
        res = cv2.matchTemplate(screenshot_gray, template_gray, cv2.TM_CCOEFF_NORMED)
        loc = np.where(res >= threshold)

        if len(loc[0]) > 0:
            return True
        else:
            return False

    import pyautogui
    import time
    import pyperclip
    import json
    import pandas as pd
    from datetime import datetime, timedelta
    import unicodedata
    import win32api
    import win32con
    win32api.SetCursorPos((800, 700))
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    time.sleep(0.01)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)
    time.sleep(1)
    
    def remove_accents(input_str):
        # Removes accents from text
        nfkd_form = unicodedata.normalize('NFKD', input_str)
        return ''.join([c for c in nfkd_form if not unicodedata.combining(c)])

    link = 'https://api.prizepicks.com/projections?&per_page=250&single_stat=true&game_mode=pickem'

    # Open a new browser window and navigate to the link
    pyautogui.hotkey('esc')
    pyautogui.hotkey('ctrl', 'n')
    pyautogui.typewrite(link)
    pyautogui.hotkey('enter')

    # Wait for the page and data to load
    time.sleep(6)

    # Copy all data from the webpage
    pyautogui.hotkey('ctrl', 'a')
    pyautogui.hotkey('ctrl', 'c')

    data = pyperclip.paste()
    try:
        data = data.encode('latin1').decode('utf-8', errors='ignore')
    except UnicodeEncodeError as e:
        pass
    if not data.strip():
        print("No data copied to clipboard! Please ensure the page loaded correctly.")
    else:
        pass

    try:
        json_data = json.loads(data)
        # Extract projections and player information
        projections = json_data.get("data", [])
        player_info = json_data.get("included", [])

        if projections:
            player_stats = []            
            for projection in projections:
                attributes = projection.get("attributes", {})
                player_id = projection.get("relationships", {}).get("new_player", {}).get("data", {}).get("id", "Unknown Player ID")

                # Skip projections with adjusted odds (scorchers and goblins)
                if attributes.get("adjusted_odds") is not None:
                    continue

                # Extract opponent from the description
                opponent = attributes.get("description", "Unknown Opponent")

                # Find the player data corresponding to the player ID
                player_name = "Unknown Player"
                league_name = "Unknown League"
                team = "Unknown Team"
                for player in player_info:
                    if player.get("id") == player_id:
                        player_attributes = player.get("attributes", {})
                        player_name = player_attributes.get("display_name", "Unknown Player")
                        league_name = player_attributes.get("league", "Unknown League")
                        team = player_attributes.get("team", "Unknown Team")

                player_name = remove_accents(player_name)
                league_name = remove_accents(league_name)
                team = remove_accents(team)
                opponent = remove_accents(opponent)
                player_stats.append({
                    "player_id": player_id,
                    "Name": player_name,
                    "Team": team,
                    "Opponent": opponent,
                    "Stat": attributes.get("stat_display_name", "Unknown Stat"),
                    "Line": attributes.get("line_score", "Unknown Line Score"),
                    "game_start_time": attributes.get("start_time", "Unknown Game Start Time"),
                    "Sport": league_name
                })

            # Process timestamps
            for stat in player_stats:
                try:
                    clean_time = stat['game_start_time'][:-6]  # Strip timezone
                    parsed_time = datetime.strptime(clean_time, '%Y-%m-%dT%H:%M:%S')

                    # Adjust time from Eastern to Pacific (can change to correspond to your timezone)
                    parsed_time = parsed_time - timedelta(hours=3)                    
                    stat['Time'] = parsed_time.strftime('%I:%M%p').lower()
                    stat['Date'] = parsed_time.strftime('%Y-%m-%d')
                except ValueError as e:
                    print(f"Error parsing time for player {stat['Name']}: {e}")
                    stat['Date'] = 'Invalid Date'
                    stat['Time'] = 'Invalid Time'
            df = pd.DataFrame(player_stats)
            output_file = r"C:\\PrizePicks Scraper.csv" # Replace with desired csv location
            df[['Name', 'Team', 'Opponent', 'Stat', 'Line', 'Date', 'Time', 'Sport']].to_csv(output_file, index=False)
        else:
            print("No projections found in the data.")
            time.sleep(7)
            pyautogui.hotkey('ctrl', 'w')
            scrape()
    except json.JSONDecodeError as e:
        print(f"Failed to parse JSON: {e}")
        time.sleep(7)
        pyautogui.hotkey('ctrl', 'w')
        scrape()

    time.sleep(7)
    pyautogui.hotkey('ctrl', 'w')


driver = webdriver.Chrome()
driver.set_window_size(1920, 1080)
driver.set_window_position(-1000, 1100)
while True:
    # All sports will be collected from the PrizePicks site
    scrape()


# In[ ]:




