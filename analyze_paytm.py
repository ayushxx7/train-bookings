from scrapling import DynamicFetcher
import time

def analyze():
    url = "https://tickets.paytm.com/trains/searchTrains/ADI_Ahmedabad%20Jn/NDLS_Delhi-%20All%20Stations/20260503"
    print(f"Fetching {url}...")
    
    # Using DynamicFetcher for JS rendering
    # The correct way seems to be DynamicFetcher.fetch or similar
    from scrapling.fetchers import DynamicFetcher
    page = DynamicFetcher.fetch(url, network_idle=True, timeout=60000)
    
    # Save the rendered HTML for manual inspection if needed
    # Scrapling Response usually has .text or .html_content
    html_content = ""
    if hasattr(page, 'html_content') and page.html_content:
        html_content = page.html_content
    elif hasattr(page, 'text') and page.text:
        html_content = page.text
    elif hasattr(page, 'body') and page.body:
        html_content = page.body.decode('utf-8') if isinstance(page.body, bytes) else page.body
    
    with open("paytm_rendered.html", "w", encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"Content Length: {len(html_content)}")
    print("Page title:", page.css("title::text").get())
    
    # Let's try to find train cards
    # Paytm often uses classes like '_1z6A' or similar (hashed)
    # But let's look for text like 'ADI' or 'Ahmedabad' or 'Train'
    found_train = "Ahmedabad" in html_content
    print(f"Found 'Ahmedabad' in content: {found_train}")
    
    # Try to find all divs and see which one has more content
    divs = page.css("div").getall()
    print(f"Found {len(divs)} divs.")
    
    # Print some text to see what's there
    print("\nPage Text Preview (first 1000 chars):")
    print(page.text[:1000])

if __name__ == "__main__":
    analyze()
