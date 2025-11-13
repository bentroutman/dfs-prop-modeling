# DFS Prop Modeling
This project investigates player prop modeling and market movements using publicly available data from Daily Fantasy Sports (DFS) platforms like PrizePicks and Underdog. Model demonstrated a consistent predictive edge, with estimated ROI of 14.8% on Underdog and 14.4% on PrizePicks, corresponding to ~57.6% hit rates per prop. It focuses on automated data collection and cleaning and predictive modeling to estimate expected value (EV) and identify inefficiencies in player props. Prop lines are compared to equivalent props on various DFS sites and sportsbooks to identify price and/or line discrepancies.

---

## Features
- Automated data collection from DFS and sportsbook APIs  
- Cleaning and standardizing player prop data  
- Expected value and probability estimation models  
- Line movement tracking
- Discord notifications identifying new profitable opportunities

---

## Model Performance
Model implementation demonstrated very strong predictive accuracy across platforms:

| Platform    | Prop Hit Rate | Estimated ROI * |
|-------------|---------------|-----------------|
| Underdog    | 0.5763        | 14.8%           |
| PrizePicks  | 0.5759        | 14.4%           |

\* ROI assumes a 3-leg parlay with 6x payout, since this is generally the most optimal bet type on DFS

---

## Technologies Used
- Language: Python
- Automation Libraries: Selenium, PyAutoGUI, win32api, win32con, time, cv2, pytesseract
- Data & Analysis: pandas, numpy, requests, re
- Workflow: Jupyter Notebook

---

## Betting Platforms
- DFS: Underdog, PrizePicks
- Sportsbooks (used only as a data point, not to place bets): Pinnacle, DraftKings
