#!/bin/bash
# Setup script for train-bookings

echo "🚀 Setting up the train-bookings environment..."

# 1. Create and activate virtual environment
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

source venv/bin/activate

# 2. Install dependencies
echo "📥 Installing dependencies..."
pip install "scrapling[all]" pandas argparse playwright

# 3. Install browser binaries for Playwright/Scrapling
echo "🌐 Installing browser binaries..."
playwright install chromium

echo "✅ Setup complete! You can now run the scraper:"
echo "source venv/bin/activate"
echo "python3 multi_scraper.py --source ADI --dest NDLS --date 20260503"
