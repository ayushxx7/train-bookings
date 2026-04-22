from scrapling.fetchers import DynamicSession

def analyze_confirmtkt():
    url = "https://www.confirmtkt.com/rbooking/trains/from/ADI/to/NDLS/03-05-2026"
    print(f"Fetching {url}...")
    
    with DynamicSession(headless=True) as session:
        response = session.fetch(url, network_idle=True)
        html_content = response.text or response.html_content or ""
        
        print(f"Content length: {len(html_content)}")
        with open("confirmtkt_rendered.html", "w", encoding='utf-8') as f:
            f.write(html_content)
        
        # Check for some text
        if "Ashram" in html_content:
            print("Found 'Ashram' in HTML")
        else:
            print("Did not find 'Ashram' in HTML")

if __name__ == "__main__":
    analyze_confirmtkt()

if __name__ == "__main__":
    analyze_confirmtkt()
