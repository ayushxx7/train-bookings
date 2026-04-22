import json
import time
import argparse
from playwright.sync_api import sync_playwright

def load_passengers():
    with open('passengers.json', 'r') as f:
        return json.load(f)

def highlight(element):
    try:
        element.evaluate("el => { el.style.border = '5px solid red'; el.style.backgroundColor = 'yellow'; }")
        time.sleep(0.5)
    except: pass

def close_modals(page):
    """Closes any blocking modals or overlays."""
    try:
        # Check for common close buttons or overlays
        selectors = [
            "button:has-text('No')", 
            "button:has-text('✕')", 
            "button:has-text('Close')", 
            "div[class*='close']",
            "span:has-text('✕')",
            "div.modal-close"
        ]
        for selector in selectors:
            btns = page.locator(selector).all()
            for btn in btns:
                if btn.is_visible():
                    print(f"🪄 Closing modal via: {selector}")
                    btn.click()
                    time.sleep(1)
        
        # Also try clicking escape key
        page.keyboard.press("Escape")
    except Exception:
        pass

def run_booking(source, dest, date, train_no, train_class, quota="GN", headless=False):
    passengers = load_passengers()
    phone_number = "9818994579"
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless)
        context = browser.new_context()
        page = context.new_page()
        
        # 1. Navigate to Search
        d = str(date)
        formatted_date = f"{d[6:8]}-{d[4:6]}-{d[0:4]}" if len(d) == 8 else d
        url = f"https://www.confirmtkt.com/rbooking/trains/from/{source}/to/{dest}/{formatted_date}"
        if quota != "GN":
            url = f"{url}?quota={quota}"
            
        print(f"🚀 Navigating to: {url}")
        page.goto(url)
        time.sleep(5)
        close_modals(page)
        
        # 2. Find and Select Train
        print(f"🔎 Looking for Train No: {train_no}, Class: {train_class}...")
        try:
            page.wait_for_selector(f"div[id='train-{train_no}']", timeout=20000)
            train_card = page.locator(f"div[id='train-{train_no}']")
            train_card.scroll_into_view_if_needed()
            highlight(train_card)
            
            # Find class card
            class_card = train_card.locator("div._cache-card-wrapper_662zq_5").filter(has_text=train_class).first
            if not class_card.is_visible():
                class_card = train_card.locator("div").filter(has_text=train_class).first
            
            highlight(class_card)
            class_card.click(force=True)
            print(f"✅ Selected Class {train_class}")
            time.sleep(2)
            
            # 3. Handle 'Secure my trip' or other post-selection popups
            close_modals(page)
            
            # 4. Find and Click 'Book' button
            # It could be 'Book', 'Book Now', 'PROCEED', 'Proceed to Book'
            print("📑 Searching for Book button...")
            book_selectors = [
                "button:has-text('Book')", 
                "button:has-text('BOOK')", 
                "button:has-text('Proceed')",
                "button:has-text('PROCEED')",
                "div.book-btn",
                "a:has-text('Book')"
            ]
            
            book_btn = None
            for selector in book_selectors:
                try:
                    btn = page.locator(selector).filter(has_not=page.locator(".hidden")).first
                    if btn.is_visible(timeout=2000):
                        book_btn = btn
                        break
                except: continue
                
            if not book_btn:
                print("⚠️ Book button not found, trying one more time after closing modals...")
                close_modals(page)
                time.sleep(2)
                for selector in book_selectors:
                    try:
                        btn = page.locator(selector).filter(has_not=page.locator(".hidden")).first
                        if btn.is_visible(timeout=2000):
                            book_btn = btn
                            break
                    except: continue

            if book_btn:
                highlight(book_btn)
                book_btn.click(force=True)
                print("✅ Clicked Book button")
            else:
                print("❌ Could not find Book button. Taking screenshot.")
                page.screenshot(path="error_book_button.png")
                if headless: return

        except Exception as e:
            print(f"❌ Error during selection: {e}")
            page.screenshot(path="error_selection.png")
            if headless: return

        # 5. Phone Number / Login
        try:
            print(f"📱 Entering phone number: {phone_number}...")
            # Wait for phone input - could be in a modal
            phone_selectors = [
                "input[type='tel']",
                "input[placeholder*='Phone']",
                "input[placeholder*='Mobile']",
                "input[name*='mobile']",
                "input[id*='mobile']"
            ]
            
            phone_input = None
            for sel in phone_selectors:
                try:
                    inp = page.locator(sel).first
                    if inp.is_visible(timeout=5000):
                        phone_input = inp
                        break
                except: continue
                
            if not phone_input:
                print("⚠️ Phone input not found with standard selectors, trying wait_for_selector...")
                page.wait_for_selector("input[placeholder*='Mobile'], input[type='tel']", timeout=10000)
                phone_input = page.locator("input[placeholder*='Mobile'], input[type='tel']").first

            phone_input.click()
            phone_input.fill("")
            phone_input.type(phone_number, delay=100)
            print(f"✅ Filled phone number: {phone_number}")
            
            # Click proceed
            # The button might have different text or be an icon
            proceed_btn = page.locator("button:has-text('PROCEED'), button:has-text('Proceed'), button:has-text('Login'), button[aria-label='Login'], button:has-text('NEXT')").first
            
            highlight(proceed_btn)
            proceed_btn.click(force=True)
            print("✅ Clicked Proceed/Login button")
            
            print("⏳ WAITING FOR OTP... Please enter it in the browser.")
            # Wait for passenger name input to appear (max 2 mins)
            page.wait_for_selector("input[placeholder='Passenger Name'], input[name='name'], input[placeholder='Search Name']", timeout=120000) 
            print("✅ OTP verified. Filling passenger details...")
            
        except Exception as e:
            print(f"❌ Error during login/OTP: {e}")
            page.screenshot(path="error_login.png")

        # 6. Fill Passenger Details
        try:
            print(f"📋 Filling {len(passengers)} passenger details...")
            for i, p_info in enumerate(passengers):
                print(f"  -> Adding {p_info['name']} ({p_info['age']})...")
                
                # If we need to click "Add Adult" for every passenger or just after the first
                # Usually there's one empty form, then we click "Add" for others
                if i > 0 or not page.locator("input[placeholder*='Name']").first.is_visible():
                    add_btn_selectors = [
                        "button:has-text('Add Adult')",
                        "button:has-text('ADD ADULT')",
                        "button:has-text('Add Passenger')",
                        "button:has-text('ADD PASSENGER')",
                        "text='+ Add'",
                        ".add-passenger-btn"
                    ]
                    added = False
                    for selector in add_btn_selectors:
                        btn = page.locator(selector).first
                        if btn.is_visible():
                            btn.click()
                            time.sleep(1)
                            added = True
                            break
                    if not added and i > 0:
                        print(f"⚠️ Could not find 'Add' button for passenger {i+1}")

                # Fill details in the latest form or the specific index
                # If it's a modal, we always use the first visible one
                name_input = page.locator("input[placeholder*='Name'], input[name='name']").last
                age_input = page.locator("input[placeholder*='Age'], input[name='age']").last
                
                name_input.fill(p_info['name'])
                age_input.fill(str(p_info['age']))
                
                # Gender Selection - look for labels or buttons
                gender_val = "Male" if p_info['gender'] == 'M' else "Female"
                gender_btn = page.locator(f"text={gender_val}, label:has-text('{gender_val}')").last
                if gender_btn.is_visible():
                    gender_btn.click()
                
                # Berth Preference if available
                if 'preference' in p_info:
                    try:
                        pref_select = page.locator("select[name*='berth'], .berth-preference-select").last
                        if pref_select.is_visible():
                            pref_select.select_option(label=p_info['preference'])
                    except: pass

                # Save / Done button for this passenger if it's a modal
                save_selectors = [
                    "button:has-text('Save')",
                    "button:has-text('SAVE')",
                    "button:has-text('Done')",
                    "button:has-text('Add Passenger')",
                    "button:has-text('ADD')"
                ]
                for selector in save_selectors:
                    btn = page.locator(selector).first
                    # Only click if it's likely a save button for the current entry (e.g. inside a modal or bottom of form)
                    if btn.is_visible():
                        print(f"    Clicking {selector} to save passenger...")
                        btn.click()
                        time.sleep(1)
                        break

            print("✅ All passenger details filled!")
            print("\n🏁 FINAL STEP: Review and Pay manually.")
            
        except Exception as e:
            print(f"❌ Error filling details: {e}")
            page.screenshot(path="error_passengers.png")

        if not headless:
            print("Browser kept open for finalization. Press Ctrl+C to exit.")
            try:
                while True: time.sleep(1)
            except KeyboardInterrupt: pass
        
        browser.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True)
    parser.add_argument("--dest", required=True)
    parser.add_argument("--date", required=True)
    parser.add_argument("--train", required=True)
    parser.add_argument("--class_code", required=True)
    parser.add_argument("--quota", default="GN")
    parser.add_argument("--headless", action="store_true")
    args = parser.parse_args()
    run_booking(args.source, args.dest, args.date, args.train, args.class_code, args.quota, args.headless)
