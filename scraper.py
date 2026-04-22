import argparse
import json
import re
from scrapling.fetchers import DynamicFetcher
import pandas as pd

class TrainScraper:
    def __init__(self):
        self.base_url = "https://tickets.paytm.com/trains/searchTrains"

    def fetch_trains(self, source, destination, date):
        url = f"{self.base_url}/{source}/{destination}/{date}"
        print(f"Fetching trains from {url}...")
        
        def interact(page):
            try:
                page.wait_for_selector("div.Gwgxn", timeout=10000)
                check_buttons = page.locator("button:has-text('Check Availability')")
                count = check_buttons.count()
                print(f"Found {count} 'Check Availability' buttons to confirm...")
                
                for i in range(count):
                    try:
                        btn = check_buttons.nth(i)
                        btn_text = btn.inner_text().replace('\n', ' ')
                        print(f"Clicking button {i} with text: {btn_text}")
                        btn.scroll_into_view_if_needed()
                        btn.click()
                        page.wait_for_timeout(1500)
                    except Exception as e:
                        print(f"Error clicking button {i}: {e}")
                
                page.wait_for_timeout(2000)
            except Exception as e:
                print(f"Interaction error: {e}")

        # Using fetch with page_action
        page = DynamicFetcher.fetch(url, network_idle=True, timeout=60000, page_action=interact)
        return self.parse_page(page)

    def parse_page(self, page):
        trains = []
        cards = page.css("div.Gwgxn")
        
        page_text = page.text or ""
        has_global_not_started = "Tatkal Booking not started yet" in page_text
        print(f"Global 'Not started' message present: {has_global_not_started}")

        for card in cards:
            train_name = card.css('[data-testid="trainName"] h1::text').get()
            train_number_raw = card.css('[data-testid="trainNumber"]::text').get()
            
            # Check for "Tatkal Booking not started" message in this card
            # Get all text in card
            all_text = " ".join(card.css("*::text").getall())
            not_started = "Tatkal Booking not started yet" in all_text or "expected to start at" in all_text
            if not_started:
                print(f"Train {train_name} has 'Not started' message detected in text")
            
            train_number = ""
            if train_number_raw:
                match = re.search(r'(\d{5})', train_number_raw)
                train_number = match.group(1) if match else train_number_raw.strip(" ()")
            
            dept_time = card.css('[data-testid="deptDateTime"] .enfHN::text').get()
            dept_date = card.css('[data-testid="deptDateTime"] .rqIJl::text').get()
            source_station = card.css('#srpSource::text').get()
            duration = card.css('#srpDuration::text').get()
            arr_time = card.css('#srpArrDateTime .enfHN::text').get()
            arr_date = card.css('#srpArrDateTime .rqIJl::text').get()
            dest_station = card.css('#srpDest::text').get()
            
            class_cards = card.css('div.dRu9W')
            availabilities = []
            for cc in class_cards:
                class_code = cc.css('[id$="-code"]::text').get()
                status = cc.css('[id$="-status"]::text').get()
                is_tatkal = "Tatkal" in (cc.css('.iE8j3::text').get() or "")
                
                # Check for "Tatkal Booking not started" message in this specific class card text
                cc_text = " ".join(cc.css("*::text").getall())
                cc_not_started = "Tatkal Booking not started yet" in cc_text or "expected to start at" in cc_text
                
                # If we detected "Not started" at card level, it's usually because one class was clicked
                # If this class is Tatkal, we should check if it's the one showing the message
                if is_tatkal and (cc_not_started or not_started):
                    status = "NOT OPEN"
                
                fare = cc.css('[id$="-fare"]::text').get()
                if not fare:
                    fare_text = cc.css('::text').getall()
                    for t in fare_text:
                        if '₹' in t:
                            fare = t
                            break
                
                chance = cc.css('.Ob72l span::text').get()
                
                if class_code:
                    availabilities.append({
                        "class": class_code,
                        "status": status,
                        "fare": fare,
                        "chance": chance,
                        "is_tatkal": is_tatkal
                    })
            
            trains.append({
                "name": train_name,
                "number": train_number,
                "departure": {"time": dept_time, "date": dept_date, "station": source_station},
                "arrival": {"time": arr_time, "date": arr_date, "station": dest_station},
                "duration": duration.strip() if duration else None,
                "availabilities": availabilities
            })
            
        return trains

def filter_and_rank(trains):
    flat_data = []
    for t in trains:
        for av in t['availabilities']:
            fare_val = 0
            if av['fare']:
                fare_val = int(re.sub(r'[^\d]', '', av['fare']))
            
            chance_val = 0
            if av['status'] == "NOT OPEN":
                chance_val = 0
            elif av['chance']:
                chance_val = int(av['chance'].strip('%'))
            elif av['status'] and 'AVL' in av['status']:
                chance_val = 100
            elif av['status'] and 'RAC' in av['status']:
                chance_val = 90
            
            score = chance_val * 10 - (fare_val / 100)
            if av['status'] == "NOT OPEN":
                score = -1000
            
            flat_data.append({
                "Train Name": t['name'],
                "Train No": t['number'],
                "Class": av['class'],
                "Status": av['status'],
                "Fare": av['fare'],
                "Chance": av['chance'] or ("100%" if (av['status'] and 'AVL' in av['status']) else "N/A"),
                "Departure": f"{t['departure']['time']} ({t['departure']['station']})",
                "Duration": t['duration'],
                "Score": score
            })
    
    df = pd.DataFrame(flat_data)
    if not df.empty:
        df = df.sort_values(by="Score", ascending=False)
    return df

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scrape Paytm Train Bookings")
    parser.add_argument("--source", default="ADI_Ahmedabad Jn", help="Source station")
    parser.add_argument("--dest", default="NDLS_Delhi- All Stations", help="Destination station")
    parser.add_argument("--date", default="20260503", help="Date in YYYYMMDD format")
    
    args = parser.parse_args()
    
    scraper = TrainScraper()
    train_data = scraper.fetch_trains(args.source, args.dest, args.date)
    
    if not train_data:
        print("No trains found.")
    else:
        results = filter_and_rank(train_data)
        print("\nTop Recommended Tickets:")
        print(results.head(15).to_string(index=False))
        
        with open("train_results.json", "w") as f:
            json.dump(train_data, f, indent=4)
        print(f"\nFull data saved to train_results.json")
