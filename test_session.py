from scrapling.fetchers import DynamicSession

def test_session():
    url = "https://tickets.paytm.com/trains/searchTrains/ADI_Ahmedabad%20Jn/NDLS_Delhi-%20All%20Stations/20260503"
    with DynamicSession(headless=True) as session:
        page = session.fetch(url, network_idle=True)
        print("Session attributes:", dir(session))
        # Check if there is a 'page' or similar
        if hasattr(session, 'page'):
            print("Page attributes:", dir(session.page))

if __name__ == "__main__":
    test_session()
