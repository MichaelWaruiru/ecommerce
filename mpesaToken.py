import requests
import base64

consumer_key = "zuX4O3IsL0UZyGdkQtmUpp7UupDjHkMf"
consumer_secret = "wr2EReiPnJKrFFRA"

def get_access_token():
    url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
    auth_header = base64.b64encode(f"{consumer_key}:{consumer_secret}".encode()).decode()

    headers = {
        "Authorization": f"Basic {auth_header}",
        "Content-Type": "application/json"
    }

    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"Unexpected status code: {response.status_code}")

    token_response = response.json()
    return token_response.get("access_token")

try:
    access_token = get_access_token()
    print(f"Access token: {access_token}")
except Exception as e:
    print(f"Error: {e}")