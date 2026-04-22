---
name: train-bookings
description: Scrapes and ranks train tickets from sources like Paytm and ConfirmTkt. Use when the user asks to find trains, check availability, or search for trains between stations on a specific date.
---

# Train Search & Availability

This skill allows you to find and cross-verify train ticket availability using real-time data from multiple sources.

## Core Knowledge & Rules

### 1. Tatkal Rules
- **Booking Window:** Tatkal quota opens only **one day before** the journey date (excluding the date of travel) at 10:00 AM for AC and 11:00 AM for non-AC.
- **Skepticism:** If a search date is more than 1 day in the future, disregard "Available" status for Tatkal. The scraper automatically flags these as "NOT OPEN (TATKAL)".

### 2. Cross-Verification (ConfirmTkt vs. Paytm)
- **Status Priority:** Always prioritize ConfirmTkt status for real-time accuracy and window checks.
- **Discrepancy Handling:** If Paytm says "Available" but ConfirmTkt says "Waitlisted", the skill will flag this discrepancy and show the waitlist status (the safer bet).

## Workflow

1.  **Search:** Use the `multi_scraper.py` to find the best train based on route and date.
2.  **Analyze:** Present the results to the user, highlighting the chance of confirmation and Tatkal window alerts.

## Reference Files
- **Multi Scraper:** `multi_scraper.py` (Core logic for cross-source verification).
