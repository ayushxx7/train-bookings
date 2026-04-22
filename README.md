# 🚂 RailSkeptic (Train Search Skill)

[![Tested on Gemini CLI](https://img.shields.io/badge/Tested%20on-Gemini%20CLI-7A23FD.svg?style=for-the-badge)](https://github.com/google/gemini-cli)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg?style=for-the-badge)](LICENSE)
[![Built with Scrapling](https://img.shields.io/badge/Built%20With-Scrapling-orange.svg?style=for-the-badge)](https://github.com/D4Vinci/Scrapling)

**RailSkeptic** is a high-signal train search and availability verification tool and Gemini CLI Skill. It cross-verifies availability between **Paytm** and **ConfirmTkt**, enforcing strict IRCTC rules (like Tatkal windows) to ensure you're never misled by cached data.

![Demo](showcase/demo.gif)

## 🆕 What's New (April 2026)
- **🧠 Automatic Quota Detection**: Intelligently recommends **Senior Citizen (SS)** and **Ladies (LD)** quotas based on passenger profiles in `passengers.json`.
- **⚠️ Group Booking Strategies**: Detects mixed groups (e.g., Seniors + Young Males) and suggests optimal **split-booking** paths to maximize seat availability.
- **🕒 Detailed Schedules**: Captures **Departure**, **Arrival**, and **Duration** for every train, allowing for better trip planning.
- **💾 Contextual Memory**: Search results are persisted in `multi_source_results.json`, enabling context-aware follow-up questions within the Gemini CLI.

## ⚡ Quick Start: Install as a Skill
If you have [Gemini CLI (OpenCode)](https://github.com/google/gemini-cli) installed, you can use RailSkeptic as a native skill:

1. **Install the skill:**
   ```bash
   gemini skills install https://github.com/ayushxx7/train-bookings
   ```
2. **Reload & Use:**
   ```bash
   /skills reload
   "Find available tickets for Ahmedabad to Delhi on May 15"
   ```

---

## 🌟 Why This Exists?
Most train booking aggregators show cached or "placeholder" availability. This tool **cross-references** data from multiple sources and manually validates it against IRCTC's real-time rules:
- **Tatkal Protection**: Automatically flags Tatkal seats as "NOT OPEN" if searched outside the official 24h window.
- **Cross-Source Skepticism**: If Source A says "Available" but Source B says "Waitlisted", we show the more conservative status.
- **Smart Ranking**: Ranks trains by a score combining official **Chance of Confirmation**, timing, and fare value.

## 🧠 AI Memory & Follow-up
RailSkeptic stores the latest search context in `multi_source_results.json`. This allows the Gemini CLI to:
- **Remember your trip**: "Which of these trains arrives earliest?" or "What's the fare for the 2A class on Ashram?"
- **Answer deep questions**: "Is there a train that leaves after 6 PM?"
- **Smart Recommendations**: It uses the stored `raw_data` to provide more nuanced answers without hitting the network again.

## 📦 Features
- **🧠 Intelligent Quota Engine**: Automatically analyzes `passengers.json` to recommend the best quota (SS, LD, GN, TQ).
- **⚠️ Booking Strategy Alerts**: Suggests split bookings for mixed groups to optimize availability.
- **🕒 Timing & Schedules**: Captures Departure, Arrival, and Duration for better trip context.
- **Official Chance Scores**: Extracts confirmation percentages directly from source UIs.
- **IRCTC Rule Engine**: Enforces booking window logic (AC 10am, Non-AC 11am).
- **Multi-Source Verification**: Instant comparison between Paytm and ConfirmTkt.
- **💾 Result Persistence**: Stores search data in `multi_source_results.json` for follow-up questions.

## 🎟️ Supported Quotas
The tool supports and intelligently recommends:
- **GN (General)**: Default quota.
- **SS (Senior Citizen)**: Automatic for men 60+, women 45+.
- **LD (Ladies)**: Automatic for female-only adult groups.
- **TQ (Tatkal)**: Real-time window enforcement for last-minute booking.

## 🛠️ Tech Stack
- **Python 3.14** | **Scrapling** | **Playwright** | **Gemini CLI (OpenCode)**

## 🚀 CLI Usage (Raw)
```bash
./setup.sh
source venv/bin/activate
python3 multi_scraper.py --source ADI --dest NDLS --date 20260503
```

## ⚖️ License
Distributed under the **MIT License**. See `LICENSE` for more information.
