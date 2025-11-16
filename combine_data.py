#!/usr/bin/env python
# coding: utf-8

# In[ ]:

# Combines the data from DFS sites and sportsbooks into csvs that estimate expected value (EV)
# Sends a discord notification to the user when profitable opportunities are available
# Run this after running the prizepicks, underdog, pinnacle, and draftkings scrapers first

from selenium import webdriver
def scrape():
    deletedPlayers = []
    from selenium.common.exceptions import NoSuchElementException, TimeoutException, StaleElementReferenceException, NoSuchWindowException
    from smtplib import SMTPDataError
    import pandas as pd
    import pyautogui
    import time
    import cv2
    import re
    import numpy as np
    import pandas as pd
    import requests
    
    def combine(dfs, sport, sportsbook, dfsCSV, sportsbookCSV, fileLoc, fileName):
        dfs_df = pd.read_csv(dfsCSV)
        sportsbook_df = pd.read_csv(sportsbookCSV)
            
        sportsbook_names = sportsbook_df["Name"].values.tolist()
        sportsbook_oldLines = sportsbook_df["Line"].values.tolist()
        sportsbook_oldStats = sportsbook_df["Stat"].values.tolist()
        try:
            dfs_df['Time'] = dfs_df['Time'].str.lower()
        except AttributeError:
            pass
        dfs_names = dfs_df["Name"].values.tolist()
        dfs_times = dfs_df["Time"].values.tolist()
        dfs_oldLines = dfs_df["Line"].values.tolist()
        dfs_oldStats = dfs_df["Stat"].values.tolist()
        dfs_sports = dfs_df["Sport"].values.tolist()
        
            
        try:
            dfs_higherOrLowers = dfs_df["Higher/Lower"].values.tolist()
            dfs_payouts = dfs_df["Payout"].values.tolist()
        except KeyError:
            pass
        
        try:
            sportsbook_higherOrLowers = sportsbook_df["Higher/Lower"].values.tolist()
            sportsbook_payouts = sportsbook_df["Payout"].values.tolist()
        except KeyError:
            pass
        
        try:
            sportsbook_df['Time'] = sportsbook_df['Time'].str.lower()
            sportsbook_times = sportsbook_df['Time'].values.tolist()
        except KeyError:
            sportsbook_times = []
            for name in sportsbook_names:
                sportsbook_times.append("")
        except AttributeError:
            sportsbook_times = []
            for name in sportsbook_names:
                sportsbook_times.append("")

        dfs_stats = []
        sportsbook_newStats = []
        names = []
        stats = []
        sportsbooks = []
        sportsbook_lines = []
        dfs_lines = []
        overPrices = []
        underPrices = []
        overPercentages = []
        underPercentages = []
        discrepancies = []
        payouts = []
        higherOrLowers = []
        evs = []
        times = []
        
        names1 = []
        stats1 = []
        sportsbooks1 = []
        sportsbook_lines1 = []
        dfs_lines1 = []
        overPrices1 = []
        underPrices1 = []
        overPercentages1 = []
        underPercentages1 = []
        discrepancies1 = []
        payouts1 = []
        higherOrLowers1 = []
        evs1 = []
        times1 = []
        
        names2 = []
        stats2 = []
        sportsbooks2 = []
        sportsbook_lines2 = []
        dfs_lines2 = []
        overPrices2 = []
        underPrices2 = []
        overPercentages2 = []
        underPercentages2 = []
        discrepancies2 = []
        payouts2 = []
        higherOrLowers2 = []
        evs2 = []
        times2 = []

        for stat in dfs_oldStats:
            if "Kills in Maps 1+2+3" in stat:
                dfs_stats.append("Kills on Maps 1+2+3")
            elif "Kills on Map 1+2" in stat:
                dfs_stats.append("Kills on Maps 1+2")
            elif "Kills in Maps 1+2" in stat:
                dfs_stats.append("Kills on Maps 1+2")
            elif stat == "Kills on Game 1+2+3":
                dfs_stats.append("Kills on Maps 1+2+3")
            elif "Kills on Game 1" in stat:
                dfs_stats.append("Kills on Map 1")
            elif "Kills on Game 2" in stat:
                dfs_stats.append("Kills on Map 2")
            elif "Kills on Game 3" in stat:
                dfs_stats.append("Kills on Map 3")
            else:
                dfs_stats.append(stat)
        
        if "Underdog" in dfs:
            for stat in sportsbook_oldStats:
                if "MAP 1 Kills" in stat:
                    sportsbook_newStats.append("Kills on Map 1")
                elif "MAP 2 Kills" in stat:
                    sportsbook_newStats.append("Kills on Map 2")
                elif "MAP 3 Kills" in stat:
                    sportsbook_newStats.append("Kills on Map 3")
                elif "Total Strikeouts" in stat:
                    sportsbook_newStats.append("Strikeouts")
                elif "Pitcher Strikeouts" in stat:
                    sportsbook_newStats.append("Strikeouts")
                elif "Strikeouts Thrown" in stat:
                    sportsbook_newStats.append("Strikeouts")
                elif "Threes" in stat:
                    sportsbook_newStats.append("3-Pointers Made")
                elif "Hits+Runs+RBIs" in stat:
                    sportsbook_newStats.append("Hits + Runs + RBIs")
                elif "Walks" in stat and "Walks Allowed" not in stat:
                    sportsbook_newStats.append("Batter Walks")
                elif "Hitter Strikeouts" in stat:
                    sportsbook_newStats.append("Batter Strikeouts")
                elif "MAPS 1-2 Kills" in stat and "MAPS 1-3 Kills" not in stat:
                    sportsbook_newStats.append("Kills on Maps 1+2")
                elif "MAPS 1-3 Kills" in stat:
                    sportsbook_newStats.append("Kills on Maps 1+2+3")
                elif "MAPS 1-3 Headshots" in stat:
                    sportsbook_newStats.append("Headshots on Maps 1+2+3")
                elif "MAPS 1-2 Headshots" in stat:
                    sportsbook_newStats.append("Headshots on Maps 1+2")
                elif "MAP 1 Headshots" in stat:
                    sportsbook_newStats.append("Headshots on Map 1")
                elif "MAP 1 Assists" in stat:
                    sportsbook_newStats.append("Assists on Map 1")
                elif "MAPS 1-2 Assists" in stat and "MAPS 1-3 Assists" not in stat:
                    sportsbook_newStats.append("Assists on Maps 1+2")
                elif "MAPS 1-3 Assists" in stat:
                    sportsbook_newStats.append("Assists on Maps 1+2+3")
                elif "Shots On Target" in stat and sport == "SOCCER":
                    sportsbook_newStats.append("Shots on Target")
                elif "Shots" in stat and "Assisted" not in stat and sport == "SOCCER":
                    sportsbook_newStats.append("Shots Attempted")
                elif "3-PT Made" in stat:
                    sportsbook_newStats.append("3-Pointers Made")
                elif "Goalie Saves" in stat:
                    sportsbook_newStats.append("Saves")
                elif "Birdies Or Better" in stat:
                    sportsbook_newStats.append("Birdies or Better")
                elif "Goals (Handball)" in stat:
                    sportsbook_newStats.append("Goals")
                elif "Pts+Rebs+Asts" in stat:
                    sportsbook_newStats.append("Pts + Rebs + Asts")
                elif "Pts+Rebs" in stat:
                    sportsbook_newStats.append("Points + Rebounds")
                elif "Rebs+Asts" in stat:
                    sportsbook_newStats.append("Rebounds + Assists")
                elif "Pts+Asts" in stat:
                    sportsbook_newStats.append("Points + Assists")
                elif "Blocked Shots" in stat:
                    sportsbook_newStats.append("Blocks")
                elif stat == "Pass Yards":
                    sportsbook_newStats.append("Passing Yards")
                elif stat == "Rush Yards":
                    sportsbook_newStats.append("Rushing Yards")
                elif stat == "Rush+Rec TDs":
                    sportsbook_newStats.append("Rush + Rec TDs")
                elif stat == "Pass TDs":
                    sportsbook_newStats.append("Passing TDs")
                elif stat == "Rush+Rec Yards":
                    sportsbook_newStats.append("Rush + Rec Yards")
                elif stat == "Pass Attempts":
                    sportsbook_newStats.append("Passing Attempts")
                elif stat == "Pass Completions":
                    sportsbook_newStats.append("Completions")
                elif stat == "INT":
                    sportsbook_newStats.append("Interceptions")
                elif stat == "Pass+Rush Yds":
                    sportsbook_newStats.append("Pass + Rush Yards")
                elif stat == "Rush Attempts":
                    sportsbook_newStats.append("Rushing Attempts")
                elif stat == "Rec Targets":
                    sportsbook_newStats.append("Targets")
                elif stat == "Rec Yards":
                    sportsbook_newStats.append("Receiving Yards")
                elif stat == "Tackles + Ast":
                    sportsbook_newStats.append("Tackles + Assists")
                elif stat == "Kicking Pts":
                    sportsbook_newStats.append("Kicking Points")
                elif stat == "PAT Made":
                    sportsbook_newStats.append("XP Made")
                elif stat == "TD Passes":
                    sportsbook_newStats.append("Passing TDs")
                elif stat == "1st TD Scorer":
                    sportsbook_newStats.append("First TD Scorer")
                elif stat == "Anytime TD":
                    sportsbook_newStats.append("Rush + Rec TDs")
                elif stat == "Goalie Saves" and sport == "NHL":
                    sportsbook_newStats.append("Saves")
                elif stat == "Shots On Goal" and sport == "NHL":
                    sportsbook_newStats.append("Shots")
                elif stat == "Blocks" and sport == "NHL":
                    sportsbook_newStats.append("Blocked Shots")
                elif stat == "ShotsOnGoal":
                    sportsbook_newStats.append("Shots")
                elif stat == "Pts+Rebs+Asts" or stat == "Pts + Reb + Ast":
                    sportsbook_newStats.append("Pts + Rebs + Asts")
                elif stat == "Ast + Reb" or stat == "Rebs+Asts":
                    sportsbook_newStats.append("Rebounds + Assists")
                elif stat == "Pts + Ast" or stat == "Pts+Asts":
                    sportsbook_newStats.append("Points + Assists")
                elif stat == "Pts + Reb" or stat == "Pts+Rebs":
                    sportsbook_newStats.append("Points + Rebounds")
                elif stat == "Threes" or stat == "3-PT Made" or "3 Point FG" in stat:
                    sportsbook_newStats.append("3-Pointers Made")
                elif "Double+Double" in stat:
                    sportsbook_newStats.append("Double Doubles")
                elif "Triple+Double" in stat:
                    sportsbook_newStats.append("Triple Doubles")
                else:
                    sportsbook_newStats.append(stat)
        elif "PrizePicks" in dfs:
            for stat in sportsbook_oldStats:
                if "Total Strikeouts" in stat:
                    sportsbook_newStats.append("Pitcher Strikeouts")
                elif "Threes" in stat or "3-Pointers Made" in stat:
                    sportsbook_newStats.append("3-PT Made")
                elif "Blocks" in stat:
                    sportsbook_newStats.append("Blocked Shots")
                elif "Strikeouts Thrown" in stat:
                    sportsbook_newStats.append("Pitcher Strikeouts")
                elif "Runs Scored" in stat:
                    sportsbook_newStats.append("Runs")
                elif "Saves" in stat:
                    sportsbook_newStats.append("Goalie Saves")
                elif "Hits + Runs + RBIs" in stat:
                    sportsbook_newStats.append("Hits+Runs+RBIs")
                elif "Kills on Maps 1+2+3" in stat or "Kills in Maps 1+2+3" in stat:
                    sportsbook_newStats.append("MAPS 1-3 Kills")
                elif "Kills on Maps 1+2" in stat or "Kills on Map 1+2" in stat or "Kills in Maps 1+2" in stat:
                    sportsbook_newStats.append("MAPS 1-2 Kills")
                elif "Headshots on Maps 1+2+3" in stat:
                    sportsbook_newStats.append("MAPS 1-3 Headshots")
                elif "Headshots on Maps 1+2" in stat:
                    sportsbook_newStats.append("MAPS 1-2 Headshots")
                elif "Kills on Map 1" in stat:
                    sportsbook_newStats.append("MAP 1 Kills")
                elif "Kills on Map 2" in stat:
                    sportsbook_newStats.append("MAP 2 Kills")
                elif "Kills on Map 3" in stat:
                    sportsbook_newStats.append("MAP 3 Kills")
                elif "Headshots on Map 1" in stat:
                    sportsbook_newStats.append("MAP 1 Headshots")
                elif "Assists on Maps 1+2+3" in stat:
                    sportsbook_newStats.append("MAPS 1-3 Assists")
                elif "Assists on Maps 1+2" in stat:
                    sportsbook_newStats.append("MAPS 1-2 Assists")
                elif "Assists on Map 1" in stat:
                    sportsbook_newStats.append("MAP 1 Assists")
                elif "Batter Strikeouts" in stat:
                    sportsbook_newStats.append("Hitter Strikeouts")
                elif "Strikeouts" in stat:
                    sportsbook_newStats.append("Pitcher Strikeouts")
                elif "3-Pointers Made" in stat and "1H" not in stat:
                    sportsbook_newStats.append("3-PT Made")
                elif "Hits + Runs + RBIs" in stat:
                    sportsbook_newStats.append("Hits+Runs+RBIs")
                elif "Batter Walks" in stat:
                    sportsbook_newStats.append("Walks")
                elif "Birdies or Better" in stat:
                    sportsbook_newStats.append("Birdies Or Better")
                elif "Shots on Target" in stat:
                    sportsbook_newStats.append("Shots On Target")
                elif "Shots Attempted" in stat:
                    sportsbook_newStats.append("Shots")
                elif "Saves" in stat:
                    sportsbook_newStats.append("Goalie Saves")
                elif "Pts + Rebs + Asts" in stat and "1H" not in stat:
                    sportsbook_newStats.append("Pts+Rebs+Asts")
                elif "Points + Rebounds" in stat and "1H" not in stat:
                    sportsbook_newStats.append("Pts+Rebs")
                elif "Rebounds + Assists" in stat and "1H" not in stat:
                    sportsbook_newStats.append("Rebs+Asts")
                elif "Points + Assists" in stat and "1H" not in stat:
                    sportsbook_newStats.append("Pts+Asts")
                elif stat == "Passing Yards":
                    sportsbook_newStats.append("Pass Yards")
                elif stat == "Rushing Yards":
                    sportsbook_newStats.append("Rush Yards")
                elif stat == "Rush + Rec TDs":
                    sportsbook_newStats.append("Rush+Rec TDs")
                elif stat == "Passing TDs":
                    sportsbook_newStats.append("Pass TDs")
                elif stat == "Rush + Rec Yards":
                    sportsbook_newStats.append("Rush+Rec Yards")
                elif stat == "Passing Attempts":
                    sportsbook_newStats.append("Pass Attempts")
                elif stat == "Completions":
                    sportsbook_newStats.append("Pass Completions")
                elif stat == "Interceptions":
                    sportsbook_newStats.append("INT")
                elif stat == "Pass + Rush Yards":
                    sportsbook_newStats.append("Pass+Rush Yds")
                elif stat == "Rushing Attempts":
                    sportsbook_newStats.append("Rush Attempts")
                elif stat == "Targets":
                    sportsbook_newStats.append("Rec Targets")
                elif stat == "Rec Yards":
                    sportsbook_newStats.append("Receiving Yards")
                elif stat == "Kicking Pts":
                    sportsbook_newStats.append("Kicking Points")
                elif stat == "TD Passes":
                    sportsbook_newStats.append("Pass TDs")
                elif stat == "Anytime TD":
                    sportsbook_newStats.append("Rush+Rec TDs")
                elif stat == "Pts + Rebs + Asts" or stat == "Pts + Reb + Ast":
                    sportsbook_newStats.append("Pts+Rebs+Asts")
                elif stat == "Ast + Reb" or stat == "Rebounds + Assists":
                    sportsbook_newStats.append("Rebs+Asts")
                elif stat == "Pts + Ast" or stat == "Points + Assists":
                    sportsbook_newStats.append("Pts+Asts")
                elif stat == "Pts + Reb" or stat == "Points + Rebounds":
                    sportsbook_newStats.append("Pts+Rebs")
                elif stat == "Threes" or stat == "3-Pointers Made":
                    sportsbook_newStats.append("3-PT Made")
                else:
                    sportsbook_newStats.append(stat)
                    
        from datetime import datetime, timedelta
        def is_within_next_hour(target_time_str):
            current_time = datetime.now()
            upper_boundary = current_time + timedelta(hours=1)
            target_time = datetime.strptime(target_time_str, "%I:%M%p")
            target_time = target_time.replace(year=current_time.year, month=current_time.month, day=current_time.day)
            return current_time <= target_time <= upper_boundary
                    
        i = 0
        while i < len(sportsbook_names):
            j = 0
            while j < len(dfs_names):
                if sportsbook_names[i] == dfs_names[j]:
                    if 0 <= i < len(sportsbook_newStats) and 0 <= j < len(dfs_stats):
                        try:
                            if (sportsbook_newStats[i] == dfs_stats[j]) and (("GOLF" in sport) or (sportsbook_times[i] == dfs_times[j]) or (":" not in str(dfs_times[j]) and is_within_next_hour(str(sportsbook_times[i]))) or (":" not in str(sportsbook_times[i]) and is_within_next_hour(str(dfs_times[j]))) or "DraftKings" in sportsbook or "Pinnacle" in sportsbook):
                                if float(sportsbook_oldLines[i]) == float(dfs_oldLines[j]):
                                    higherOrLower = ""
                                    try:
                                        higherOrLower = str((dfs_higherOrLowers)[j])
                                    except UnboundLocalError:
                                        pass
                                    if "Higher" in higherOrLower:
                                        multiplier = dfs_payouts[j][:-1]
                                        if float(multiplier) <= 1:
                                            names.append(sportsbook_names[i])
                                            stats.append(sportsbook_newStats[i])
                                            sportsbooks.append(sportsbook)
                                            sportsbook_lines.append(sportsbook_oldLines[i])
                                            dfs_lines.append(dfs_oldLines[j])
                                            discrepancies.append("0")
                                            higherOrLowers.append(dfs_higherOrLowers[j])
                                            times.append(dfs_times[j])
                                            try:
                                                payouts.append(dfs_payouts[j])
                                            except UnboundLocalError:
                                                payouts.append("1x")
                                            if "PrizePicks" in sportsbook:
                                                overPercentages.append(0.5)
                                                underPercentages.append(0.5)
                                                value = round((((0.5 * float(multiplier)) ** 3) * 6 - 1) * 100, 1)
                                                evs.append(float(value))
                                                overPrices.append(1.817)
                                                underPrices.append(1.817)
                                            elif "Pinnacle" in sportsbook or "DraftKings" in sportsbook:
                                                sportsbook_overPercentages = sportsbook_df["% Over"].values.tolist()
                                                sportsbook_underPercentages = sportsbook_df["% Under"].values.tolist()
                                                sportsbook_overPrices = sportsbook_df["Over Price"].values.tolist()
                                                sportsbook_underPrices = sportsbook_df["Under Price"].values.tolist()
                                                overPercentage = sportsbook_overPercentages[i]
                                                overPercentages.append(overPercentage)
                                                underPercentage = sportsbook_underPercentages[i]
                                                underPercentages.append(underPercentage)
                                                overPrices.append(sportsbook_overPrices[i])
                                                underPrices.append(sportsbook_underPrices[i])
                                                value = round((((overPercentage * float(multiplier)) ** 3) * 6 - 1) * 100, 1)
                                                evs.append(float(value))
                                        elif float(multiplier) <= 2.5:
                                            names1.append(sportsbook_names[i])
                                            stats1.append(sportsbook_newStats[i])
                                            sportsbooks1.append(sportsbook)
                                            sportsbook_lines1.append(sportsbook_oldLines[i])
                                            dfs_lines1.append(dfs_oldLines[j])
                                            discrepancies1.append("0")
                                            higherOrLowers1.append(dfs_higherOrLowers[j])
                                            times1.append(dfs_times[j])
                                            try:
                                                payouts1.append(dfs_payouts[j])
                                            except UnboundLocalError:
                                                payouts1.append("1x")
                                            if "PrizePicks" in sportsbook:
                                                overPercentages1.append(0.5)
                                                underPercentages1.append(1-0.5)
                                                value = round((((0.5 * float(multiplier)) ** 3) * 6 - 1) * 100, 1)
                                                evs1.append(float(value))
                                                overPrices1.append(1.817)
                                                underPrices1.append(1.817)
                                            elif "Pinnacle" in sportsbook or "DraftKings" in sportsbook:
                                                sportsbook_overPercentages = sportsbook_df["% Over"].values.tolist()
                                                sportsbook_underPercentages = sportsbook_df["% Under"].values.tolist()
                                                sportsbook_overPrices = sportsbook_df["Over Price"].values.tolist()
                                                sportsbook_underPrices = sportsbook_df["Under Price"].values.tolist()
                                                overPercentage = sportsbook_overPercentages[i]
                                                overPercentages1.append(overPercentage)
                                                underPercentage = sportsbook_underPercentages[i]
                                                underPercentages1.append(underPercentage)
                                                overPrices1.append(sportsbook_overPrices[i])
                                                underPrices1.append(sportsbook_underPrices[i])
                                                value = round((((overPercentage * float(multiplier)) ** 3) * 6 - 1) * 100, 1)
                                                evs1.append(float(value))
                                        else:
                                            names2.append(sportsbook_names[i])
                                            stats2.append(sportsbook_newStats[i])
                                            sportsbooks2.append(sportsbook)
                                            sportsbook_lines2.append(sportsbook_oldLines[i])
                                            dfs_lines2.append(dfs_oldLines[j])
                                            discrepancies2.append("0")
                                            higherOrLowers2.append(dfs_higherOrLowers[j])
                                            times2.append(dfs_times[j])
                                            try:
                                                payouts2.append(dfs_payouts[j])
                                            except UnboundLocalError:
                                                payouts2.append("1x")
                                            sportsbook_overPercentages = sportsbook_df["% Over"].values.tolist()
                                            sportsbook_underPercentages = sportsbook_df["% Under"].values.tolist()
                                            sportsbook_overPrices = sportsbook_df["Over Price"].values.tolist()
                                            sportsbook_underPrices = sportsbook_df["Under Price"].values.tolist()
                                            overPercentage = sportsbook_overPercentages[i]
                                            overPercentages2.append(overPercentage)
                                            underPercentage = sportsbook_underPercentages[i]
                                            underPercentages2.append(underPercentage)
                                            overPrices2.append(sportsbook_overPrices[i])
                                            underPrices2.append(sportsbook_underPrices[i])
                                            value = round((((overPercentage * float(multiplier)) ** 2) * 3 - 1) * 100, 1)
                                            evs2.append(float(value))
                                    elif "Lower" in higherOrLower:
                                        multiplier = dfs_payouts[j][:-1]
                                        if float(multiplier) <= 1.1:
                                            names.append(sportsbook_names[i])
                                            stats.append(sportsbook_newStats[i])
                                            sportsbooks.append(sportsbook)
                                            sportsbook_lines.append(sportsbook_oldLines[i])
                                            dfs_lines.append(dfs_oldLines[j])
                                            times.append(dfs_times[j])
                                            try:
                                                payouts.append(dfs_payouts[j])
                                            except UnboundLocalError:
                                                payouts.append("1x")
                                            discrepancy = float(dfs_oldLines[j]) - float(sportsbook_oldLines[i])
                                            discrepancies.append(discrepancy)
                                            higherOrLowers.append(dfs_higherOrLowers[j])
                                            if "PrizePicks" in sportsbook:
                                                underPercentages.append(0.5)
                                                overPercentages.append(0.5)
                                                value = round((((0.5 * float(multiplier)) ** 3) * 6 - 1) * 100, 1)
                                                evs.append(float(value))
                                                overPrices.append(1.817)
                                                underPrices.append(1.817)
                                            elif "Pinnacle" in sportsbook or "DraftKings" in sportsbook:
                                                sportsbook_overPercentages = sportsbook_df["% Over"].values.tolist()
                                                sportsbook_underPercentages = sportsbook_df["% Under"].values.tolist()
                                                sportsbook_overPrices = sportsbook_df["Over Price"].values.tolist()
                                                sportsbook_underPrices = sportsbook_df["Under Price"].values.tolist()
                                                overPercentage = sportsbook_overPercentages[i]
                                                overPercentages.append(overPercentage)
                                                underPercentage = sportsbook_underPercentages[i]
                                                underPercentages.append(underPercentage)
                                                overPrices.append(sportsbook_overPrices[i])
                                                underPrices.append(sportsbook_underPrices[i])
                                                value = round((((underPercentage * float(multiplier)) ** 3) * 6 - 1) * 100, 1)
                                                evs.append(float(value))
                                        elif float(multiplier) <= 2.5:
                                            names1.append(sportsbook_names[i])
                                            stats1.append(sportsbook_newStats[i])
                                            sportsbooks1.append(sportsbook)
                                            sportsbook_lines1.append(sportsbook_oldLines[i])
                                            dfs_lines1.append(dfs_oldLines[j])
                                            times1.append(dfs_times[j])
                                            try:
                                                payouts1.append(dfs_payouts[j])
                                            except UnboundLocalError:
                                                payouts1.append("1x")
                                            discrepancy = float(dfs_oldLines[j]) - float(sportsbook_oldLines[i])
                                            discrepancies1.append(discrepancy)
                                            higherOrLowers1.append(dfs_higherOrLowers[j])
                                            if "PrizePicks" in sportsbook or "Underdog" in sportsbook:
                                                underPercentages1.append(0.5)
                                                overPercentages1.append(1-0.5)
                                                value = round((((0.5 * float(multiplier)) ** 3) * 6 - 1) * 100, 1)
                                                evs1.append(float(value))
                                                overPrices1.append(1.817)
                                                underPrices1.append(1.817)
                                            elif "Pinnacle" in sportsbook or "DraftKings" in sportsbook:
                                                sportsbook_overPercentages = sportsbook_df["% Over"].values.tolist()
                                                sportsbook_underPercentages = sportsbook_df["% Under"].values.tolist()
                                                sportsbook_overPrices = sportsbook_df["Over Price"].values.tolist()
                                                sportsbook_underPrices = sportsbook_df["Under Price"].values.tolist()
                                                overPercentage = sportsbook_overPercentages[i]
                                                overPercentages1.append(overPercentage)
                                                underPercentage = sportsbook_underPercentages[i]
                                                underPercentages1.append(underPercentage)
                                                overPrices1.append(sportsbook_overPrices[i])
                                                underPrices1.append(sportsbook_underPrices[i])
                                                value = round((((underPercentage * float(multiplier)) ** 3) * 6 - 1) * 100, 1)
                                                evs1.append(float(value))
                                        else:
                                            names2.append(sportsbook_names[i])
                                            stats2.append(sportsbook_newStats[i])
                                            sportsbooks2.append(sportsbook)
                                            sportsbook_lines2.append(sportsbook_oldLines[i])
                                            dfs_lines2.append(dfs_oldLines[j])
                                            times2.append(dfs_times[j])
                                            try:
                                                payouts2.append(dfs_payouts[j])
                                            except UnboundLocalError:
                                                payouts2.append("1x")
                                            discrepancy = float(dfs_oldLines[j]) - float(sportsbook_oldLines[i])
                                            discrepancies2.append(discrepancy)
                                            higherOrLowers2.append(dfs_higherOrLowers[j])
                                            sportsbook_overPercentages = sportsbook_df["% Over"].values.tolist()
                                            sportsbook_underPercentages = sportsbook_df["% Under"].values.tolist()
                                            sportsbook_overPrices = sportsbook_df["Over Price"].values.tolist()
                                            sportsbook_underPrices = sportsbook_df["Under Price"].values.tolist()
                                            overPercentage = sportsbook_overPercentages[i]
                                            overPercentages2.append(overPercentage)
                                            underPercentage = sportsbook_underPercentages[i]
                                            underPercentages2.append(underPercentage)
                                            overPrices2.append(sportsbook_overPrices[i])
                                            underPrices2.append(sportsbook_underPrices[i])
                                            value = round((((underPercentage * float(multiplier)) ** 2) * 3 - 1) * 100, 1)
                                            evs2.append(float(value))
                                    else:
                                        sportsbook_multiplier = "1"
                                        try:
                                            if "x" in str(sportsbook_payouts[i]):
                                                sportsbook_multiplier = str(sportsbook_payouts[i])[:-1]
                                        except UnboundLocalError:
                                            pass
                                        multiplier = "1"
                                        names.append(sportsbook_names[i])
                                        stats.append(sportsbook_newStats[i])
                                        sportsbooks.append(sportsbook)
                                        sportsbook_lines.append(sportsbook_oldLines[i])
                                        dfs_lines.append(dfs_oldLines[j])
                                        discrepancies.append("0")
                                        payouts.append("1x")
                                        times.append(dfs_times[j])
                                        if "PrizePicks" in sportsbook:
                                            overPercentages.append(0.5)
                                            underPercentages.append(0.5)
                                            value = round((((0.5 * float(multiplier)) ** 3) * 6 - 1) * 100, 1)
                                            evs.append(float(value))
                                            overPrices.append(1.817)
                                            underPrices.append(1.817)
                                            higherOrLowers.append("Higher")
                                            overPercentages.append(0.5)
                                            underPercentages.append(0.5)
                                            value = round((((0.5 * float(multiplier)) ** 3) * 6 - 1) * 100, 1)
                                            evs.append(float(value))
                                            overPrices.append(1.817)
                                            underPrices.append(1.817)
                                            higherOrLowers.append("Lower")
                                            names.append(sportsbook_names[i])
                                            stats.append(sportsbook_newStats[i])
                                            sportsbooks.append(sportsbook)
                                            sportsbook_lines.append(sportsbook_oldLines[i])
                                            dfs_lines.append(dfs_oldLines[j])
                                            discrepancies.append("0")
                                            payouts.append("1x")
                                            times.append(dfs_times[j])
                                        elif "Underdog" in sportsbook:
                                            if "Higher" in str(sportsbook_higherOrLowers[i]):
                                                overPercentages.append(0.5 / float(sportsbook_multiplier))
                                                underPercentages.append(0.5 * float(sportsbook_multiplier))
                                                value = round((((0.5 * float(sportsbook_multiplier) * float(multiplier)) ** 3) * 6 - 1) * 100, 1)
                                                evs.append(float(value))
                                                overPrices.append(1.817 * float(sportsbook_multiplier))
                                                underPrices.append(1.817 / float(sportsbook_multiplier))
                                                higherOrLowers.append("Lower")
                                            elif "Lower" in str(sportsbook_higherOrLowers[i]):
                                                overPercentages.append(0.5 * float(sportsbook_multiplier))
                                                underPercentages.append(0.5 / float(sportsbook_multiplier))
                                                value = round((((0.5 * float(sportsbook_multiplier) * float(multiplier)) ** 3) * 6 - 1) * 100, 1)
                                                evs.append(float(value))
                                                overPrices.append(1.817 / float(sportsbook_multiplier))
                                                underPrices.append(1.817 * float(sportsbook_multiplier))
                                                higherOrLowers.append("Higher")
                                            else:
                                                overPercentages.append(0.5)
                                                underPercentages.append(0.5)
                                                value = round((((0.5 * float(multiplier)) ** 3) * 6 - 1) * 100, 1)
                                                evs.append(float(value))
                                                overPrices.append(1.817)
                                                underPrices.append(1.817)
                                                higherOrLowers.append("Higher")
                                                overPercentages.append(0.5)
                                                underPercentages.append(0.5)
                                                value = round((((0.5 * float(multiplier)) ** 3) * 6 - 1) * 100, 1)
                                                evs.append(float(value))
                                                overPrices.append(1.817)
                                                underPrices.append(1.817)
                                                higherOrLowers.append("Lower")
                                                names.append(sportsbook_names[i])
                                                stats.append(sportsbook_newStats[i])
                                                sportsbooks.append(sportsbook)
                                                sportsbook_lines.append(sportsbook_oldLines[i])
                                                dfs_lines.append(dfs_oldLines[j])
                                                discrepancies.append("0")
                                                payouts.append("1x")
                                                times.append(dfs_times[j])
                                        elif "Pinnacle" in sportsbook or "DraftKings" in sportsbook:
                                            sportsbook_overPercentages = sportsbook_df["% Over"].values.tolist()
                                            sportsbook_underPercentages = sportsbook_df["% Under"].values.tolist()
                                            sportsbook_overPrices = sportsbook_df["Over Price"].values.tolist()
                                            sportsbook_underPrices = sportsbook_df["Under Price"].values.tolist()
                                            overPercentage = sportsbook_overPercentages[i]
                                            underPercentage = sportsbook_underPercentages[i]
                                            overPercentages.append(overPercentage)
                                            underPercentages.append(underPercentage)
                                            overPrices.append(sportsbook_overPrices[i])
                                            underPrices.append(sportsbook_underPrices[i])
                                            value = round((((overPercentage * float(multiplier)) ** 3) * 6 - 1) * 100, 1)
                                            evs.append(float(value))
                                            higherOrLowers.append("Higher")
                                            overPercentages.append(overPercentage)
                                            underPercentages.append(underPercentage)
                                            overPrices.append(sportsbook_overPrices[i])
                                            underPrices.append(sportsbook_underPrices[i])
                                            value = round((((underPercentage * float(multiplier)) ** 3) * 6 - 1) * 100, 1)
                                            evs.append(float(value))
                                            higherOrLowers.append("Lower")
                                            names.append(sportsbook_names[i])
                                            stats.append(sportsbook_newStats[i])
                                            sportsbooks.append(sportsbook)
                                            sportsbook_lines.append(sportsbook_oldLines[i])
                                            dfs_lines.append(dfs_oldLines[j])
                                            discrepancies.append("0")
                                            payouts.append("1x")
                                            times.append(dfs_times[j])
                                else:
                                    sportsbook_multiplier = "1"
                                    try:
                                        if "x" in str(sportsbook_payouts[i]):
                                            sportsbook_multiplier = str(sportsbook_payouts[i])[:-1]
                                    except UnboundLocalError:
                                        pass
                                    sportsbook_higherOrLower = ""
                                    try:
                                        sportsbook_higherOrLower = str(sportsbook_higherOrLowers[i])
                                    except UnboundLocalError:
                                        pass
                                    multiplier = "1"
                                    try:
                                        multiplier = str(dfs_payouts[j])[:-1]
                                    except UnboundLocalError:
                                        pass
                                    discrepancy = float(dfs_oldLines[j]) - float(sportsbook_oldLines[i])
                                    middle = (float(sportsbook_oldLines[i]) + float(dfs_oldLines[j])) / 2
                                    tempSport = dfs_df['Sport'].values.tolist()[j]
                                    tempStat = dfs_df['Stat'].values.tolist()[j]
                                    tempLine = (float(sportsbook_df['Line'].values.tolist()[i]) + float(dfs_df['Line'].values.tolist()[j])) / 2
                                    standardDev = float(sportsbook_oldLines[i]) / 1.25
                                    if "LoL" in tempSport or '/lol' in tempSport:
                                        if "Kills" in tempStat:
                                            if float(tempLine) > 7:
                                                standardDev = 4.516168958
                                            elif float(tempLine) > 5:
                                                standardDev = 3.58808277
                                            else:
                                                standardDev = 2.118145047
                                        elif "Assists" in tempStat:
                                            if float(tempLine) > 9:
                                                standardDev = 5.437868992
                                            elif float(tempLine) > 6:
                                                standardDev = 4.352977811
                                            else:
                                                standardDev = 3.319898845
                                        elif "Deaths" in tempStat:
                                            if float(tempLine) > 6:
                                                standardDev = 2.085348505
                                            elif float(tempLine) > 3:
                                                standardDev = 1.994106434
                                            else:
                                                standardDev = 1.690664301
                                    elif "MLB" in tempSport or '/mlb' in tempSport:
                                        if "Total Bases" in tempStat:
                                            if float(tempLine) > 1.75:
                                                standardDev = 2.117690388
                                            elif float(tempLine) > 1.25:
                                                standardDev = 1.775888646
                                            else:
                                                standardDev = 1.45863635
                                        elif "Earned Runs" in tempStat:
                                            if float(tempLine) > 2.75:
                                                standardDev = 1.696229048
                                            elif float(tempLine) > 2.25:
                                                standardDev = 1.987027035
                                            elif float(tempLine) > 1.75:
                                                standardDev = 1.959887171
                                            else:
                                                standardDev = 1.305949358
                                        elif "Hits Allowed" in tempStat:
                                            if float(tempLine) > 5.75:
                                                standardDev = 2.166987156
                                            elif float(tempLine) > 5.25:
                                                standardDev = 2.263953474
                                            elif float(tempLine) > 4.75:
                                                standardDev = 2.620780155
                                            else:
                                                standardDev = 2.218407667
                                        elif "Walks Allowed" in tempStat:
                                            if float(tempLine) > 1.75:
                                                standardDev = 1.048530021
                                            elif float(tempLine) > 1.25:
                                                standardDev = 1.187937243
                                            else:
                                                standardDev = 0.759091333
                                        elif "Hits + Runs + RBI" in tempStat or "Hits+Runs+RBI" in tempStat:
                                            if float(tempLine) > 2.75:
                                                standardDev = 2.225507721
                                            elif float(tempLine) > 2.25:
                                                standardDev = 2.248137356
                                            elif float(tempLine) > 1.75:
                                                standardDev = 1.988185644
                                            else:
                                                standardDev = 1.828742722
                                        elif "Hits" in tempStat:
                                            if float(tempLine) > 1.25:
                                                standardDev = 0.946907923
                                            elif float(tempLine) > 0.75:
                                                standardDev = 0.889525319
                                            else:
                                                standardDev = 0.768260704
                                        elif "Batter Strikeouts" in tempStat or "Hitter Strikeouts" in tempStat:
                                            if float(tempLine) > 1.25:
                                                standardDev = 0.922423379
                                            elif float(tempLine) > 0.75:
                                                standardDev = 0.892862689
                                            else:
                                                standardDev = 0.740882244
                                        elif "Strikeouts" in tempStat:
                                            if float(tempLine) > 6.25:
                                                standardDev = 2.450305375
                                            elif float(tempLine) > 4.75:
                                                standardDev = 2.231997459
                                            else:
                                                standardDev = 2.473189574
                                    elif "VAL" in tempSport or '/val' in tempSport:
                                        if "Kills" in tempStat:
                                            if float(tempLine) > 45:
                                                standardDev = 18.80904038
                                            elif float(tempLine) > 35:
                                                standardDev = 13.05201267
                                            else:
                                                standardDev = 7.71083109
                                        elif "Assists" in tempStat:
                                            if float(tempLine) > 30:
                                                standardDev = 19.09188309
                                            elif float(tempLine) > 20:
                                                standardDev = 9.545941546
                                            elif float(tempLine) > 10:
                                                standardDev = 4.975001282
                                            else:
                                                standardDev = 3.154784101
                                        elif "Deaths" in tempStat:
                                            if float(tempLine) > 50:
                                                standardDev = 26.87005769
                                            elif float(tempLine) > 40:
                                                standardDev = 14.00071427
                                            else:
                                                standardDev = 7.179853471
                                    elif "PGA" in tempSport or "/pga" in tempSport or "OGOLF" in tempSport or "/olympic_golf" in tempSport or "/golf" in tempSport or "LIVGOLF" in tempSport:
                                        if "Strokes" in tempStat:
                                            standardDev = 3
                                        elif "Birdies" in tempStat:
                                            if float(tempLine) > 4:
                                                standardDev = 1.898420626
                                            elif float(tempLine) > 3:
                                                standardDev = 1.804750401
                                            else:
                                                standardDev = 1.763762616
                                    elif "SOCCER" in tempSport or "/soccer" in tempSport or "/o_soccer" in tempSport or "/fifa" in tempSport or '/wsoccer' in tempSport:
                                        if "Shots on Target" in tempStat or "Shots On Target" in tempStat:
                                            if float(tempLine) > 1.25:
                                                standardDev = 0.951189731
                                            elif float(tempLine) > 0.75:
                                                standardDev = 0.757110965
                                            else:
                                                standardDev = 0.620527073
                                        elif "Shots" in tempStat and "Shots Assisted" not in tempStat:
                                            if float(tempLine) > 2.5:
                                                standardDev = 1.511885783
                                            elif float(tempLine) > 1:
                                                standardDev = 1.43410989
                                            else:
                                                standardDev = 0.628025604
                                        elif "Goals Allowed" in tempStat:
                                            if float(tempLine) > 1.5:
                                                standardDev = 1.227066294
                                            elif float(tempLine) > 0.75:
                                                standardDev = 1.141946323
                                            else:
                                                standardDev = 0.67017893
                                        elif "Saves" in tempStat:
                                            if float(tempLine) > 3.5:
                                                standardDev = 2.93212243
                                            elif float(tempLine) > 2.5:
                                                standardDev = 1.953077392
                                            else:
                                                standardDev = 1.234448788
                                    elif "NBA" in tempSport or "/nba" in tempSport or "/basketball" in tempSport or "OBBALL" in tempSport or "/olympic_basketball" in tempSport or "WNBA" in tempSport or "/wnba" in tempSport:
                                        if "Points + Rebounds + Assists" in tempStat or "Points+Rebounds+Assists" in tempStat:
                                            if float(tempLine) > 30:
                                                standardDev = 9.654034593
                                            elif float(tempLine) > 20:
                                                standardDev = 8.600107508
                                            elif float(tempLine) > 8:
                                                standardDev = 7.455263356
                                            else:
                                                standardDev = 4.143670333
                                        elif "Points + Assists" in tempStat or "Pts+Asts" in tempStat:
                                            if float(tempLine) > 25:
                                                standardDev = 8.512946597
                                            elif float(tempLine) > 15:
                                                standardDev = 7.442072799
                                            elif float(tempLine) > 6:
                                                standardDev = 5.966991661
                                            else:
                                                standardDev = 3.188556075
                                        elif "Points + Rebounds" in tempStat or "Pts+Rebs" in tempStat:
                                            if float(tempLine) > 25:
                                                standardDev = 9.107967809
                                            elif float(tempLine) > 15:
                                                standardDev = 7.82006781
                                            elif float(tempLine) > 6:
                                                standardDev = 6.481179673
                                            else:
                                                standardDev = 3.506160574
                                        elif "Rebounds + Assists" in tempStat or "Rebs+Asts" in tempStat:
                                            if float(tempLine) > 10:
                                                standardDev = 4.337586542
                                            elif float(tempLine) > 7:
                                                standardDev = 3.636612521
                                            elif float(tempLine) > 4:
                                                standardDev = 3.226938434
                                            else:
                                                standardDev = 2.010717369
                                        elif "3-PT Made" in tempStat or "3-Pointers Made" in tempStat:
                                            if float(tempLine) > 3.25:
                                                standardDev = 1.975369909
                                            elif float(tempLine) > 2.25:
                                                standardDev = 1.679031433
                                            elif float(tempLine) > 1.25:
                                                standardDev = 1.412853582
                                            else:
                                                standardDev = 0.788664417
                                        elif "Steals" in tempStat:
                                            if float(tempLine) > 1.75:
                                                standardDev = 1.486175435
                                            elif float(tempLine) > 1.25:
                                                standardDev = 1.264253457
                                            elif float(tempLine) > 0.75:
                                                standardDev = 0.96688369
                                            else:
                                                standardDev = 0.656297334
                                        elif "Blocks" in tempStat or "Blocked Shots" in tempStat:
                                            if float(tempLine) > 2.25:
                                                standardDev = 2.54681357
                                            elif float(tempLine) > 1.75:
                                                standardDev = 1.575473744
                                            elif float(tempLine) > 1.25:
                                                standardDev = 1.23559388
                                            elif float(tempLine) > 0.75:
                                                standardDev = 1.008950055
                                            else:
                                                standardDev = 0.613984115
                                        elif "Rebounds" in tempStat:
                                            if float(tempLine) > 311:
                                                standardDev = 4.77788195
                                            elif float(tempLine) > 8:
                                                standardDev = 3.440733621
                                            elif float(tempLine) > 4:
                                                standardDev = 2.863009048
                                            else:
                                                standardDev = 1.658522506
                                        elif "Points" in tempStat:
                                            if float(tempLine) > 25:
                                                standardDev = 8.37812274
                                            elif float(tempLine) > 20:
                                                standardDev = 8.152253173
                                            elif float(tempLine) > 14:
                                                standardDev = 6.705450373
                                            elif float(tempLine) > 11:
                                                standardDev = 6.306422186
                                            elif float(tempLine) > 7:
                                                standardDev = 5.365162329
                                            else:
                                                standardDev = 3.581245485
                                        elif "Assists" in tempStat:
                                            if float(tempLine) > 8:
                                                standardDev = 2.893506536
                                            elif float(tempLine) > 6:
                                                standardDev = 2.795596645
                                            elif float(tempLine) > 4:
                                                standardDev = 2.480347531
                                            else:
                                                standardDev = 1.79720224
                                    elif "CS2" in tempSport or "/cs2" in tempSport:
                                        if "Kills" in tempStat:
                                            if float(tempLine) > 18:
                                                standardDev = 5.754809761
                                            elif float(tempLine) > 14:
                                                standardDev = 4.361990501
                                            else:
                                                standardDev = 4.073651122
                                        elif "Headshots" in tempStat:
                                            if float(tempLine) > 10:
                                                standardDev = 4.548475535
                                            elif float(tempLine) > 7:
                                                standardDev = 3.125716759
                                            elif float(tempLine) > 4:
                                                standardDev = 2.632166008
                                            else:
                                                standardDev = 1.727650566
                                    elif "NFL" in tempSport or "/nfl" in tempSport or "CFB" in tempSport or "/cfb" in tempSport:
                                        if "Rush Attempts" in tempStat or "Rushing Attempts" in tempStat:
                                            if float(tempLine) > 12:
                                                standardDev = 6.124917468
                                            elif float(tempLine) > 7:
                                                standardDev = 4.601316013
                                            else:
                                                standardDev = 3.074738589
                                        elif "Rush Yards" in tempStat or "Rushing Yards" in tempStat or "Longest Rush" in tempStat:
                                            if float(tempLine) > 60:
                                                standardDev = 35.95687957
                                            elif float(tempLine) > 45:
                                                standardDev = 31.62514014
                                            elif float(tempLine) > 25:
                                                standardDev = 20.91688832
                                            else:
                                                standardDev = 12.76973855
                                        elif "Rush + Rec TDs" in tempStat or "Rush+Rec TDs" in tempStat:
                                            standardDev = 0.449677167
                                        elif "Rec Yards" in tempStat or "Receiving Yards" in tempStat or "Longets Reception" in tempStat:
                                            if float(tempLine) > 60:
                                                standardDev = 46.5776403
                                            elif float(tempLine) > 40:
                                                standardDev = 33.82604042
                                            elif float(tempLine) > 20:
                                                standardDev = 20.91688832
                                            else:
                                                standardDev = 16.08755804
                                        elif "Receptions" in tempStat:
                                            if float(tempLine) > 6:
                                                standardDev = 2.948045532
                                            elif float(tempLine) > 3:
                                                standardDev = 2.076409481
                                            else:
                                                standardDev = 1.6599949
                                        elif "Targets" in tempStat:
                                            if float(tempLine) > 9:
                                                standardDev = 3.950267146
                                            elif float(tempLine) > 5:
                                                standardDev = 2.736476669
                                            else:
                                                standardDev = 2.363933286
                                        elif "Rush+Rec Yards" in tempStat or "Rush + Rec Yards" in tempStat:
                                            if float(tempLine) > 60:
                                                standardDev = 42.06856494
                                            elif float(tempLine) > 40:
                                                standardDev = 35.54067739
                                            else:
                                                standardDev = 20.03676482
                                        elif "Pass Yards" in tempStat or "Passing Yards" in tempStat or "Longest Completion" in tempStat:
                                            standardDev = 75.63872818
                                        elif "Completions" in tempStat:
                                            standardDev = 5.803266699
                                        elif "Pass Attempts" in tempStat or "Passing Attempts" in tempStat:
                                            standardDev = 7.90696985613982
                                        elif "TD Passes" in tempStat or "Pass TDs" in tempStat or "Passing TDs" in tempStat:
                                            standardDev = 0.990825882401897
                                        elif "INT" in tempStat or "Interceptions" in tempStat:
                                            standardDev = 0.749110694728588
                                        elif "Sacks Taken" in tempStat:
                                            if float(tempLine) > 2.25:
                                                standardDev = 1.782150091
                                            else:
                                                standardDev = 1.674319283
                                        elif "Pass+Rush TDs" in tempStat or "Pass + Rush TDs" in tempStat:
                                            standardDev = 1.08597846839806
                                        elif "Pass + Rush Yards" in tempStat or "Pass+Rush Yards" in tempStat:
                                            standardDev = 81.3220399602091
                                        elif "Sacks" in tempStat:
                                            standardDev = 0.642282689957109
                                        elif "Tackles+Assists" in tempStat or "Tackles + Assists" in tempStat:
                                            if float(tempLine) > 2.5:
                                                standardDev = 2.062511004
                                            else:
                                                standardDev = 1.657059937
                                        elif "Solo Tackles" in tempStat:
                                            if float(tempLine) > 2:
                                                standardDev = 1.634447169
                                            else:
                                                standardDev = 1.31593382
                                        elif "Assists" in tempStat:
                                            if float(tempLine) > 1:
                                                standardDev = 1.229844158
                                            else:
                                                standardDev = 0.921717056
                                        elif "FGM" in tempStat or "FG Made" in tempStat:
                                            if float(tempLine) > 2.25:
                                                standardDev = 1.215739272
                                            else:
                                                standardDev = 0.944780645
                                        elif "FGA" in tempStat or "FG Attempted" in tempStat:
                                            if float(tempLine) > 2.25:
                                                standardDev = 1.25154058
                                            else:
                                                standardDev = 1.017422425
                                        elif "XPM" in tempStat or "XP Made" in tempStat:
                                            if float(tempLine) > 1.75:
                                                standardDev = 1.339018503
                                            else:
                                                standardDev = 0.755928946
                                        elif "Kicking Points" in tempStat:
                                            if float(tempLine) > 8:
                                                standardDev = 4.022912319
                                            elif float(tempLine) > 5:
                                                standardDev = 3.833706693
                                            else:
                                                standardDev = 2.483277404
                                    if dfs == "Underdog":
                                        if float(dfs_oldLines[j]) < float(sportsbook_oldLines[i]):
                                            discrepancies.append(discrepancy)
                                            if "PrizePicks" in sportsbook:
                                                if "Higher" in str((dfs_higherOrLowers)[j]):
                                                    overPrices.append(1.817)
                                                    underPrices.append(1.817)
                                                    middleProbability = calculate_probability(float(middle) - float(discrepancy), float(sportsbook_oldLines[i]), float(standardDev)) - calculate_probability(float(middle), float(sportsbook_oldLines[i]), float(standardDev))
                                                    if (sport == "NBA" or sport == "OBBALL" or sport == "WNBA") and (float(discrepancy) < 2) and ("Points" in sportsbook_newStats[i]):
                                                        overPercent = 0.5 + middleProbability / 2
                                                        underPercent = 0.5 - middleProbability / 2
                                                        overPercentages.append(overPercent)
                                                        underPercentages.append(underPercent)
                                                    elif "Pitching Outs" in sportsbook_newStats[i]:
                                                        overPercent = 0.5 + middleProbability / 4
                                                        underPercent = 0.5 - middleProbability / 4
                                                        overPercentages.append(overPercent)
                                                        underPercentages.append(underPercent)
                                                    elif "Strikeouts" in sportsbook_newStats[i] and "Batter" not in sportsbook_newStats[i] and "Hitter" not in sportsbook_newStats[i]:
                                                        overPercent = 0.5 + middleProbability / 4
                                                        underPercent = 0.5 - middleProbability / 4
                                                        overPercentages.append(overPercent)
                                                        underPercentages.append(underPercent)
                                                    elif float(discrepancy) == 0.5 or float(discrepancy) == -0.5 or float(discrepancy) == -0.25 or float(discrepancy) == 0.25:
                                                        overPercent = 0.5 + middleProbability / 4
                                                        underPercent = 0.5 - middleProbability / 4
                                                        overPercentages.append(overPercent)
                                                        underPercentages.append(underPercent)
                                                    else:
                                                        overPercent = 0.5 + middleProbability / 1.5
                                                        underPercent = 0.5 - middleProbability / 1.5
                                                        overPercentages.append(overPercent)
                                                        underPercentages.append(underPercent)
                                                    try:
                                                        value = round(((((overPercent) * float(multiplier)) ** 3) * 6 - 1) * 100, 1)
                                                    except ValueError:
                                                        multiplier = 1
                                                        value = round(((((overPercent) * float(multiplier)) ** 3) * 6 - 1) * 100, 1)
                                                    evs.append(float(value))
                                                    higherOrLowers.append("Higher")
                                                elif "Lower" in str((dfs_higherOrLowers)[j]):
                                                    overPrices.append(1.817)
                                                    underPrices.append(1.817)
                                                    middleProbability = calculate_probability(float(middle) - float(discrepancy), float(sportsbook_oldLines[i]), float(standardDev)) - calculate_probability(float(middle), float(sportsbook_oldLines[i]), float(standardDev))
                                                    if (sport == "NBA" or sport == "OBBALL" or sport == "WNBA") and (float(discrepancy) < 2) and ("Points" in sportsbook_newStats[i]):
                                                        overPercent = 0.5 + middleProbability * 2
                                                        underPercent = 0.5 - middleProbability * 2
                                                        overPercentages.append(overPercent)
                                                        underPercentages.append(underPercent)
                                                    elif "Pitching Outs" in sportsbook_newStats[i]:
                                                        overPercent = 0.5 + middleProbability * 4
                                                        underPercent = 0.5 - middleProbability * 4
                                                        overPercentages.append(overPercent)
                                                        underPercentages.append(underPercent)
                                                    elif "Strikeouts" in sportsbook_newStats[i] and "Batter" not in sportsbook_newStats[i] and "Hitter" not in sportsbook_newStats[i]:
                                                        overPercent = 0.5 + middleProbability * 2
                                                        underPercent = 0.5 - middleProbability * 2
                                                        overPercentages.append(overPercent)
                                                        underPercentages.append(underPercent)
                                                    elif float(discrepancy) == 0.5 or float(discrepancy) == -0.5 or float(discrepancy) == -0.25 or float(discrepancy) == 0.25:
                                                        overPercent = 0.5 + middleProbability * 4
                                                        underPercent = 0.5 - middleProbability * 4
                                                        overPercentages.append(overPercent)
                                                        underPercentages.append(underPercent)
                                                    else:
                                                        overPercent = 0.5 + middleProbability * 1.5
                                                        underPercent = 0.5 - middleProbability * 1.5
                                                        overPercentages.append(overPercent)
                                                        underPercentages.append(underPercent)
                                                    try:
                                                        value = round(((((underPercent) * float(multiplier)) ** 3) * 6 - 1) * 100, 1)
                                                    except ValueError:
                                                        multiplier = 1
                                                        value = round(((((underPercent) * float(multiplier)) ** 3) * 6 - 1) * 100, 1)
                                                    evs.append(float(value))
                                                    higherOrLowers.append("Lower")
                                                else:
                                                    overPrices.append(1.817)
                                                    underPrices.append(1.817)
                                                    middleProbability = calculate_probability(float(middle) - float(discrepancy), float(sportsbook_oldLines[i]), float(standardDev)) - calculate_probability(float(middle), float(sportsbook_oldLines[i]), float(standardDev))
                                                    if (sport == "NBA" or sport == "OBBALL" or sport == "WNBA") and (float(discrepancy) < 2) and ("Points" in sportsbook_newStats[i]):
                                                        overPercent = 0.5 + middleProbability / 2
                                                        underPercent = 0.5 - middleProbability / 2
                                                        overPercentages.append(overPercent)
                                                        underPercentages.append(underPercent)
                                                    elif "Pitching Outs" in sportsbook_newStats[i]:
                                                        overPercent = 0.5 + middleProbability / 4
                                                        underPercent = 0.5 - middleProbability / 4
                                                        overPercentages.append(overPercent)
                                                        underPercentages.append(underPercent)
                                                    elif float(discrepancy) == 0.5 or float(discrepancy) == -0.5 or float(discrepancy) == -0.25 or float(discrepancy) == 0.25:
                                                        overPercent = 0.5 + middleProbability / 4
                                                        underPercent = 0.5 - middleProbability / 4
                                                        overPercentages.append(overPercent)
                                                        underPercentages.append(underPercent)                                       
                                                    else:
                                                        overPercent = 0.5 + middleProbability / 1.5
                                                        underPercent = 0.5 - middleProbability / 1.5
                                                        overPercentages.append(overPercent)
                                                        underPercentages.append(underPercent)
                                                    try:
                                                        value = round(((((overPercent) * float(multiplier)) ** 3) * 6 - 1) * 100, 1)
                                                    except ValueError:
                                                        multiplier = 1
                                                        value = round(((((overPercent) * float(multiplier)) ** 3) * 6 - 1) * 100, 1)
                                                    evs.append(float(value))
                                                    higherOrLowers.append("Higher")
                                            elif "Pinnacle" in sportsbook or "DraftKings" in sportsbook:
                                                if "Higher" in str((dfs_higherOrLowers)[j]):
                                                    sportsbook_overPercentages = sportsbook_df["% Over"].values.tolist()
                                                    sportsbook_underPercentages = sportsbook_df["% Under"].values.tolist()
                                                    sportsbook_overPrices = sportsbook_df["Over Price"].values.tolist()
                                                    sportsbook_underPrices = sportsbook_df["Under Price"].values.tolist()
                                                    overPrices.append(sportsbook_overPrices[i])
                                                    underPrices.append(sportsbook_underPrices[i])
                                                    middleProbability = calculate_probability(float(middle) - float(discrepancy), float(sportsbook_oldLines[i]), float(standardDev)) - calculate_probability(float(middle), float(sportsbook_oldLines[i]), float(standardDev))
                                                    if (sport == "NBA" or sport == "OBBALL" or sport == "WNBA") and (float(discrepancy) < 2) and ("Points" in sportsbook_newStats[i]):
                                                        overPercent = sportsbook_overPercentages[i] + middleProbability / 2
                                                        underPercent = sportsbook_underPercentages[i] - middleProbability / 2
                                                        overPercentages.append(overPercent)
                                                        underPercentages.append(underPercent)
                                                    elif "Pitching Outs" in sportsbook_newStats[i]:
                                                        overPercent = sportsbook_overPercentages[i] + middleProbability / 10
                                                        underPercent = sportsbook_underPercentages[i] - middleProbability / 10
                                                        overPercentages.append(overPercent)
                                                        underPercentages.append(underPercent)
                                                    elif "Strikeouts" in sportsbook_newStats[i] and "Batter" not in sportsbook_newStats[i] and "Hitter" not in sportsbook_newStats[i]:
                                                        overPercent = sportsbook_overPercentages[i] + middleProbability / 4
                                                        underPercent = sportsbook_underPercentages[i] - middleProbability / 4
                                                        overPercentages.append(overPercent)
                                                        underPercentages.append(underPercent)
                                                    elif float(discrepancy) == 0.5 or float(discrepancy) == -0.5 or float(discrepancy) == -0.25 or float(discrepancy) == 0.25:
                                                        overPercent = sportsbook_overPercentages[i] + middleProbability / 4
                                                        underPercent = sportsbook_underPercentages[i] - middleProbability / 4
                                                        overPercentages.append(overPercent)
                                                        underPercentages.append(underPercent)
                                                    else:
                                                        overPercent = sportsbook_overPercentages[i] + middleProbability / 1.5
                                                        underPercent = sportsbook_underPercentages[i] - middleProbability / 1.5
                                                        overPercentages.append(overPercent)
                                                        underPercentages.append(underPercent)
                                                    try:
                                                        value = round(((((overPercent) * float(multiplier)) ** 3) * 6 - 1) * 100, 1)
                                                    except ValueError:
                                                        multiplier = 1
                                                        value = round(((((overPercent) * float(multiplier)) ** 3) * 6 - 1) * 100, 1)
                                                    evs.append(float(value))
                                                    higherOrLowers.append("Higher")
                                                elif "Lower" in str((dfs_higherOrLowers)[j]):
                                                    sportsbook_overPercentages = sportsbook_df["% Over"].values.tolist()
                                                    sportsbook_underPercentages = sportsbook_df["% Under"].values.tolist()
                                                    sportsbook_overPrices = sportsbook_df["Over Price"].values.tolist()
                                                    sportsbook_underPrices = sportsbook_df["Under Price"].values.tolist()
                                                    overPrices.append(sportsbook_overPrices[i])
                                                    underPrices.append(sportsbook_underPrices[i])
                                                    middleProbability = calculate_probability(float(middle) - float(discrepancy), float(sportsbook_oldLines[i]), float(standardDev)) - calculate_probability(float(middle), float(sportsbook_oldLines[i]), float(standardDev))
                                                    if (sport == "NBA" or sport == "OBBALL" or sport == "WNBA") and (float(discrepancy) < 2) and ("Points" in sportsbook_newStats[i]):
                                                        overPercent = sportsbook_overPercentages[i] + middleProbability * 2
                                                        underPercent = sportsbook_underPercentages[i] - middleProbability * 2
                                                        overPercentages.append(overPercent)
                                                        underPercentages.append(underPercent)
                                                    elif "Pitching Outs" in sportsbook_newStats[i]:
                                                        overPercent = sportsbook_overPercentages[i] + middleProbability * 10
                                                        underPercent = sportsbook_underPercentages[i] - middleProbability * 10
                                                        overPercentages.append(overPercent)
                                                        underPercentages.append(underPercent)
                                                    elif "Strikeouts" in sportsbook_newStats[i] and "Batter" not in sportsbook_newStats[i] and "Hitter" not in sportsbook_newStats[i]:
                                                        overPercent = sportsbook_overPercentages[i] + middleProbability * 2
                                                        underPercent = sportsbook_underPercentages[i] - middleProbability * 2
                                                        overPercentages.append(overPercent)
                                                        underPercentages.append(underPercent)
                                                    elif float(discrepancy) == 0.5 or float(discrepancy) == -0.5 or float(discrepancy) == -0.25 or float(discrepancy) == 0.25:
                                                        overPercent = sportsbook_overPercentages[i] + middleProbability * 4
                                                        underPercent = sportsbook_underPercentages[i] - middleProbability * 4
                                                        overPercentages.append(overPercent)
                                                        underPercentages.append(underPercent)
                                                    else:
                                                        overPercent = sportsbook_overPercentages[i] + middleProbability * 1.5
                                                        underPercent = sportsbook_underPercentages[i] - middleProbability * 1.5
                                                        overPercentages.append(overPercent)
                                                        underPercentages.append(underPercent)
                                                    try:
                                                        value = round(((((underPercent) * float(multiplier)) ** 3) * 6 - 1) * 100, 1)
                                                    except ValueError:
                                                        multiplier = 1
                                                        value = round(((((underPercent) * float(multiplier)) ** 3) * 6 - 1) * 100, 1)
                                                    evs.append(float(value))
                                                    higherOrLowers.append("Lower")
                                                else:
                                                    sportsbook_overPercentages = sportsbook_df["% Over"].values.tolist()
                                                    sportsbook_underPercentages = sportsbook_df["% Under"].values.tolist()
                                                    sportsbook_overPrices = sportsbook_df["Over Price"].values.tolist()
                                                    sportsbook_underPrices = sportsbook_df["Under Price"].values.tolist()
                                                    overPrices.append(sportsbook_overPrices[i])
                                                    underPrices.append(sportsbook_underPrices[i])
                                                    middleProbability = calculate_probability(float(middle) - float(discrepancy), float(sportsbook_oldLines[i]), float(standardDev)) - calculate_probability(float(middle), float(sportsbook_oldLines[i]), float(standardDev))
                                                    if (sport == "NBA" or sport == "OBBALL" or sport == "WNBA") and (float(discrepancy) < 2) and ("Points" in sportsbook_newStats[i]):
                                                        overPercent = sportsbook_overPercentages[i] + middleProbability / 2
                                                        underPercent = sportsbook_underPercentages[i] - middleProbability / 2
                                                        overPercentages.append(overPercent)
                                                        underPercentages.append(underPercent)
                                                    elif "Pitching Outs" in sportsbook_newStats[i]:
                                                        overPercent = sportsbook_overPercentages[i] + middleProbability / 10
                                                        underPercent = sportsbook_underPercentages[i] - middleProbability / 10
                                                        overPercentages.append(overPercent)
                                                        underPercentages.append(underPercent)
                                                    elif float(discrepancy) == 0.5 or float(discrepancy) == -0.5 or float(discrepancy) == -0.25 or float(discrepancy) == 0.25:
                                                        overPercent = sportsbook_overPercentages[i] + middleProbability / 4
                                                        underPercent = sportsbook_underPercentages[i] - middleProbability / 4
                                                        overPercentages.append(overPercent)
                                                        underPercentages.append(underPercent)
                                                    else:
                                                        overPercent = sportsbook_overPercentages[i] + middleProbability / 1.5
                                                        underPercent = sportsbook_underPercentages[i] - middleProbability / 1.5
                                                        overPercentages.append(overPercent)
                                                        underPercentages.append(underPercent)
                                                    try:
                                                        value = round(((((overPercent) * float(multiplier)) ** 3) * 6 - 1) * 100, 1)
                                                    except ValueError:
                                                        multiplier = 1
                                                        value = round(((((overPercent) * float(multiplier)) ** 3) * 6 - 1) * 100, 1)
                                                    evs.append(float(value))
                                                    higherOrLowers.append("Higher")
                                                    overPrices.append(sportsbook_overPrices[i])
                                                    underPrices.append(sportsbook_underPrices[i])
                                                    middleProbability = calculate_probability(float(middle) - float(discrepancy), float(sportsbook_oldLines[i]), float(standardDev)) - calculate_probability(float(middle), float(sportsbook_oldLines[i]), float(standardDev))
                                                    if (sport == "NBA" or sport == "OBBALL" or sport == "WNBA") and (float(discrepancy) < 2) and ("Points" in sportsbook_newStats[i]):
                                                        overPercent = sportsbook_overPercentages[i] + middleProbability * 2
                                                        underPercent = sportsbook_underPercentages[i] - middleProbability * 2
                                                        overPercentages.append(overPercent)
                                                        underPercentages.append(underPercent)
                                                    elif "Pitching Outs" in sportsbook_newStats[i]:
                                                        overPercent = sportsbook_overPercentages[i] + middleProbability * 10
                                                        underPercent = sportsbook_underPercentages[i] - middleProbability * 10
                                                        overPercentages.append(overPercent)
                                                        underPercentages.append(underPercent)
                                                    elif float(discrepancy) == 0.5 or float(discrepancy) == -0.5 or float(discrepancy) == -0.25 or float(discrepancy) == 0.25:
                                                        overPercent = sportsbook_overPercentages[i] + middleProbability * 4
                                                        underPercent = sportsbook_underPercentages[i] - middleProbability * 4
                                                        overPercentages.append(overPercent)
                                                        underPercentages.append(underPercent)
                                                    else:
                                                        overPercent = sportsbook_overPercentages[i] + middleProbability * 1.5
                                                        underPercent = sportsbook_underPercentages[i] - middleProbability * 1.5
                                                        overPercentages.append(overPercent)
                                                        underPercentages.append(underPercent)
                                                    try:
                                                        value = round(((((underPercent) * float(multiplier)) ** 3) * 6 - 1) * 100, 1)
                                                    except ValueError:
                                                        multiplier = 1
                                                        value = round(((((underPercent) * float(multiplier)) ** 3) * 6 - 1) * 100, 1)
                                                    evs.append(float(value))
                                                    higherOrLowers.append("Lower")
                                                    names.append(sportsbook_names[i])
                                                    stats.append(sportsbook_newStats[i])
                                                    sportsbooks.append(sportsbook)
                                                    sportsbook_lines.append(sportsbook_oldLines[i])
                                                    dfs_lines.append(dfs_oldLines[j])
                                                    times.append(dfs_times[j])
                                                    try:
                                                        payouts.append(dfs_payouts[j])
                                                    except UnboundLocalError:
                                                        payouts.append("1x")
                                                    discrepancies.append(discrepancy)
                                            names.append(sportsbook_names[i])
                                            stats.append(sportsbook_newStats[i])
                                            sportsbooks.append(sportsbook)
                                            sportsbook_lines.append(sportsbook_oldLines[i])
                                            dfs_lines.append(dfs_oldLines[j])
                                            times.append(dfs_times[j])
                                            try:
                                                payouts.append(dfs_payouts[j])
                                            except UnboundLocalError:
                                                payouts.append("1x")
                                        elif float(dfs_oldLines[j]) > float(sportsbook_oldLines[i]):
                                            discrepancies.append(discrepancy)
                                            if "PrizePicks" in sportsbook:
                                                if "Higher" in str((dfs_higherOrLowers)[j]):
                                                    overPrices.append(1.817)
                                                    underPrices.append(1.817)
                                                    middleProbability = calculate_probability(float(middle) - float(discrepancy), float(sportsbook_oldLines[i]), float(standardDev)) - calculate_probability(float(middle), float(sportsbook_oldLines[i]), float(standardDev))
                                                    if (sport == "NBA" or sport == "OBBALL" or sport == "WNBA") and (float(discrepancy) < 2) and ("Points" in sportsbook_newStats[i]):
                                                        overPercent = 0.5 + middleProbability * 2
                                                        underPercent = 0.5 - middleProbability * 2
                                                        overPercentages.append(overPercent)
                                                        underPercentages.append(underPercent)
                                                    elif "Pitching Outs" in sportsbook_newStats[i]:
                                                        overPercent = 0.5 + middleProbability * 4
                                                        underPercent = 0.5 - middleProbability * 4
                                                        overPercentages.append(overPercent)
                                                        underPercentages.append(underPercent)
                                                    elif "Strikeouts" in sportsbook_newStats[i] and "Batter" not in sportsbook_newStats[i] and "Hitter" not in sportsbook_newStats[i]:
                                                        overPercent = 0.5 + middleProbability * 2
                                                        underPercent = 0.5 - middleProbability * 2
                                                        overPercentages.append(overPercent)
                                                        underPercentages.append(underPercent)
                                                    elif float(discrepancy) == 0.5 or float(discrepancy) == -0.5 or float(discrepancy) == -0.25 or float(discrepancy) == 0.25:
                                                        overPercent = 0.5 + middleProbability * 4
                                                        underPercent = 0.5 - middleProbability * 4
                                                        overPercentages.append(overPercent)
                                                        underPercentages.append(underPercent)
                                                    else:
                                                        overPercent = 0.5 + middleProbability * 1.5
                                                        underPercent = 0.5 - middleProbability * 1.5
                                                        overPercentages.append(overPercent)
                                                        underPercentages.append(underPercent)
                                                    try:
                                                        value = round(((((overPercent) * float(multiplier)) ** 3) * 6 - 1) * 100, 1)
                                                    except ValueError:
                                                        multiplier = 1
                                                        value = round(((((overPercent) * float(multiplier)) ** 3) * 6 - 1) * 100, 1)
                                                    evs.append(float(value))
                                                    higherOrLowers.append("Higher")
                                                elif "Lower" in str((dfs_higherOrLowers)[j]):
                                                    overPrices.append(1.817)
                                                    underPrices.append(1.817)
                                                    middleProbability = calculate_probability(float(middle) - float(discrepancy), float(sportsbook_oldLines[i]), float(standardDev)) - calculate_probability(float(middle), float(sportsbook_oldLines[i]), float(standardDev))
                                                    if (sport == "NBA" or sport == "OBBALL" or sport == "WNBA") and (float(discrepancy) < 2) and ("Points" in sportsbook_newStats[i]):
                                                        overPercent = 0.5 + middleProbability / 2
                                                        underPercent = 0.5 - middleProbability / 2
                                                        overPercentages.append(overPercent)
                                                        underPercentages.append(underPercent)
                                                    elif "Pitching Outs" in sportsbook_newStats[i]:
                                                        overPercent = 0.5 + middleProbability / 4
                                                        underPercent = 0.5 - middleProbability / 4
                                                        overPercentages.append(overPercent)
                                                        underPercentages.append(underPercent)
                                                    elif "Strikeouts" in sportsbook_newStats[i] and "Batter" not in sportsbook_newStats[i] and "Hitter" not in sportsbook_newStats[i]:
                                                        overPercent = 0.5 + middleProbability / 4
                                                        underPercent = 0.5 - middleProbability / 4
                                                        overPercentages.append(overPercent)
                                                        underPercentages.append(underPercent)
                                                    elif float(discrepancy) == 0.5 or float(discrepancy) == -0.5 or float(discrepancy) == -0.25 or float(discrepancy) == 0.25:
                                                        overPercent = 0.5 + middleProbability / 4
                                                        underPercent = 0.5 - middleProbability / 4
                                                        overPercentages.append(overPercent)
                                                        underPercentages.append(underPercent)
                                                    else:
                                                        overPercent = 0.5 + middleProbability / 1.5
                                                        underPercent = 0.5 - middleProbability / 1.5
                                                        overPercentages.append(overPercent)
                                                        underPercentages.append(underPercent)
                                                    try:
                                                        value = round(((((underPercent) * float(multiplier)) ** 3) * 6 - 1) * 100, 1)
                                                    except ValueError:
                                                        multiplier = 1
                                                        value = round(((((underPercent) * float(multiplier)) ** 3) * 6 - 1) * 100, 1)
                                                    evs.append(float(value))
                                                    higherOrLowers.append("Lower")
                                                else:
                                                    overPrices.append(1.817)
                                                    underPrices.append(1.817)
                                                    middleProbability = calculate_probability(float(middle) - float(discrepancy), float(sportsbook_oldLines[i]), float(standardDev)) - calculate_probability(float(middle), float(sportsbook_oldLines[i]), float(standardDev))
                                                    if (sport == "NBA" or sport == "OBBALL" or sport == "WNBA") and (float(discrepancy) < 2) and ("Points" in sportsbook_newStats[i]):
                                                        overPercent = 0.5 + middleProbability / 2
                                                        underPercent = 0.5 - middleProbability / 2
                                                        overPercentages.append(overPercent)
                                                        underPercentages.append(underPercent)
                                                    elif "Pitching Outs" in sportsbook_newStats[i]:
                                                        overPercent = 0.5 + middleProbability / 4
                                                        underPercent = 0.5 - middleProbability / 4
                                                        overPercentages.append(overPercent)
                                                        underPercentages.append(underPercent)
                                                    elif float(discrepancy) == 0.5 or float(discrepancy) == -0.5 or float(discrepancy) == -0.25 or float(discrepancy) == 0.25:
                                                        overPercent = 0.5 + middleProbability / 4
                                                        underPercent = 0.5 - middleProbability / 4
                                                        overPercentages.append(overPercent)
                                                        underPercentages.append(underPercent)
                                                    else:
                                                        overPercent = 0.5 + middleProbability / 1.5
                                                        underPercent = 0.5 - middleProbability / 1.5
                                                        overPercentages.append(overPercent)
                                                        underPercentages.append(underPercent)
                                                    try:
                                                        value = round(((((underPercent) * float(multiplier)) ** 3) * 6 - 1) * 100, 1)
                                                    except ValueError:
                                                        multiplier = 1
                                                        value = round(((((underPercent) * float(multiplier)) ** 3) * 6 - 1) * 100, 1)
                                                    evs.append(float(value))
                                                    higherOrLowers.append("Lower")
                                            elif "Pinnacle" in sportsbook or "DraftKings" in sportsbook:
                                                if "Higher" in str((dfs_higherOrLowers)[j]):
                                                    sportsbook_overPercentages = sportsbook_df["% Over"].values.tolist()
                                                    sportsbook_underPercentages = sportsbook_df["% Under"].values.tolist()
                                                    sportsbook_overPrices = sportsbook_df["Over Price"].values.tolist()
                                                    sportsbook_underPrices = sportsbook_df["Under Price"].values.tolist()
                                                    overPrices.append(sportsbook_overPrices[i])
                                                    underPrices.append(sportsbook_underPrices[i])
                                                    middleProbability = calculate_probability(float(middle) - float(discrepancy), float(sportsbook_oldLines[i]), float(standardDev)) - calculate_probability(float(middle), float(sportsbook_oldLines[i]), float(standardDev))
                                                    if (sport == "NBA" or sport == "OBBALL" or sport == "WNBA") and (float(discrepancy) < 2) and ("Points" in sportsbook_newStats[i]):
                                                        overPercent = sportsbook_overPercentages[i] + middleProbability * 2
                                                        underPercent = sportsbook_underPercentages[i] - middleProbability * 2
                                                        overPercentages.append(overPercent)
                                                        underPercentages.append(underPercent)
                                                    elif "Pitching Outs" in sportsbook_newStats[i]:
                                                        overPercent = sportsbook_overPercentages[i] + middleProbability * 10
                                                        underPercent = sportsbook_underPercentages[i] - middleProbability * 10
                                                        overPercentages.append(overPercent)
                                                        underPercentages.append(underPercent)
                                                    elif "Strikeouts" in sportsbook_newStats[i] and "Batter" not in sportsbook_newStats[i] and "Hitter" not in sportsbook_newStats[i]:
                                                        overPercent = sportsbook_overPercentages[i] + middleProbability * 2
                                                        underPercent = sportsbook_underPercentages[i] - middleProbability * 2
                                                        overPercentages.append(overPercent)
                                                        underPercentages.append(underPercent)
                                                    elif float(discrepancy) == 0.5 or float(discrepancy) == -0.5 or float(discrepancy) == -0.25 or float(discrepancy) == 0.25:
                                                        overPercent = sportsbook_overPercentages[i] + middleProbability * 4
                                                        underPercent = sportsbook_underPercentages[i] - middleProbability * 4
                                                        overPercentages.append(overPercent)
                                                        underPercentages.append(underPercent)
                                                    else:
                                                        overPercent = sportsbook_overPercentages[i] + middleProbability * 1.5
                                                        underPercent = sportsbook_underPercentages[i] - middleProbability * 1.5
                                                        overPercentages.append(overPercent)
                                                        underPercentages.append(underPercent)
                                                    try:
                                                        value = round(((((overPercent) * float(multiplier)) ** 3) * 6 - 1) * 100, 1)
                                                    except ValueError:
                                                        multiplier = 1
                                                        value = round(((((overPercent) * float(multiplier)) ** 3) * 6 - 1) * 100, 1)
                                                    evs.append(float(value))
                                                    higherOrLowers.append("Higher")
                                                elif "Lower" in str((dfs_higherOrLowers)[j]):
                                                    sportsbook_overPercentages = sportsbook_df["% Over"].values.tolist()
                                                    sportsbook_underPercentages = sportsbook_df["% Under"].values.tolist()
                                                    sportsbook_overPrices = sportsbook_df["Over Price"].values.tolist()
                                                    sportsbook_underPrices = sportsbook_df["Under Price"].values.tolist()
                                                    overPrices.append(sportsbook_overPrices[i])
                                                    underPrices.append(sportsbook_underPrices[i])
                                                    middleProbability = calculate_probability(float(middle) - float(discrepancy), float(sportsbook_oldLines[i]), float(standardDev)) - calculate_probability(float(middle), float(sportsbook_oldLines[i]), float(standardDev))
                                                    if (sport == "NBA" or sport == "OBBALL" or sport == "WNBA") and (float(discrepancy) < 2) and ("Points" in sportsbook_newStats[i]):
                                                        overPercent = sportsbook_overPercentages[i] + middleProbability / 2
                                                        underPercent = sportsbook_underPercentages[i] - middleProbability / 2
                                                        overPercentages.append(overPercent)
                                                        underPercentages.append(underPercent)
                                                    elif "Pitching Outs" in sportsbook_newStats[i]:
                                                        overPercent = sportsbook_overPercentages[i] + middleProbability / 10
                                                        underPercent = sportsbook_underPercentages[i] - middleProbability / 10
                                                        overPercentages.append(overPercent)
                                                        underPercentages.append(underPercent)
                                                    elif "Strikeouts" in sportsbook_newStats[i] and "Batter" not in sportsbook_newStats[i] and "Hitter" not in sportsbook_newStats[i]:
                                                        overPercent = sportsbook_overPercentages[i] + middleProbability / 4
                                                        underPercent = sportsbook_underPercentages[i] - middleProbability / 4
                                                        overPercentages.append(overPercent)
                                                        underPercentages.append(underPercent)
                                                    elif float(discrepancy) == 0.5 or float(discrepancy) == -0.5 or float(discrepancy) == -0.25 or float(discrepancy) == 0.25:
                                                        overPercent = sportsbook_overPercentages[i] + middleProbability / 4
                                                        underPercent = sportsbook_underPercentages[i] - middleProbability / 4
                                                        overPercentages.append(overPercent)
                                                        underPercentages.append(underPercent)
                                                    else:
                                                        overPercent = sportsbook_overPercentages[i] + middleProbability / 1.5
                                                        underPercent = sportsbook_underPercentages[i] - middleProbability / 1.5
                                                        overPercentages.append(overPercent)
                                                        underPercentages.append(underPercent)
                                                    try:
                                                        value = round(((((underPercent) * float(multiplier)) ** 3) * 6 - 1) * 100, 1)
                                                    except ValueError:
                                                        multiplier = 1
                                                        value = round(((((underPercent) * float(multiplier)) ** 3) * 6 - 1) * 100, 1)
                                                    evs.append(float(value))
                                                    higherOrLowers.append("Lower")
                                                else:
                                                    sportsbook_overPercentages = sportsbook_df["% Over"].values.tolist()
                                                    sportsbook_underPercentages = sportsbook_df["% Under"].values.tolist()
                                                    sportsbook_overPrices = sportsbook_df["Over Price"].values.tolist()
                                                    sportsbook_underPrices = sportsbook_df["Under Price"].values.tolist()
                                                    overPrices.append(sportsbook_overPrices[i])
                                                    underPrices.append(sportsbook_underPrices[i])
                                                    middleProbability = calculate_probability(float(middle) - float(discrepancy), float(sportsbook_oldLines[i]), float(standardDev)) - calculate_probability(float(middle), float(sportsbook_oldLines[i]), float(standardDev))
                                                    if (sport == "NBA" or sport == "OBBALL" or sport == "WNBA") and (float(discrepancy) < 2) and ("Points" in sportsbook_newStats[i]):
                                                        overPercent = sportsbook_overPercentages[i] + middleProbability * 2
                                                        underPercent = sportsbook_underPercentages[i] - middleProbability * 2
                                                        overPercentages.append(overPercent)
                                                        underPercentages.append(underPercent)
                                                    elif "Pitching Outs" in sportsbook_newStats[i]:
                                                        overPercent = sportsbook_overPercentages[i] + middleProbability * 10
                                                        underPercent = sportsbook_underPercentages[i] - middleProbability * 10
                                                        overPercentages.append(overPercent)
                                                        underPercentages.append(underPercent)
                                                    elif float(discrepancy) == 0.5 or float(discrepancy) == -0.5 or float(discrepancy) == -0.25 or float(discrepancy) == 0.25:
                                                        overPercent = sportsbook_overPercentages[i] + middleProbability * 4
                                                        underPercent = sportsbook_underPercentages[i] - middleProbability * 4
                                                        overPercentages.append(overPercent)
                                                        underPercentages.append(underPercent)
                                                    else:
                                                        overPercent = sportsbook_overPercentages[i] + middleProbability * 1.5
                                                        underPercent = sportsbook_underPercentages[i] - middleProbability * 1.5
                                                        overPercentages.append(overPercent)
                                                        underPercentages.append(underPercent)
                                                    try:
                                                        value = round(((((overPercent) * float(multiplier)) ** 3) * 6 - 1) * 100, 1)
                                                    except ValueError:
                                                        multiplier = 1
                                                        value = round(((((overPercent) * float(multiplier)) ** 3) * 6 - 1) * 100, 1)
                                                    evs.append(float(value))
                                                    higherOrLowers.append("Higher")
                                                    overPrices.append(sportsbook_overPrices[i])
                                                    underPrices.append(sportsbook_underPrices[i])
                                                    middleProbability = calculate_probability(float(middle) - float(discrepancy), float(sportsbook_oldLines[i]), float(standardDev)) - calculate_probability(float(middle), float(sportsbook_oldLines[i]), float(standardDev))
                                                    if (sport == "NBA" or sport == "OBBALL" or sport == "WNBA") and (float(discrepancy) < 2) and ("Points" in sportsbook_newStats[i]):
                                                        overPercent = sportsbook_overPercentages[i] + middleProbability / 2
                                                        underPercent = sportsbook_underPercentages[i] - middleProbability / 2
                                                        overPercentages.append(overPercent)
                                                        underPercentages.append(underPercent)
                                                    elif "Pitching Outs" in sportsbook_newStats[i]:
                                                        overPercent = sportsbook_overPercentages[i] + middleProbability / 10
                                                        underPercent = sportsbook_underPercentages[i] - middleProbability / 10
                                                        overPercentages.append(overPercent)
                                                        underPercentages.append(underPercent)
                                                    elif float(discrepancy) == 0.5 or float(discrepancy) == -0.5 or float(discrepancy) == -0.25 or float(discrepancy) == 0.25:
                                                        overPercent = sportsbook_overPercentages[i] + middleProbability / 4
                                                        underPercent = sportsbook_underPercentages[i] - middleProbability / 4
                                                        overPercentages.append(overPercent)
                                                        underPercentages.append(underPercent)
                                                    else:
                                                        overPercent = sportsbook_overPercentages[i] + middleProbability / 1.5
                                                        underPercent = sportsbook_underPercentages[i] - middleProbability / 1.5
                                                        overPercentages.append(overPercent)
                                                        underPercentages.append(underPercent)
                                                    try:
                                                        value = round(((((underPercent) * float(multiplier)) ** 3) * 6 - 1) * 100, 1)
                                                    except ValueError:
                                                        multiplier = 1
                                                        value = round(((((underPercent) * float(multiplier)) ** 3) * 6 - 1) * 100, 1)
                                                    evs.append(float(value))
                                                    higherOrLowers.append("Lower")
                                                    names.append(sportsbook_names[i])
                                                    stats.append(sportsbook_newStats[i])
                                                    sportsbooks.append(sportsbook)
                                                    sportsbook_lines.append(sportsbook_oldLines[i])
                                                    dfs_lines.append(dfs_oldLines[j])
                                                    times.append(dfs_times[j])
                                                    try:
                                                        payouts.append(dfs_payouts[j])
                                                    except UnboundLocalError:
                                                        payouts.append("1x")
                                                    discrepancies.append(discrepancy)
                                            names.append(sportsbook_names[i])
                                            stats.append(sportsbook_newStats[i])
                                            sportsbooks.append(sportsbook)
                                            sportsbook_lines.append(sportsbook_oldLines[i])
                                            dfs_lines.append(dfs_oldLines[j])
                                            times.append(dfs_times[j])
                                            try:
                                                payouts.append(dfs_payouts[j])
                                            except UnboundLocalError:
                                                payouts.append("1x")
                                    elif dfs == "PrizePicks":
                                        sportsbook_multiplier = "1"
                                        try:
                                            if "x" in str(sportsbook_payouts[i]):
                                                sportsbook_multiplier = str(sportsbook_payouts[i])[:-1]
                                        except UnboundLocalError:
                                            pass
                                        if float(dfs_oldLines[j]) < float(sportsbook_oldLines[i]):
                                            discrepancies.append(discrepancy)
                                            if "Underdog" in sportsbook:
                                                if "Higher" in str(sportsbook_higherOrLowers[i]):
                                                    overPrices.append(1.817 * float(sportsbook_multiplier))
                                                    underPrices.append(1.817 / float(sportsbook_multiplier))
                                                    middleProbability = calculate_probability(float(middle) - float(discrepancy), float(sportsbook_oldLines[i]), float(standardDev)) - calculate_probability(float(middle), float(sportsbook_oldLines[i]), float(standardDev))
                                                    if (sport == "NBA" or sport == "OBBALL" or sport == "WNBA") and (float(discrepancy) < 2) and ("Points" in sportsbook_newStats[i]):
                                                        underPercent = (0.5 - middleProbability * 2) * float(sportsbook_multiplier)
                                                        overPercent = 1 - underPercent
                                                        overPercentages.append(overPercent)
                                                        underPercentages.append(underPercent)
                                                    elif "Pitching Outs" in sportsbook_newStats[i]:
                                                        underPercent = (0.5 - middleProbability * 4) * float(sportsbook_multiplier)
                                                        overPercent = 1 - underPercent
                                                        overPercentages.append(overPercent)
                                                        underPercentages.append(underPercent)
                                                    elif float(discrepancy) == 0.5 or float(discrepancy) == -0.5 or float(discrepancy) == -0.25 or float(discrepancy) == 0.25:
                                                        underPercent = (0.5 - middleProbability * 4) * float(sportsbook_multiplier)
                                                        overPercent = 1 - underPercent
                                                        overPercentages.append(overPercent)
                                                        underPercentages.append(underPercent)
                                                    else:
                                                        underPercent = (0.5 - middleProbability * 1.5) * float(sportsbook_multiplier)
                                                        overPercent = 1 - underPercent
                                                        overPercentages.append(overPercent)
                                                        underPercentages.append(underPercent)
                                                    try:
                                                        value = round(((((underPercent) * float(multiplier)) ** 3) * 6 - 1) * 100, 1)
                                                    except ValueError:
                                                        multiplier = 1
                                                        value = round(((((underPercent) * float(multiplier)) ** 3) * 6 - 1) * 100, 1)
                                                    evs.append(float(value))
                                                    higherOrLowers.append("Lower")
                                                elif "Lower" in str(sportsbook_higherOrLowers[i]):
                                                    overPrices.append(1.817 / float(sportsbook_multiplier))
                                                    underPrices.append(1.817 * float(sportsbook_multiplier))
                                                    middleProbability = calculate_probability(float(middle) - float(discrepancy), float(sportsbook_oldLines[i]), float(standardDev)) - calculate_probability(float(middle), float(sportsbook_oldLines[i]), float(standardDev))
                                                    if (sport == "NBA" or sport == "OBBALL" or sport == "WNBA") and (float(discrepancy) < 2) and ("Points" in sportsbook_newStats[i]):
                                                        underPercent = (0.5 - middleProbability / 2) / float(sportsbook_multiplier)
                                                        overPercent = 1 - underPercent
                                                        overPercentages.append(overPercent)
                                                        underPercentages.append(underPercent)
                                                    elif "Pitching Outs" in sportsbook_newStats[i]:
                                                        underPercent = (0.5 - middleProbability / 4) / float(sportsbook_multiplier)
                                                        overPercent = 1 - underPercent
                                                        overPercentages.append(overPercent)
                                                        underPercentages.append(underPercent)
                                                    elif float(discrepancy) == 0.5 or float(discrepancy) == -0.5 or float(discrepancy) == -0.25 or float(discrepancy) == 0.25:
                                                        underPercent = (0.5 - middleProbability / 4) / float(sportsbook_multiplier)
                                                        overPercent = 1 - underPercent
                                                        overPercentages.append(overPercent)
                                                        underPercentages.append(underPercent)
                                                    else:
                                                        underPercent = (0.5 - middleProbability / 1.5) / float(sportsbook_multiplier)
                                                        overPercent = 1 - underPercent
                                                        overPercentages.append(overPercent)
                                                        underPercentages.append(underPercent)
                                                    try:
                                                        value = round(((((overPercent) * float(multiplier)) ** 3) * 6 - 1) * 100, 1)
                                                    except ValueError:
                                                        multiplier = 1
                                                        value = round(((((overPercent) * float(multiplier)) ** 3) * 6 - 1) * 100, 1)
                                                    evs.append(float(value))
                                                    higherOrLowers.append("Higher")
                                                else:
                                                    overPrices.append(1.817)
                                                    underPrices.append(1.817)
                                                    middleProbability = calculate_probability(float(middle) - float(discrepancy), float(sportsbook_oldLines[i]), float(standardDev)) - calculate_probability(float(middle), float(sportsbook_oldLines[i]), float(standardDev))
                                                    if (sport == "NBA" or sport == "OBBALL" or sport == "WNBA") and (float(discrepancy) < 2) and ("Points" in sportsbook_newStats[i]):
                                                        underPercent = (0.5 - middleProbability / 2) * float(sportsbook_multiplier)
                                                        overPercent = 1 - underPercent
                                                        overPercentages.append(overPercent)
                                                        underPercentages.append(underPercent)
                                                    elif "Pitching Outs" in sportsbook_newStats[i]:
                                                        underPercent = (0.5 - middleProbability / 4) * float(sportsbook_multiplier)
                                                        overPercent = 1 - underPercent
                                                        overPercentages.append(overPercent)
                                                        underPercentages.append(underPercent)
                                                    elif float(discrepancy) == 0.5 or float(discrepancy) == -0.5 or float(discrepancy) == -0.25 or float(discrepancy) == 0.25:
                                                        underPercent = (0.5 - middleProbability / 4) * float(sportsbook_multiplier)
                                                        overPercent = 1 - underPercent
                                                        overPercentages.append(overPercent)
                                                        underPercentages.append(underPercent)
                                                    else:
                                                        underPercent = (0.5 - middleProbability / 1.5) * float(sportsbook_multiplier)
                                                        overPercent = 1 - underPercent
                                                        overPercentages.append(overPercent)
                                                        underPercentages.append(underPercent)
                                                    try:
                                                        value = round(((((overPercent) * float(multiplier)) ** 3) * 6 - 1) * 100, 1)
                                                    except ValueError:
                                                        multiplier = 1
                                                        value = round(((((overPercent) * float(multiplier)) ** 3) * 6 - 1) * 100, 1)
                                                    evs.append(float(value))
                                                    higherOrLowers.append("Higher")
                                            elif "Pinnacle" in sportsbook or "DraftKings" in sportsbook:
                                                sportsbook_overPercentages = sportsbook_df["% Over"].values.tolist()
                                                sportsbook_underPercentages = sportsbook_df["% Under"].values.tolist()
                                                sportsbook_overPrices = sportsbook_df["Over Price"].values.tolist()
                                                sportsbook_underPrices = sportsbook_df["Under Price"].values.tolist()
                                                overPrices.append(sportsbook_overPrices[i])
                                                underPrices.append(sportsbook_underPrices[i])
                                                middleProbability = calculate_probability(float(middle) - float(discrepancy), float(sportsbook_oldLines[i]), float(standardDev)) - calculate_probability(float(middle), float(sportsbook_oldLines[i]), float(standardDev))
                                                if (sport == "NBA" or sport == "OBBALL" or sport == "WNBA") and (float(discrepancy) < 2) and ("Points" in sportsbook_newStats[i]):
                                                    underPercent = (sportsbook_underPercentages[i] - middleProbability / 2) * float(sportsbook_multiplier)
                                                    overPercent = 1 - underPercent
                                                    overPercentages.append(overPercent)
                                                    underPercentages.append(underPercent)
                                                elif "Pitching Outs" in sportsbook_newStats[i]:
                                                    underPercent = (sportsbook_underPercentages[i] - middleProbability / 10) * float(sportsbook_multiplier)
                                                    overPercent = 1 - underPercent
                                                    overPercentages.append(overPercent)
                                                    underPercentages.append(underPercent)
                                                elif float(discrepancy) == 0.5 or float(discrepancy) == -0.5 or float(discrepancy) == -0.25 or float(discrepancy) == 0.25:
                                                    underPercent = (sportsbook_underPercentages[i] - middleProbability / 4) * float(sportsbook_multiplier)
                                                    overPercent = 1 - underPercent
                                                    overPercentages.append(overPercent)
                                                    underPercentages.append(underPercent)
                                                else:
                                                    underPercent = (sportsbook_underPercentages[i] - middleProbability / 1.5) * float(sportsbook_multiplier)
                                                    overPercent = 1 - underPercent
                                                    overPercentages.append(overPercent)
                                                    underPercentages.append(underPercent)
                                                try:
                                                    value = round(((((overPercent) * float(multiplier)) ** 3) * 6 - 1) * 100, 1)
                                                except ValueError:
                                                    multiplier = 1
                                                    value = round(((((overPercent) * float(multiplier)) ** 3) * 6 - 1) * 100, 1)
                                                evs.append(float(value))
                                                higherOrLowers.append("Higher")
                                            names.append(sportsbook_names[i])
                                            stats.append(sportsbook_newStats[i])
                                            sportsbooks.append(sportsbook)
                                            sportsbook_lines.append(sportsbook_oldLines[i])
                                            dfs_lines.append(dfs_oldLines[j])
                                            times.append(dfs_times[j])
                                            try:
                                                payouts.append(dfs_payouts[j])
                                            except UnboundLocalError:
                                                payouts.append("1x")
                                        elif float(dfs_oldLines[j]) > float(sportsbook_oldLines[i]):
                                            discrepancies.append(discrepancy)
                                            if "Underdog" in sportsbook:
                                                if "Higher" in str(sportsbook_higherOrLowers[i]):
                                                    overPrices.append(1.817 * float(sportsbook_multiplier))
                                                    underPrices.append(1.817 / float(sportsbook_multiplier))
                                                    middleProbability = calculate_probability(float(middle) - float(discrepancy), float(sportsbook_oldLines[i]), float(standardDev)) - calculate_probability(float(middle), float(sportsbook_oldLines[i]), float(standardDev))
                                                    if (sport == "NBA" or sport == "OBBALL" or sport == "WNBA") and (float(discrepancy) < 2) and ("Points" in sportsbook_newStats[i]):
                                                        underPercent = (0.5 - middleProbability / 2) * float(sportsbook_multiplier)
                                                        overPercent = 1 - underPercent
                                                        overPercentages.append(overPercent)
                                                        underPercentages.append(underPercent)
                                                    elif "Pitching Outs" in sportsbook_newStats[i]:
                                                        underPercent = (0.5 - middleProbability / 10) * float(sportsbook_multiplier)
                                                        overPercent = 1 - underPercent
                                                        overPercentages.append(overPercent)
                                                        underPercentages.append(underPercent)
                                                    elif float(discrepancy) == 0.5 or float(discrepancy) == -0.5 or float(discrepancy) == -0.25 or float(discrepancy) == 0.25:
                                                        underPercent = (0.5 - middleProbability / 4) * float(sportsbook_multiplier)
                                                        overPercent = 1 - underPercent
                                                        overPercentages.append(overPercent)
                                                        underPercentages.append(underPercent)
                                                    else:
                                                        underPercent = (0.5 - middleProbability / 1.5) * float(sportsbook_multiplier)
                                                        overPercent = 1 - underPercent
                                                        overPercentages.append(overPercent)
                                                        underPercentages.append(underPercent)
                                                    try:
                                                        value = round(((((underPercent) * float(multiplier)) ** 3) * 6 - 1) * 100, 1)
                                                    except ValueError:
                                                        multiplier = 1
                                                        value = round(((((underPercent) * float(multiplier)) ** 3) * 6 - 1) * 100, 1)
                                                    evs.append(float(value))
                                                    higherOrLowers.append("Lower")
                                                elif "Lower" in str(sportsbook_higherOrLowers[i]):
                                                    overPrices.append(1.817 * float(sportsbook_multiplier))
                                                    underPrices.append(1.817 / float(sportsbook_multiplier))
                                                    middleProbability = calculate_probability(float(middle) - float(discrepancy), float(sportsbook_oldLines[i]), float(standardDev)) - calculate_probability(float(middle), float(sportsbook_oldLines[i]), float(standardDev))
                                                    if (sport == "NBA" or sport == "OBBALL" or sport == "WNBA") and (float(discrepancy) < 2) and ("Points" in sportsbook_newStats[i]):
                                                        underPercent = (0.5 - middleProbability * 2) / float(sportsbook_multiplier)
                                                        overPercent = 1 - underPercent
                                                        overPercentages.append(overPercent)
                                                        underPercentages.append(underPercent)
                                                    elif "Pitching Outs" in sportsbook_newStats[i]:
                                                        underPercent = (0.5 - middleProbability * 10) / float(sportsbook_multiplier)
                                                        overPercent = 1 - underPercent
                                                        overPercentages.append(overPercent)
                                                        underPercentages.append(underPercent)
                                                    elif float(discrepancy) == 0.5 or float(discrepancy) == -0.5 or float(discrepancy) == -0.25 or float(discrepancy) == 0.25:
                                                        underPercent = (0.5 - middleProbability * 4) / float(sportsbook_multiplier)
                                                        overPercent = 1 - underPercent
                                                        overPercentages.append(overPercent)
                                                        underPercentages.append(underPercent)
                                                    else:
                                                        underPercent = (0.5 - middleProbability * 1.5) / float(sportsbook_multiplier)
                                                        overPercent = 1 - underPercent
                                                        overPercentages.append(overPercent)
                                                        underPercentages.append(underPercent)
                                                    try:
                                                        value = round(((((overPercent) * float(multiplier)) ** 3) * 6 - 1) * 100, 1)
                                                    except ValueError:
                                                        multiplier = 1
                                                        value = round(((((overPercent) * float(multiplier)) ** 3) * 6 - 1) * 100, 1)
                                                    evs.append(float(value))
                                                    higherOrLowers.append("Higher")
                                                else:
                                                    overPrices.append(1.817)
                                                    underPrices.append(1.817)
                                                    middleProbability = calculate_probability(float(middle) - float(discrepancy), float(sportsbook_oldLines[i]), float(standardDev)) - calculate_probability(float(middle), float(sportsbook_oldLines[i]), float(standardDev))
                                                    if (sport == "NBA" or sport == "OBBALL" or sport == "WNBA") and (float(discrepancy) < 2) and ("Points" in sportsbook_newStats[i]):
                                                        underPercent = (0.5 - middleProbability / 2) * float(sportsbook_multiplier)
                                                        overPercent = 1 - underPercent
                                                        overPercentages.append(overPercent)
                                                        underPercentages.append(underPercent)
                                                    elif "Pitching Outs" in sportsbook_newStats[i]:
                                                        underPercent = (0.5 - middleProbability / 10) * float(sportsbook_multiplier)
                                                        overPercent = 1 - underPercent
                                                        overPercentages.append(overPercent)
                                                        underPercentages.append(underPercent)
                                                    elif float(discrepancy) == 0.5 or float(discrepancy) == -0.5 or float(discrepancy) == -0.25 or float(discrepancy) == 0.25:
                                                        underPercent = (0.5 - middleProbability / 4) * float(sportsbook_multiplier)
                                                        overPercent = 1 - underPercent
                                                        overPercentages.append(overPercent)
                                                        underPercentages.append(underPercent)
                                                    else:
                                                        underPercent = (0.5 - middleProbability / 1.5) * float(sportsbook_multiplier)
                                                        overPercent = 1 - underPercent
                                                        overPercentages.append(overPercent)
                                                        underPercentages.append(underPercent)
                                                    try:
                                                        value = round(((((underPercent) * float(multiplier)) ** 3) * 6 - 1) * 100, 1)
                                                    except ValueError:
                                                        multiplier = 1
                                                        value = round(((((underPercent)  * float(multiplier)) ** 3) * 6 - 1) * 100, 1)
                                                    evs.append(float(value))
                                                    higherOrLowers.append("Lower")
                                            elif "Pinnacle" in sportsbook or "DraftKings" in sportsbook:
                                                sportsbook_overPercentages = sportsbook_df["% Over"].values.tolist()
                                                sportsbook_underPercentages = sportsbook_df["% Under"].values.tolist()
                                                sportsbook_overPrices = sportsbook_df["Over Price"].values.tolist()
                                                sportsbook_underPrices = sportsbook_df["Under Price"].values.tolist()
                                                overPrices.append(sportsbook_overPrices[i])
                                                underPrices.append(sportsbook_underPrices[i])
                                                middleProbability = calculate_probability(float(middle) - float(discrepancy), float(sportsbook_oldLines[i]), float(standardDev)) - calculate_probability(float(middle), float(sportsbook_oldLines[i]), float(standardDev))
                                                if (sport == "NBA" or sport == "OBBALL" or sport == "WNBA") and (float(discrepancy) < 2) and ("Points" in sportsbook_newStats[i]):
                                                    underPercent = (sportsbook_underPercentages[i] - middleProbability / 2) * float(sportsbook_multiplier)
                                                    overPercent = 1 - underPercent
                                                    overPercentages.append(overPercent)
                                                    underPercentages.append(underPercent)
                                                elif "Pitching Outs" in sportsbook_newStats[i]:
                                                    underPercent = (sportsbook_underPercentages[i] - middleProbability / 10) * float(sportsbook_multiplier)
                                                    overPercent = 1 - underPercent
                                                    overPercentages.append(overPercent)
                                                    underPercentages.append(underPercent)
                                                elif float(discrepancy) == 0.5 or float(discrepancy) == -0.5 or float(discrepancy) == -0.25 or float(discrepancy) == 0.25:
                                                    underPercent = (sportsbook_underPercentages[i] - middleProbability / 4) * float(sportsbook_multiplier)
                                                    overPercent = 1 - underPercent
                                                    overPercentages.append(overPercent)
                                                    underPercentages.append(underPercent)
                                                else:
                                                    underPercent = (sportsbook_underPercentages[i] - middleProbability / 1.5) * float(sportsbook_multiplier)
                                                    overPercent = 1 - underPercent
                                                    overPercentages.append(overPercent)
                                                    underPercentages.append(underPercent)
                                                try:
                                                    value = round(((((underPercent) * float(multiplier)) ** 3) * 6 - 1) * 100, 1)
                                                except ValueError:
                                                    multiplier = 1
                                                value = round(((((underPercent) * float(multiplier)) ** 3) * 6 - 1) * 100, 1)
                                                evs.append(float(value))
                                                higherOrLowers.append("Lower")
                                            names.append(sportsbook_names[i])
                                            stats.append(sportsbook_newStats[i])
                                            sportsbooks.append(sportsbook)
                                            sportsbook_lines.append(sportsbook_oldLines[i])
                                            dfs_lines.append(dfs_oldLines[j])
                                            times.append(dfs_times[j])
                                            try:
                                                payouts.append(dfs_payouts[j])
                                            except UnboundLocalError:
                                                payouts.append("1x")
                        except ValueError:
                            pass
                j = j + 1
            i = i + 1

        newPayouts = []
        for payout in payouts:
            if "x" not in str(payout):
                newPayouts.append("1x")
            else:
                newPayouts.append(payout)
              
        newPayouts1 = []
        for payout in payouts1:
            if "x" not in str(payout):
                newPayouts1.append("1x")
            else:
                newPayouts1.append(payout)    
        
        newPayouts2 = []
        for payout in payouts2:
            if "x" not in str(payout):
                newPayouts2.append("1x")
            else:
                newPayouts2.append(payout)
                
        q = len(names) - 1
        while q >= 0:
            if "Higher" in higherOrLowers[q]:
                try:
                    if float(overPercentages[q]) >= 0.3 and float(overPercentages[q]) < 0.5:
                        names1.append(names.pop(q))
                        stats1.append(stats.pop(q))
                        sportsbooks1.append(sportsbooks.pop(q))
                        sportsbook_lines1.append(sportsbook_lines.pop(q))
                        dfs_lines1.append(dfs_lines.pop(q))
                        discrepancies1.append(discrepancies.pop(q))
                        overPrices1.append(overPrices.pop(q))
                        underPrices1.append(underPrices.pop(q))
                        overPercentages1.append(overPercentages.pop(q))
                        underPercentages1.append(underPercentages.pop(q))
                        newPayouts1.append(newPayouts.pop(q))
                        higherOrLowers1.append(higherOrLowers.pop(q))
                        evs1.append(evs.pop(q))
                        times1.append(times.pop(q))
                    elif float(overPercentages[q]) < 0.3:
                        names2.append(names.pop(q))
                        stats2.append(stats.pop(q))
                        sportsbooks2.append(sportsbooks.pop(q))
                        sportsbook_lines2.append(sportsbook_lines.pop(q))
                        dfs_lines2.append(dfs_lines.pop(q))
                        discrepancies2.append(discrepancies.pop(q))
                        overPrices2.append(overPrices.pop(q))
                        underPrices2.append(underPrices.pop(q))
                        overPercentages2.append(overPercentages.pop(q))
                        underPercentages2.append(underPercentages.pop(q))
                        newPayouts2.append(newPayouts.pop(q))
                        higherOrLowers2.append(higherOrLowers.pop(q))
                        evs2.append(evs.pop(q))
                        times2.append(times.pop(q))
                except IndexError:
                    pass
            elif "Lower" in higherOrLowers[q]:
                try:
                    if float(underPercentages[q]) >= 0.3 and float(underPercentages[q]) < 0.5:
                        names1.append(names.pop(q))
                        stats1.append(stats.pop(q))
                        sportsbooks1.append(sportsbooks.pop(q))
                        sportsbook_lines1.append(sportsbook_lines.pop(q))
                        dfs_lines1.append(dfs_lines.pop(q))
                        discrepancies1.append(discrepancies.pop(q))
                        overPrices1.append(overPrices.pop(q))
                        underPrices1.append(underPrices.pop(q))
                        overPercentages1.append(overPercentages.pop(q))
                        underPercentages1.append(underPercentages.pop(q))
                        newPayouts1.append(newPayouts.pop(q))
                        higherOrLowers1.append(higherOrLowers.pop(q))
                        evs1.append(evs.pop(q))
                        times1.append(times.pop(q))
                    elif float(underPercentages[q]) < 0.3:
                        names2.append(names.pop(q))
                        stats2.append(stats.pop(q))
                        sportsbooks2.append(sportsbooks.pop(q))
                        sportsbook_lines2.append(sportsbook_lines.pop(q))
                        dfs_lines2.append(dfs_lines.pop(q))
                        discrepancies2.append(discrepancies.pop(q))
                        overPrices2.append(overPrices.pop(q))
                        underPrices2.append(underPrices.pop(q))
                        overPercentages2.append(overPercentages.pop(q))
                        underPercentages2.append(underPercentages.pop(q))
                        newPayouts2.append(newPayouts.pop(q))
                        higherOrLowers2.append(higherOrLowers.pop(q))
                        evs2.append(evs.pop(q))
                        times2.append(times.pop(q))
                except IndexError:
                    pass
            q -= 1

        # Iterate through the new dataframe1 in reverse order to move additional entries to dataframe2
        r = len(names1) - 1
        while r >= 0:
            if "Higher" in higherOrLowers1[r]:
                if float(overPercentages1[r]) < 0.3:
                    names2.append(names1.pop(r))
                    stats2.append(stats1.pop(r))
                    sportsbooks2.append(sportsbooks1.pop(r))
                    sportsbook_lines2.append(sportsbook_lines1.pop(r))
                    dfs_lines2.append(dfs_lines1.pop(r))
                    discrepancies2.append(discrepancies1.pop(r))
                    overPrices2.append(overPrices1.pop(r))
                    underPrices2.append(underPrices1.pop(r))
                    overPercentages2.append(overPercentages1.pop(r))
                    underPercentages2.append(underPercentages1.pop(r))
                    newPayouts2.append(newPayouts1.pop(r))
                    higherOrLowers2.append(higherOrLowers1.pop(r))
                    evs2.append(evs1.pop(r))
                    times2.append(times1.pop(q))
            elif "Lower" in higherOrLowers1[r]:
                if float(underPercentages1[r]) < 0.3:
                    names2.append(names1.pop(r))
                    stats2.append(stats1.pop(r))
                    sportsbooks2.append(sportsbooks1.pop(r))
                    sportsbook_lines2.append(sportsbook_lines1.pop(r))
                    dfs_lines2.append(dfs_lines1.pop(r))
                    discrepancies2.append(discrepancies1.pop(r))
                    overPrices2.append(overPrices1.pop(r))
                    underPrices2.append(underPrices1.pop(r))
                    overPercentages2.append(overPercentages1.pop(r))
                    underPercentages2.append(underPercentages1.pop(r))
                    newPayouts2.append(newPayouts1.pop(r))
                    higherOrLowers2.append(higherOrLowers1.pop(r))
                    evs2.append(evs1.pop(r))
                    times2.append(times1.pop(q))
            r -= 1
            
        data = {'Name': names, 'Time': times, 'Stat': stats, 'Sportsbook': sportsbooks, 'Sportsbook Line': sportsbook_lines, 'DFS Line': dfs_lines, 'Discrepancy': discrepancies, 'Over Price': overPrices, 'Under Price': underPrices, '% Over': overPercentages, '% Under': underPercentages, 'Payout': newPayouts, 'Higher/Lower': higherOrLowers, 'EV': evs}
        df = pd.DataFrame(data)
        df_sorted = df.sort_values(by='EV', ascending=False)
        df_sorted['EV'] = df_sorted['EV'].apply(lambda x: str(x)[:6] + '%')
        df_sorted.to_csv(fileLoc, index=False)
        
        data1 = {'Name': names1, 'Time': times1, 'Stat': stats1, 'Sportsbook': sportsbooks1, 'Sportsbook Line': sportsbook_lines1, 'DFS Line': dfs_lines1, 'Discrepancy': discrepancies1, 'Over Price': overPrices1, 'Under Price': underPrices1, '% Over': overPercentages1, '% Under': underPercentages1, 'Payout': newPayouts1, 'Higher/Lower': higherOrLowers1, 'EV': evs1}
        df1 = pd.DataFrame(data1)
        df1_sorted = df1.sort_values(by='EV', ascending=False)
        df1_sorted['EV'] = df1_sorted['EV'].apply(lambda x: str(x)[:6] + '%')
        fileLoc1 = r"Underdog Scorchers CSV Location"
        if "Pinnacle" in sportsbook:
            fileLoc1 = r"Underdog Scorchers (Pinnacle) CSV Desired Location"
            df1_sorted.to_csv(fileLoc1, index=False)
        elif "DraftKings" in sportsbook:
            fileLoc1 = r"Underdog Scorchers (DraftKings) CSV Desired Location"
            df1_sorted.to_csv(fileLoc1, index=False)
        elif "PrizePicks" in sportsbook:
            fileLoc1 = r"Underdog Scorchers (PrizePicks) CSV Desired Location"
            df1_sorted.to_csv(fileLoc1, index=False)
        
        data2 = {'Name': names2, 'Time': times2, 'Stat': stats2, 'Sportsbook': sportsbooks2, 'Sportsbook Line': sportsbook_lines2, 'DFS Line': dfs_lines2, 'Discrepancy': discrepancies2, 'Over Price': overPrices2, 'Under Price': underPrices2, '% Over': overPercentages2, '% Under': underPercentages2, 'Payout': newPayouts2, 'Higher/Lower': higherOrLowers2, 'EV': evs2}
        df2 = pd.DataFrame(data2)
        df2_sorted = df2.sort_values(by='EV', ascending=False)
        df2_sorted['EV'] = df2_sorted['EV'].apply(lambda x: str(x)[:6] + '%')
        fileLoc2 = r"Underdog Longshots CSV Desired Location"
        if "Pinnacle" in sportsbook:
            fileLoc2 = r"Underdog Longshots (Pinnacle) CSV Desired Location"
            df2_sorted.to_csv(fileLoc2, index=False)
        elif "DraftKings" in sportsbook:
            fileLoc2 = r"Underdog Longshots (DraftKings) CSV Desired Location"
            df2_sorted.to_csv(fileLoc2, index=False)
        elif "PrizePicls in sportsbook":
            fileLoc2 = r"Underdog Longshots (PrizePicks) CSV Desired Location"
            df2_sorted.to_csv(fileLoc2, index=False)
        
        def create_message(dataframe, num_entries, unwanted_strings, ev_threshold):
            if len(dataframe) < num_entries:
                num_entries = len(dataframe)

            message = ""
            i = 0
            while i < num_entries:
                overPercent = float(dataframe['% Over'].iloc[i]) * 100
                overPercent = str(overPercent)[:4] + "%" 
                underPercent = float(dataframe['% Under'].iloc[i]) * 100
                underPercent = str(underPercent)[:4] + "%" 
                if "Higher" in dataframe['Higher/Lower'].iloc[i]:
                    new_message = (
                        f"{dataframe['Name'].iloc[i]} {dataframe['Higher/Lower'].iloc[i].lower()} "
                        f"than {dataframe['DFS Line'].iloc[i]} {dataframe['Stat'].iloc[i]} ("
                        f"{dataframe['EV'].iloc[i]} EV, {overPercent}, {dataframe['Payout'].iloc[i]} payout, {dataframe['Time'].iloc[i]})\n"
                    )
                elif "Lower" in dataframe['Higher/Lower'].iloc[i]:
                    new_message = (
                        f"{dataframe['Name'].iloc[i]} {dataframe['Higher/Lower'].iloc[i].lower()} "
                        f"than {dataframe['DFS Line'].iloc[i]} {dataframe['Stat'].iloc[i]} ("
                        f"{dataframe['EV'].iloc[i]} EV, {underPercent}, {dataframe['Payout'].iloc[i]} payout, {dataframe['Time'].iloc[i]})\n"
                    )
                    
                if not any(unwanted_string in new_message for unwanted_string in unwanted_strings):
                    if float((dataframe['EV'].iloc[i])[:-1]) >= ev_threshold:
                        message += new_message
                else:
                    if num_entries < len(dataframe):
                        num_entries += 1
                i += 1
            return message.strip()

        num_entries = min(6, len(names))
        if num_entries > 0:
            msg = create_message(df_sorted, num_entries, deletedPlayers, -50)
        else:
            msg = ""

        num_entries = min(6, len(names1))
        if num_entries > 0:
            msg1 = create_message(df1_sorted, num_entries, deletedPlayers, -50)

        else:
            msg1 = ""
        
        num_entries = min(6, len(names2))
        if num_entries > 0:
            msg2 = create_message(df2_sorted, num_entries, deletedPlayers, -50)
            
        else:
            msg2 = ""
            
        num_entries = min(20, len(names))
        if num_entries > 0:
            msg3 = create_message(df_sorted, num_entries, deletedPlayers, 3)
            
        else:
            msg3 = ""
            

        num_entries = min(20, len(names1))
        if num_entries > 0:
            msg4 = create_message(df1_sorted, num_entries, deletedPlayers, 5)
            
        else:
            msg4 = ""
            
        
        num_entries = min(6, len(names2))
        if num_entries > 0:
            msg5 = create_message(df2_sorted, num_entries, deletedPlayers, 60)
            
        else:
            msg5 = ""
            

        file = {'file': (fileName, open(fileLoc, 'rb'))}
        if len(names) >= 1:
            post(msg, fileLoc, fileName, sport)
        if "Underdog" in dfs and len(names) >= 1:
            if float((df_sorted['EV'].iloc[0])[:-1]) >= 3:
                if "DraftKings" in sportsbook:
                    send(msg3, fileName, sport)
                elif "Pinnacle" in sportsbook:
                    send(msg3, fileName, sport)
                elif "PrizePicks" in sportsbook:
                    send(msg3, fileName, sport)     
        elif "PrizePicks" in dfs and len(names) >= 1:
                if "DraftKings" in sportsbook:
                    send(msg3, fileName, sport)
                elif "Pinnacle" in sportsbook:
                    send(msg3, fileName, sport)
                elif "Underdog" in sportsbook:
                    send(msg3, fileName, sport)
        
        if "Underdog" in dfs and len(names1) >= 1:
            if "DraftKings" in sportsbook:
                file1 = {'file': ("Underdog Scorchers (DraftKings)", open(fileLoc1, 'rb'))}
                post(msg1, fileLoc1, "Underdog Scorchers (" + sportsbook + ")", sport)
                if float((df1_sorted['EV'].iloc[0])[:-1]) >= 5:
                    send(msg4, "Underdog Scorchers (" + sportsbook + ")", sport)
            elif "Pinnacle" in sportsbook:
                file1 = {'file': ("Underdog Scorchers (Pinnacle)", open(fileLoc1, 'rb'))}
                post(msg1, fileLoc1, "Underdog Scorchers (" + sportsbook + ")", sport)
                if float((df1_sorted['EV'].iloc[0])[:-1]) >= 5:
                    send(msg4, "Underdog Scorchers (" + sportsbook + ")", sport)
            elif "PrizePicks" in sportsbook:
                file1 = {'file': ("Underdog Scorchers (PrizePicks)", open(fileLoc1, 'rb'))}
                post(msg1, fileLoc1, "Underdog Scorchers (" + sportsbook + ")", sport)
                if float((df1_sorted['EV'].iloc[0])[:-1]) >= 5:
                    send(msg4, "Underdog Scorchers (" + sportsbook + ")", sport)

        
        if "Underdog" in dfs and len(names2) >= 1:
            if "DraftKings" in sportsbook:
                file2 = {'file': ("Underdog Longshots (DraftKings)", open(fileLoc2, 'rb'))}
                post(msg2, fileLoc2, "Underdog Longshots (" + sportsbook + ")", sport)
                if float((df2_sorted['EV'].iloc[0])[:-1]) >= 60:
                    send(msg5, "Underdog Longshots (" + sportsbook + ")", sport)
            elif "Pinnacle" in sportsbook:
                file2 = {'file': ("Underdog Longshots (Pinnacle)", open(fileLoc2, 'rb'))}
                post(msg2, fileLoc2, "Underdog Longshots (" + sportsbook + ")", sport)
                if float((df2_sorted['EV'].iloc[0])[:-1]) >= 60:
                    send(msg5, "Underdog Longshots (" + sportsbook + ")", sport)
            elif "PrizePicks" in sportsbook:
                file2 = {'file': ("Underdog Longshots (PrizePicks)", open(fileLoc2, 'rb'))}
                post(msg2, fileLoc2, "Underdog Longshots (" + sportsbook + ")", sport)
                if float((df2_sorted['EV'].iloc[0])[:-1]) >= 60:
                    send(msg5, "Underdog Longshots (" + sportsbook + ")", sport)
                    
            
    import requests
    import asyncio

    # Replace these with your webhook URLs
    POST_WEBHOOK_URL = "https://discord.com/api/webhooks/"  # Replace with your 'post' channel webhook
    SEND_WEBHOOK_URL = "https://discord.com/api/webhooks/"  # Replace with your 'send' channel webhook

    # Webhook helper function
    def send_webhook_message(webhook_url, content, username=None, avatar_url=None):
        # Sends a message to a Discord channel using a webhook.
        payload = {
            "content": content,
            "username": username,
            "avatar_url": avatar_url
        }
        try:
            response = requests.post(webhook_url, json=payload)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"Failed to send message: {e}")

    def post(msg, fileLoc, fileName, sport):
        # Sends a low-priority notification to the designated 'post' channel using a webhook.
        # Replace all urls with proper api url
        if "Underdog Favorites (PrizePicks)" in fileName:
            POST_WEBHOOK_URL = "https://discord.com/api/webhooks/"
        elif "Underdog Scorchers (PrizePicks)" in fileName:
            POST_WEBHOOK_URL = 'https://discord.com/api/webhooks/'
        elif "Underdog Longshots (PrizePicks)" in fileName:
            POST_WEBHOOK_URL = 'https://discord.com/api/webhooks/'
        elif "Underdog Favorites (DraftKings)" in fileName:
            POST_WEBHOOK_URL = 'https://discord.com/api/webhooks/'
        elif "Underdog Scorchers (DraftKings)" in fileName:
            POST_WEBHOOK_URL = 'https://discord.com/api/webhooks/'
        elif "Underdog Longshots (DraftKings)" in fileName:
            POST_WEBHOOK_URL = 'https://discord.com/api/webhooks/'
        elif "Underdog Favorites (Pinnacle)" in fileName:
            POST_WEBHOOK_URL = 'https://discord.com/api/webhooks/'
        elif "Underdog Scorchers (Pinnacle)" in fileName:
            POST_WEBHOOK_URL = 'https://discord.com/api/webhooks/'
        elif "Underdog Longshots (Pinnacle)" in fileName:
            POST_WEBHOOK_URL = 'https://discord.com/api/webhooks/'
        elif "PrizePicks Favorites (Underdog)" in fileName:
            POST_WEBHOOK_URL = 'https://discord.com/api/webhooks/'
        elif "PrizePicks Favorites (DraftKings)" in fileName:
            POST_WEBHOOK_URL = 'https://discord.com/api/webhooks/'
        elif "PrizePicks Favorites (Pinnacle)" in fileName:
            POST_WEBHOOK_URL = 'https://discord.com/api/webhooks/'


        title = f"**{fileName} - {sport}**\n"
        content = f"{title}{msg}"
        if len(msg) > 1:
            send_webhook_message(POST_WEBHOOK_URL, content, username="Projections Bot")            

    def send(msg2, fileName, sport):
        # Sends a normal-priority notification to the designated 'send' channel using a webhook.
        # Replace with your 'post' channel webhook
        if "Underdog Favorites (PrizePicks)" in fileName:
            SEND_WEBHOOK_URL = 'https://discord.com/api/webhooks/'
        elif "Underdog Scorchers (PrizePicks)" in fileName:
            SEND_WEBHOOK_URL = 'https://discord.com/api/webhooks/'
        elif "Underdog Longshots (PrizePicks)" in fileName:
            SEND_WEBHOOK_URL = 'https://discord.com/api/webhooks/'
        elif "Underdog Favorites (DraftKings)" in fileName:
            SEND_WEBHOOK_URL = 'https://discord.com/api/webhooks/'
        elif "Underdog Scorchers (DraftKings)" in fileName:
            SEND_WEBHOOK_URL = 'https://discord.com/api/webhooks/'
        elif "Underdog Longshots (DraftKings)" in fileName:
            SEND_WEBHOOK_URL = 'https://discord.com/api/webhooks/'
        elif "Underdog Favorites (Pinnacle)" in fileName:
            SEND_WEBHOOK_URL = 'https://discord.com/api/webhooks/'
        elif "Underdog Scorchers (Pinnacle)" in fileName:
            SEND_WEBHOOK_URL = 'https://discord.com/api/webhooks/'
        elif "Underdog Longshots (Pinnacle)" in fileName:
            SEND_WEBHOOK_URL = 'https://discord.com/api/webhooks/'
        elif "PrizePicks Favorites (Underdog)" in fileName:
            SEND_WEBHOOK_URL = 'https://discord.com/api/webhooks/'
        elif "PrizePicks Favorites (DraftKings)" in fileName:
            SEND_WEBHOOK_URL = 'https://discord.com/api/webhooks/'
        elif "PrizePicks Favorites (Pinnacle)" in fileName:
            SEND_WEBHOOK_URL = 'https://discord.com/api/webhooks/'


        title = f"**{fileName} - {sport} +EV**\n"
        content = f"{title}{msg2} <@1199947719842734111>"
        if len(msg2) > 1:
            send_webhook_message(SEND_WEBHOOK_URL, content, username="Projections Bot")
    
    import re
    from unidecode import unidecode

    from scipy import stats    
    def calculate_probability(projection, mean, std_deviation):
        probability = stats.norm.cdf(projection, mean, std_deviation)    
        return probability
        
    sports = ['NFL', 'NHL']
    for sport in sports:
        combine("Underdog", sport, "PrizePicks", r"Underdog Scraper CSV Location", r"PrizePicks Scraper CSV Location", r"Underdog Favorites (PrizePicks) CSV Desired Location", 'Underdog Favorites (PrizePicks)')
        combine("PrizePicks", sport, "Underdog", r"PrizePicks Scraper CSV Location", r"Underdog Scraper CSV Location", r"PrizePicks Favorites (Underdog) CSV Desired Location", 'PrizePicks Favorites (Underdog)')
        combine("Underdog", sport, "Pinnacle", r"Underdog Scraper CSV Location", r"Pinnacle Scraper CSV Location", r"Underdog Favorites (Pinnacle) CSV Desired Location", 'Underdog Favorites (Pinnacle)')
        combine("PrizePicks", sport, "Pinnacle", r"PrizePicks Scraper CSV Location", r"Pinnacle Scraper CSV Location", r"PrizePicks Favorites (Pinnacle) CSV Desired Location", 'PrizePicks Favorites (Pinnacle)')
        combine("Underdog", sport, "DraftKings", r"Underdog Scraper CSV Location", r"DraftKings Scraper CSV Location", r"Underdog Favorites (DraftKings) CSV Desired Location", 'Underdog Favorites (DraftKings)')
        combine("PrizePicks", sport, "DraftKings", r"PrizePicks Scraper CSV Location", r"DraftKings Scraper CSV Location", r"PrizePicks Favorites (DraftKings) CSV Desired Location", 'PrizePicks Favorites (DraftKings)')
    time.sleep(1200)

driver1 = webdriver.Chrome()
driver1.set_window_position(-1000, 1100)
driver1.set_window_size(1920, 1080)
while True:
    scrape()

