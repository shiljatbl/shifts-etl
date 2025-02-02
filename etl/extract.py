import requests

def fetch_shifts(base_url="http://localhost:8000"):
    
    # Fetches all shifts from the Shift API.
    # Handles pagination to retrieve all records.
    
    shifts = []
    next_page = "/api/shifts"  # Initial endpoint
    while next_page:
        try:
            response = requests.get(f"{base_url}{next_page}")
            response.raise_for_status()  # Raise an error for bad status codes
            data = response.json()
            shifts.extend(data['results'])  # Extract shifts from the 'results' key
            next_page = data['links'].get('next')  # Get the next page URL
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data from API: {e}")
            break
    return shifts