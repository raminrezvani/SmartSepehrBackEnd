import requests
import json
import urllib3

# Disable insecure request warnings (use cautiously)
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def call_api(url, params):
    """
    Calls an API endpoint with the given parameters and returns the JSON response.

    Args:
        url (str): The URL of the API endpoint.
        params (dict): A dictionary of parameters to send with the request.

    Returns:
        dict or None: The JSON response from the API, or None if an error occurs.
    """
    try:
        # Set verify=False if you need to bypass SSL verification (not recommended for production)
        response = requests.get(url, params=params, timeout=30, verify=False)
        response.raise_for_status() # Raise an exception for bad status codes (4xx or 5xx)
        return response.json()
    except requests.exceptions.Timeout:
        print(f"API request timed out for URL: {url}")
        return None
    except requests.exceptions.RequestException as e:
        print(f"API request failed: {e}")
        return None
    except json.JSONDecodeError:
        print(f"Failed to decode JSON response from URL: {url}")
        return None

def main():
    """
    Main function to call the Alwin Hotels API.
    """
    # api_url = "http://45.149.76.168:5053/alwin_hotels"
    api_url = "http://localhost:5055/alwin_hotels"

    # --- Define your parameters here ---
    # Example parameters (replace with actual values)
    parameters = {
        'startdate': '2025-05-13', # Example start date
        'end_date': '2025-05-16',   # Example end date
        'adults': 2,               # Example number of adults
        'target': 'KIH',           # Example target (e.g., city or hotel code)
        'isAnalysis': '1' ,
        'hotelstarAnalysis': json.dumps(['فلامینگو']),
        'priorityTimestamp': 1,
        'use_cache': True,

        # Add any other required parameters
    }
    # ------------------------------------

    print(f"Calling API: {api_url}")
    print(f"With parameters: {parameters}")

    data = call_api(api_url, parameters)

    if data:
        print("\nAPI Response:")
        # Pretty print the JSON data
        print(json.dumps(data, indent=4, ensure_ascii=False))
    else:
        print("\nFailed to retrieve data from the API.")

if __name__ == "__main__":
    main()