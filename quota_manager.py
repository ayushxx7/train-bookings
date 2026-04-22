import json

def analyze_passengers(passengers_file='passengers.json'):
    try:
        with open(passengers_file, 'r') as f:
            passengers = json.load(f)
    except Exception as e:
        print(f"Error loading passengers: {e}")
        return None

    analysis = {
        "total_passengers": len(passengers),
        "eligible_quotas": {
            "GN": True, # General is always eligible
            "TQ": True, # Tatkal is always eligible
            "SS": False, # Senior Citizen
            "LD": False, # Ladies
        },
        "details": []
    }

    senior_citizens = 0
    females = 0
    males = 0

    for p in passengers:
        age = p.get('age', 0)
        gender = p.get('gender', 'M')
        
        p_quotas = ["GN", "TQ"]
        
        # Senior Citizen: Men 60+, Women 45+ (IRCTC rules)
        is_senior = (gender == 'M' and age >= 60) or (gender == 'F' and age >= 45)
        if is_senior:
            p_quotas.append("SS")
            senior_citizens += 1
            
        # Ladies: Any female
        if gender == 'F':
            p_quotas.append("LD")
            females += 1
        else:
            males += 1
            
        analysis["details"].append({
            "name": p['name'],
            "eligible_quotas": p_quotas
        })

    # Eligibility for Group Booking Quotas:
    
    # Senior Citizen Quota (SS): 
    # Usually available if at least one or two seniors are traveling.
    # IRCTC often allows it if it's 1-2 seniors. 
    # If mixed with young males, SS quota might not apply to the whole group PNR.
    if senior_citizens > 0:
        analysis["eligible_quotas"]["SS"] = True

    # Ladies Quota (LD):
    # Available if ALL adult passengers are female. 
    # Adult males (12+) are NOT allowed in LD quota bookings.
    if males == 0 and females > 0:
        analysis["eligible_quotas"]["LD"] = True
    elif females > 0:
        # Partial support: Female passengers qualify, but adult males don't.
        analysis["eligible_quotas"]["LD_PARTIAL"] = True

    # Recommended Strategy Logic
    if males > 0 and (senior_citizens > 0 or females > 0):
        analysis["strategy"] = "SPLIT"
        analysis["strategy_note"] = (
            f"Mixed group detected. For better chances:\n"
            f"1. Book {senior_citizens} senior(s) + {females if females > 0 else ''} ladies "
            f"under SS or LD quotas.\n"
            f"2. Book remaining {males} male(s) under GN quota."
        )
    else:
        analysis["strategy"] = "SINGLE"
        analysis["strategy_note"] = "All passengers can book together under recommended quota."

    return analysis

if __name__ == "__main__":
    result = analyze_passengers()
    print(json.dumps(result, indent=4))
