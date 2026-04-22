import argparse
import json
import re
from datetime import datetime, timedelta
from scrapling.fetchers import DynamicFetcher
import pandas as pd

class MultiSourceScraper:
    def __init__(self):
        self.paytm_base = "https://tickets.paytm.com/trains/searchTrains"
        self.confirmtkt_base = "https://www.confirmtkt.com/rbooking/trains/from"

    def is_tatkal_open(self, date_str):
        """
        Tatkal opens 1 day before journey (excluding journey date).
        Search date: YYYYMMDD
        """
        try:
            journey_date = datetime.strptime(date_str, "%Y%m%d").date()
            today = datetime.now().date()
            # Tatkal opens 1 day before. 
            # If journey is May 3, opens May 2.
            # So if today is BEFORE (journey_date - 1 day), it's NOT open.
            opens_on = journey_date - timedelta(days=1)
            return today >= opens_on
        except:
            return True # Fallback to showing if date parsing fails

    def fetch_paytm(self, source, dest, date):
        url = f"{self.paytm_base}/{source}/{dest}/{date}"
        print(f"Fetching Paytm: {url}...")
        self.current_search_date = date
        
        def interact(page):
            try:
                page.wait_for_selector("div.Gwgxn", timeout=10000)
                check_buttons = page.locator("button:has-text('Check Availability')")
                count = min(check_buttons.count(), 10) # Limit clicks
                for i in range(count):
                    try:
                        btn = check_buttons.nth(i)
                        btn.scroll_into_view_if_needed()
                        btn.click()
                        page.wait_for_timeout(1000)
                    except: pass
                page.wait_for_timeout(1000)
            except: pass

        response = DynamicFetcher.fetch(url, network_idle=True, timeout=60000, page_action=interact)
        return self.parse_paytm(response)

    def parse_paytm(self, page):
        trains = {}
        cards = page.css("div.Gwgxn")
        tatkal_open = self.is_tatkal_open(self.current_search_date)
        
        for card in cards:
            name = card.css('[data-testid="trainName"] h1::text').get()
            num_raw = card.css('[data-testid="trainNumber"]::text').get()
            num = re.search(r'(\d{5})', num_raw).group(1) if num_raw and re.search(r'(\d{5})', num_raw) else ""
            
            all_text = " ".join(card.css("*::text").getall())
            not_started = "Tatkal Booking not started yet" in all_text or "expected to start at" in all_text
            
            classes = []
            for cc in card.css('div.dRu9W'):
                code = cc.css('[id$="-code"]::text').get()
                status = cc.css('[id$="-status"]::text').get()
                is_tatkal = "Tatkal" in (cc.css('.iE8j3::text').get() or "")
                
                if is_tatkal and (not_started or not tatkal_open):
                    status = "NOT OPEN (TATKAL)"
                
                # Extract Chance Score if available
                chance = cc.xpath('following-sibling::div[contains(@class, "Ob72l")]//span/text()').get()
                if not chance: # Sometimes it's nested differently
                    chance = card.css('.Ob72l span::text').get() # Fallback

                fare = cc.css('[id$="-fare"]::text').get()
                if not fare:
                    for t in cc.css('::text').getall():
                        if '₹' in t: fare = t; break
                
                if code:
                    classes.append({
                        "class": code, 
                        "status": status, 
                        "fare": fare, 
                        "chance": chance,
                        "source": "Paytm"
                    })
            
            if num: trains[num] = {"name": name, "classes": classes}
        return trains

    def fetch_confirmtkt(self, source_code, dest_code, date_str):
        # date_str: YYYYMMDD -> DD-MM-YYYY
        self.current_search_date = date_str
        d = date_str
        formatted_date = f"{d[6:8]}-{d[4:6]}-{d[0:4]}"
        url = f"{self.confirmtkt_base}/{source_code}/to/{dest_code}/{formatted_date}"
        print(f"Fetching ConfirmTkt: {url}...")
        
        response = DynamicFetcher.fetch(url, network_idle=True, timeout=60000)
        return self.parse_confirmtkt(response)

    def parse_confirmtkt(self, page):
        trains = {}
        tatkal_open = self.is_tatkal_open(self.current_search_date)
        # Cards are divs with id starting with train-
        cards = page.css('div[id^="train-"]')
        for card in cards:
            num = card.attrib.get('id', '').replace('train-', '')
            name = card.css('.truncate::text').get() # Simple selector for name
            
            classes = []
            # Availability cards
            avail_cards = card.css('div._cache-card-wrapper_662zq_5')
            for ac in avail_cards:
                code = ac.css('span::text').get() # e.g. SL, 3A
                status_main = ac.css('._prediction-text_662zq_115::text').get()
                status_sub = ac.css('.truncate::text').get()
                
                # Check for Tatkal indicator in ConfirmTkt
                # ConfirmTkt often shows TQ or Tatkal in labels
                all_ac_text = " ".join(ac.css("*::text").getall())
                is_tatkal = "TQ" in code or "Tatkal" in all_ac_text
                
                if is_tatkal and not tatkal_open:
                    status = "NOT OPEN (TATKAL)"
                else:
                    status = f"{status_main} ({status_sub})" if status_sub else status_main
                
                fare = ac.css('span.body-xs::text').get()
                if fare and '₹' not in fare: fare = f"₹{fare.strip()}"
                
                if code and len(code) <= 3: # Filter out noise
                    classes.append({"class": code, "status": status, "fare": fare, "source": "ConfirmTkt"})
            
            if num: trains[num] = {"name": name, "classes": classes}
        return trains

def merge_and_rank(paytm_data, ct_data):
    all_nums = set(paytm_data.keys()) | set(ct_data.keys())
    merged_results = []
    
    for num in all_nums:
        p_info = paytm_data.get(num, {})
        c_info = ct_data.get(num, {})
        name = p_info.get('name') or c_info.get('name') or "Unknown"
        
        p_classes = {cl['class']: cl for cl in p_info.get('classes', [])}
        c_classes = {cl['class']: cl for cl in c_info.get('classes', [])}
        
        all_codes = set(p_classes.keys()) | set(c_classes.keys())
        for code in all_codes:
            pc = p_classes.get(code)
            cc = c_classes.get(code)
            
            p_status = str(pc['status']) if pc else ""
            c_status = str(cc['status']) if cc else ""
            
            # Extract official chance
            chance = cc.get('chance') if cc and cc.get('chance') else (pc.get('chance') if pc else "")
            
            final_status = c_status if c_status else p_status
            
            if pc and cc:
                p_is_avl = "AVL" in p_status or "AVAILABLE" in p_status.upper()
                c_is_avl = "AVL" in c_status or "AVAILABLE" in c_status.upper()
                
                if p_is_avl and not c_is_avl:
                    final_status = f"{c_status} (Paytm claimed AVL)"
                elif "NOT OPEN" in p_status:
                    final_status = p_status
            
            fare = cc['fare'] if cc and cc['fare'] else (pc['fare'] if pc else "N/A")
            is_blocked = "NOT OPEN" in final_status or "Regret" in final_status or "No more booking" in final_status
            
            chance_val = 0
            if is_blocked: chance_val = -100
            elif "AVL" in final_status or "AVAILABLE" in final_status.upper(): chance_val = 100
            elif chance and "%" in chance:
                chance_val = int(re.sub(r'[^\d]', '', chance))
            elif "RAC" in final_status: chance_val = 80
            elif "WL" in final_status:
                match = re.search(r'WL\s*(\d+)', final_status)
                wl_num = int(match.group(1)) if match else 100
                chance_val = max(0, 70 - wl_num)
            
            fare_num = int(re.sub(r'[^\d]', '', fare)) if fare and re.sub(r'[^\d]', '', fare).isdigit() else 1000
            score = chance_val * 10 - (fare_num / 100)
            
            merged_results.append({
                "Train": f"{name} ({num})",
                "Class": code,
                "Status": final_status,
                "Chance": chance if chance else f"{chance_val}%",
                "Fare": fare,
                "Score": score,
                "Verified": "Both" if (pc and cc) else ("Paytm" if pc else "ConfirmTkt")
            })
            
    df = pd.DataFrame(merged_results)
    if not df.empty:
        df = df.sort_values(by="Score", ascending=False)
    return df

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", default="ADI")
    parser.add_argument("--dest", default="NDLS")
    parser.add_argument("--date", default="20260503")
    args = parser.parse_args()
    
    scraper = MultiSourceScraper()
    # For Paytm we need the full names usually, but let's try with codes first or map them
    # For ADI/NDLS it works
    p_data = scraper.fetch_paytm(f"{args.source}_Ahmedabad Jn", f"{args.dest}_Delhi- All Stations", args.date)
    c_data = scraper.fetch_confirmtkt(args.source, args.dest, args.date)
    
    results = merge_and_rank(p_data, c_data)
    print("\nCross-Verified Recommended Tickets:")
    print(results.head(15).to_string(index=False))
    
    with open("multi_source_results.json", "w") as f:
        json.dump({"paytm": p_data, "confirmtkt": c_data}, f, indent=4)
