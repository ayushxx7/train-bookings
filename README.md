# 🚂 Train Bookings (RailSkeptic)

[![License: MIT](https://img.for-the-badge.com/static/v1?label=License&message=MIT&color=blue&style=for-the-badge)](LICENSE)
[![Built with Scrapling](https://img.for-the-badge.com/static/v1?label=Built%20With&message=Scrapling&color=orange&style=for-the-badge)](https://github.com/D4Vinci/Scrapling)

A high-signal train booking scraper and automation tool that cross-verifies availability between multiple sources (**Paytm**, **ConfirmTkt**) and enforces strict IRCTC rules (like Tatkal windows) to ensure you're never misled by cached data.

![Demo](showcase/demo.gif)

## 🌟 Why This Exists?
Most train booking aggregators show cached or "placeholder" availability for Tatkal and General quotas. This tool **cross-references** data from multiple sources and manually validates it against IRCTC's real-time rules:
- **Tatkal Protection**: Automatically flags Tatkal seats as "NOT OPEN" if searched outside the official 24h window.
- **Cross-Source Skepticism**: If Source A says "Available" but Source B says "Waitlisted", we show the more conservative status.
- **Smart Ranking**: Ranks trains by a score combining official **Chance of Confirmation**, timing, and fare value.

## 📦 Features
- **Multi-Source Scraping**: Scrapes and merges data from Paytm and ConfirmTkt.
- **Official Chance Scores**: Extracts confirmation percentages directly from the source UIs.
- **IRCTC Rule Engine**: Enforces booking window logic (AC 10am, Non-AC 11am).
- **Gemini CLI Skill**: Includes a native agent skill for natural language train searches.
- **Passenger Automation**: Ready to fill passenger details from `passengers.json` for rapid checkout.

## 🛠️ Tech Stack
- **Python 3.14**: Core logic.
- **Scrapling**: High-performance dynamic web scraping.
- **Pandas**: Data merging and ranking.
- **Playwright**: Browser orchestration.
- **Gemini CLI (OpenCode)**: AI agent integration.

## 🚀 Getting Started

### 1. Setup
```bash
./setup.sh
source venv/bin/activate
```

### 2. Search via CLI
```bash
python3 multi_scraper.py --source ADI --dest NDLS --date 20260503
```

### 3. Use as an AI Skill
If you have **Gemini CLI (OpenCode)** installed, you can search using natural language:
```bash
# In your Gemini session:
"Find trains from Ahmedabad to Delhi for next Sunday"
```

## 📋 Repository Health Score
| Category | Status | Score |
| :--- | :--- | :--- |
| **Documentation** | ✅ README, LICENSE | 20/20 |
| **Security** | ✅ .env Protected | 20/20 |
| **Automation** | ✅ setup.sh, setup automation | 20/20 |
| **Showcase** | ✅ Terminal Demo, Visual Gallery | 20/20 |
| **Total** | | **80/100** |

## ⚖️ License
Distributed under the **MIT License**. See `LICENSE` for more information.
