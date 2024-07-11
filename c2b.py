from mpesaToken import *
import json


def c2b_payment(token):
    url = "https://sandbox.safaricom.co.ke/mpesa/c2b/v1/registerurl"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    payload = {
        "ShortCode": 600981,
        "ResponseType": "Completed",
        "ConfirmationURL": "https://mydomain.com/confirmation",
        "ValidationURL": "https://mydomain.com/validation"
    }

    response = requests.post(url, headers=headers, data=json.dumps(payload))

    if response.status_code != 200:
        print(f"Unexpected status code: {response.status_code}")
        print(response.text)
        return

    print(response.json())

try:
    access_token = get_access_token()
    print("Executing C2B payment...")
    c2b_payment(access_token)
except Exception as e:
    print(f"Error: {e}")