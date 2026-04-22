import json
import time
import argparse
from playwright.sync_api import sync_playwright

def load_passengers():
    with open('passengers.json', 'r') as f:
        return json.load(f)

def highlight(element):
    element.evaluate("el => { el.style.border = '5px solid red'; el.style.backgroundColor = 'yellow'; }")
    time.sleep(1)

def run_booking(source, dest, date, train_no, train_class, quota="GN", headless=False):
    passengers = load_passengers()
    
    with sync_playwright() as p:
        # Launch browser
        browser = p.chromium.launch(headless=headless)
        context = browser.new_context()
        page = context.new_page()
        
        # 1. Navigate to Search
        import urllib.parse
        s_enc = urllib.parse.quote(source)
        d_enc = urllib.parse.quote(dest)
        url = f"https://tickets.paytm.com/trains/searchTrains/{s_enc}/{d_enc}/{date}"
        if quota != "GN":
            url = f"{url}?quota={quota}"
            
        print(f"🚀 Navigating to: {url}")
        page.goto(url)
        page.screenshot(path="step1_search.png")
        
        # 2. Find and Select Train
        print(f"🔎 Looking for Train No: {train_no}, Class: {train_class}...")
        try:
            # Find the card with the train number
            train_card = page.locator(f"div.Gwgxn:has-text('{train_no}')")
            train_card.scroll_into_view_if_needed()
            highlight(train_card)
            
            # Find the specific class button within that card
            class_btn = train_card.locator(f"div.dRu9W:has-text('{train_class}')").locator("button").first
            highlight(class_btn)
            class_btn.click()
            print(f"✅ Selected Class {train_class}")
            
            # Wait for and click 'Book' button
            page.wait_for_timeout(2000)
            page.screenshot(path="step2_class_selected.png")
            
            if "confirm" not in page.url:
                print("⏳ Waiting for 'Book' button...")
                book_btn = page.locator("button:has-text('Book')").first
                try:
                    book_btn.wait_for(state="visible", timeout=5000)
                    highlight(book_btn)
                    book_btn.click()
                    print("✅ Clicked Book button")
                except:
                    print("ℹ️ 'Book' button not found or already navigated.")
            else:
                print("✅ Navigated to booking page directly.")
            
            page.wait_for_timeout(2000)
            page.screenshot(path="step3_confirm_page.png")
            
        except Exception as e:
            print(f"❌ Error finding train/class: {e}")
            page.screenshot(path="error_select.png")
            if headless:
                browser.close()
                return
            # If not headless, we fall through to the manual check/wait loop

        # 3. Manual Login Phase (If needed)
        print("📝 Checking for passenger details form...")
        try:
            # Wait for passenger section
            try:
                # Try multiple possible selectors for the passenger page
                page.wait_for_selector("text=Add New Passenger, text=Passenger Details, input[placeholder='Name']", timeout=8000)
                print("✅ Passenger details page detected!")
            except:
                print("DEBUG: Current URL:", page.url)
                # Print some text from the page to see where we are
                try:
                    texts = page.locator("button, h1, h2, label").all_inner_texts()
                    print("DEBUG: Visible elements on page:", [t.strip() for t in texts if t.strip()][:15])
                except: pass

                if not headless:
                    print("\n🔑 LOGIN OR NAVIGATION REQUIRED.")
                    print("If you are on the passenger page, just wait. If not, please login/navigate.")
                    print("Once you are on the page where you enter passenger names, press ENTER here...")
                    input(">>> Press ENTER to continue...")
                else:
                    print("\n⚠️ Running in HEADLESS mode. Cannot proceed.")
                    browser.close()
                    return
        except Exception as e:
            print(f"❌ Error during page check: {e}")

        # 4. Fill Passenger Details
        print("📝 Filling passenger details...")
        try:
            for i, p_info in enumerate(passengers):
                print(f"  -> Adding {p_info['name']}...")
                page.screenshot(path=f"step4_filling_p{i}.png")
                
                # Click 'Add New' if not the first one
                if i > 0:
                    add_btn = page.locator("text=Add New Passenger")
                    highlight(add_btn)
                    add_btn.click()
                
                # Fill details
                name_field = page.locator("input[placeholder='Name']").last
                highlight(name_field)
                name_field.fill(p_info['name'])
                
                age_field = page.locator("input[placeholder='Age']").last
                highlight(age_field)
                age_field.fill(str(p_info['age']))
                
                # Gender Selection
                if p_info['gender'] == 'M':
                    page.locator("text=Male").last.click()
                else:
                    page.locator("text=Female").last.click()

            print("✅ All passenger details filled!")
            page.screenshot(path="step5_filled.png")
            
            # Proceed to Review
            proceed_btn = page.locator("button:has-text('Proceed')").first
            highlight(proceed_btn)
            # proceed_btn.click() # Commented out for safety during testing
            
        except Exception as e:
            print(f"❌ Error during form filling: {e}")
            page.screenshot(path="error_fill.png")
                    
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
        if not headless:
            while True:
                time.sleep(1)
                if page.is_closed():
                    break
        else:
            print("🚀 Headless run finished.")
            browser.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Automate Train Booking on Paytm")
    parser.add_argument("--source", required=True, help="Source station code")
    parser.add_argument("--dest", required=True, help="Destination station code")
    parser.add_argument("--date", required=True, help="Date in YYYYMMDD")
    parser.add_argument("--train", required=True, help="Train Number (5 digits)")
    parser.add_argument("--class_code", required=True, help="Class (e.g. 2A, 3A, SL)")
    parser.add_argument("--quota", default="GN", help="Quota (GN, SS, LD, TQ)")
    parser.add_argument("--headless", action="store_true", help="Run in headless mode")
    
    args = parser.parse_args()
    
    run_booking(args.source, args.dest, args.date, args.train, args.class_code, args.quota, args.headless)
