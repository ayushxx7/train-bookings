---
name: train-bookings
description: Scrapes and ranks train tickets from sources like Paytm and ConfirmTkt. Use when the user asks to find trains, check availability, or search for trains between stations on a specific date.
---

# Train Search & Availability

This skill allows you to find and cross-verify train ticket availability using real-time data from multiple sources and provides intelligent booking recommendations.

## Core Knowledge & Rules

### 1. Automatic Quota Detection
The skill automatically analyzes passenger details (age and gender) to recommend the best booking quota:
- **SS (Senior Citizen):** Recommended if seniors (Males 60+, Females 45+) are traveling.
- **LD (Ladies):** Recommended if all adult passengers are female.
- **GN (General):** Default for all other cases.
- **TQ (Tatkal):** Always available but subject to specific timing rules.

### 2. Booking Strategies
- **Split Booking Strategy:** If a group is mixed (e.g., seniors and young males), the skill suggests splitting the booking to maximize the chance of getting a seat. Seniors/Ladies can book under SS/LD quotas while others use GN.
- **Quota Bonus:** Search results are ranked with a significant bonus (+500 score) for matches within the recommended quota, as these are targeted for the group.

### 3. Tatkal Rules
- **Booking Window:** Tatkal quota opens only **one day before** the journey date (excluding the date of travel) at 10:00 AM for AC and 11:00 AM for non-AC.
- **Skepticism:** If a search date is more than 1 day in the future, disregard "Available" status for Tatkal. The scraper automatically flags these as "NOT OPEN (TATKAL)".

### 4. Cross-Verification (ConfirmTkt vs. Paytm)
- **Status Priority:** Always prioritize ConfirmTkt status for real-time accuracy and window checks.
- **Discrepancy Handling:** If Paytm says "Available" but ConfirmTkt says "Waitlisted", the skill flags this discrepancy and prioritizes the safer (Waitlisted) status.

## Workflow

1.  **Analyze Passengers:** Reads `passengers.json` to determine eligibility for special quotas.
2.  **Search:** Uses `multi_scraper.py` with the recommended quota to find and rank the best trains.
3.  **Recommend:** Presents a cross-verified list of tickets, highlighting the best quota-based options and any necessary booking strategies (e.g., split bookings).

## Reference Files
- **Quota Manager:** `quota_manager.py` (Logic for passenger analysis and quota eligibility).
- **Multi Scraper:** `multi_scraper.py` (Core logic for cross-source verification and quota-aware searching).
