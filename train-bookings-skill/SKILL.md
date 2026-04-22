---
name: train-bookings
description: Scrapes and ranks train tickets from sources like Paytm and ConfirmTkt. Use when the user asks to find trains, book tickets, check availability, or search for trains between stations on a specific date.
---

# Train Bookings

This skill allows you to find and cross-verify train ticket availability and automate the booking process up to the payment screen.

## Core Knowledge & Rules

### 1. Tatkal Rules
- **Booking Window:** Tatkal quota opens only **one day before** the journey date (excluding the date of travel) at 10:00 AM for AC and 11:00 AM for non-AC.
- **Skepticism:** If a search date is more than 1 day in the future, disregard "Available" status for Tatkal. The scraper automatically flags these as "NOT OPEN (TATKAL)".

### 2. Cross-Verification (ConfirmTkt vs. Paytm)
- **Status Priority:** Always prioritize ConfirmTkt status for real-time accuracy and window checks.
- **Discrepancy Handling:** If Paytm says "Available" but ConfirmTkt says "Waitlisted", the skill will flag this discrepancy and show the waitlist status (the safer bet).

### 3. Booking Automation (`booking_agent.py`)
- **Workflow:** Once a train and class are selected, the agent can trigger the booking automation.
- **Manual Phase:** The user must log in manually in the opened browser window.
- **Automated Phase:** Once logged in, the script will automatically fill in all passenger details from `passengers.json`.
- **Hand-off:** The script stops at the payment gateway for the user to complete the transaction.

## Workflow

1.  **Search:** Use the `multi_scraper.py` to find the best train.
2.  **Select:** Ask the user if they want to book a specific train/class found in the results.
3.  **Execute Booking:**
    ```bash
    /Users/air/thevibecoder/projects/self/train-bookings/venv/bin/python3 /Users/air/thevibecoder/projects/self/train-bookings/booking_agent.py --source <SRC> --dest <DEST> --date <YYYYMMDD> --train <TRAIN_NO> --class_code <CLASS>
    ```

## Reference Files
- **Passengers:** `passengers.json` (Managed list of family members).
- **Booking Agent:** `booking_agent.py` (Playwright automation).
