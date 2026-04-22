import json
import time
import argparse
from playwright.sync_api import sync_playwright

def load_passengers():
    with open('passengers.json', 'r') as f:
        return json.load(f)

def run_booking(source, dest, date, train_no, train_class):
    passengers = load_passengers()
    
    with sync_playwright() as p:
        # Launch browser in headful mode so the user can see/login
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()
        
        # 1. Navigate to Search
        url = f"https://tickets.paytm.com/trains/searchTrains/{source}/{dest}/{date}"
        print(f"🚀 Navigating to: {url}")
        page.goto(url)
        
        # 2. Manual Login Phase
        print("\n🔑 PLEASE LOGIN MANUALLY IN THE BROWSER WINDOW.")
        print("Once you are logged in and back on the search results page, press ENTER here...")
        input(">>> Press ENTER to continue after login...")

        # 3. Find and Select Train
        print(f"🔎 Looking for Train No: {train_no}, Class: {train_class}...")
        try:
            # Find the card with the train number
            train_card = page.locator(f"div.Gwgxn:has-text('{train_no}')")
            train_card.scroll_into_view_if_needed()
            
            # Find the specific class button within that card
            class_btn = train_card.locator(f"div.dRu9W:has-text('{train_class}')").locator("button")
            class_btn.click()
            print(f"✅ Selected Class {train_class}")
            
            # Wait for and click 'Book' button (usually appears after selecting class)
            book_btn = page.locator("button:has-text('Book')").first
            book_btn.wait_for(state="visible", timeout=5000)
            book_btn.click()
            print("✅ Clicked Book button")
            
        except Exception as e:
            print(f"❌ Error finding train/class: {e}")
            browser.close()
            return

        # 4. Fill Passenger Details
        print("📝 Automagically filling passenger details...")
        try:
            page.wait_for_selector("text=Add New Passenger", timeout=10000)
            
            for i, p_info in enumerate(passengers):
                print(f"  -> Adding {p_info['name']}...")
                # Click 'Add New' if not the first one
                if i > 0:
                    page.locator("text=Add New Passenger").click()
                
                # Fill details (selectors based on typical Paytm IRCTC form)
                # Note: These may need adjustment if Paytm updates their UI
                page.locator("input[placeholder='Name']").last.fill(p_info['name'])
                page.locator("input[placeholder='Age']").last.fill(str(p_info['age']))
                
                # Gender Selection
                if p_info['gender'] == 'M':
                    page.locator("text=Male").last.click()
                else:
                    page.locator("text=Female").last.click()
                    
                # Berth Preference (if exists in UI)
                # page.locator("select").last.select_option(label=p_info['preference'])

            print("✅ All passenger details filled!")
            
            # Proceed to Review
            proceed_btn = page.locator("button:has-text('Proceed')").first
            proceed_btn.click()
            
        except Exception as e:
            print(f"❌ Error during form filling: {e}")

        # 5. Hand-off to user for Payment
        print("\n🏁 AUTOMATION COMPLETE UP TO PAYMENT.")
        print("Please review the details and complete the payment manually.")
        print("The browser will stay open. Close it when you're done.")
        
        # Keep open
        while True:
            time.sleep(10)
            if page.is_closed():
                break

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Automate Train Booking on Paytm")
    parser.add_argument("--source", required=True, help="Source station code")
    parser.add_argument("--dest", required=True, help="Destination station code")
    parser.add_argument("--date", required=True, help="Date in YYYYMMDD")
    parser.add_argument("--train", required=True, help="Train Number (5 digits)")
    parser.add_argument("--class_code", required=True, help="Class (e.g. 2A, 3A, SL)")
    
    args = parser.parse_args()
    
    run_booking(args.source, args.dest, args.date, args.train, args.class_code)
