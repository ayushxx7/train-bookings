# 🚂 RailSkeptic (Train Bookings Skill)

[![Tested on Gemini CLI](https://img.shields.io/badge/Tested%20on-Gemini%20CLI-7A23FD.svg?style=for-the-badge)](https://github.com/google/gemini-cli)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg?style=for-the-badge)](LICENSE)
[![Built with Scrapling](https://img.shields.io/badge/Built%20With-Scrapling-orange.svg?style=for-the-badge)](https://github.com/D4Vinci/Scrapling)

**RailSkeptic** is a high-signal train booking automation tool and Gemini CLI Skill. It cross-verifies availability between **Paytm** and **ConfirmTkt**, enforcing strict IRCTC rules (like Tatkal windows) to ensure you're never misled by cached data.

![Demo](showcase/demo.gif)

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

## 📦 Features
- **Official Chance Scores**: Extracts confirmation percentages directly from source UIs.
- **IRCTC Rule Engine**: Enforces booking window logic (AC 10am, Non-AC 11am).
- **Passenger Automation**: Injects family details from `passengers.json` for rapid checkout (coming soon).

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
