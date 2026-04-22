---
name: train-bookings
description: Scrapes and ranks train tickets from sources like Paytm and ConfirmTkt. Use when the user asks to find trains, book tickets, check availability, or search for trains between stations on a specific date.
---

# Train Bookings

This skill allows you to find and cross-verify train ticket availability and manage passenger details for future booking automation.

## Core Knowledge & Rules

### 1. Tatkal Rules
- **Booking Window:** Tatkal quota opens only **one day before** the journey date (excluding the date of travel) at 10:00 AM for AC and 11:00 AM for non-AC.
- **Skepticism:** If a search date is more than 1 day in the future, disregard "Available" status for Tatkal. The scraper automatically flags these as "NOT OPEN (TATKAL)".
- **Search Strategy:** For future dates, prioritize General quota results first.

### 2. Cross-Verification (ConfirmTkt vs. Paytm)
- **Status Priority:** Always prioritize ConfirmTkt status for real-time accuracy and window checks.
- **Discrepancy Handling:** If Paytm says "Available" but ConfirmTkt says "Waitlisted", the skill will flag this discrepancy and show the waitlist status (the safer bet).

### 3. Chance Scores
- Official percentage confirmation scores (e.g., "70% Chance") are extracted from the UI and used to rank results.

### 4. Passenger Automation
- **Data Source:** Family details are stored in `/Users/air/thevibecoder/projects/self/train-bookings/passengers.json`.
- **Goal:** Automate form filling up to the payment screen (manual intervention required for final payment).

## Workflow

1.  **Extract Parameters:** Identify the `source` station, `destination` station, and `date`.
2.  **Execute Scraper:**
    ```bash
    /Users/air/thevibecoder/projects/self/train-bookings/venv/bin/python3 /Users/air/thevibecoder/projects/self/train-bookings/multi_scraper.py --source <CODE> --dest <CODE> --date <YYYYMMDD>
    ```
3.  **Result Analysis:** Rank by "Score" (Chance - Fare penalty). Flag any discrepancies where sources disagree.

## Reference Files
- **Passengers:** `passengers.json` (Add real names/ages here for booking automation).
- **Scraper:** `multi_scraper.py` (The main engine).
