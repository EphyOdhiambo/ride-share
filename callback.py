import requests
import os
from dotenv import load_dotenv

# Load .env variables
load_dotenv()

ACCESS_TOKEN = "YOUR_ACCESS_TOKEN"  # Replace with MPESA API access token
SHORTCODE = os.getenv("MPESA_SHORTCODE")
CALLBACK_URL = os.getenv("MPESA_CALLBACK_URL")

headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Content-Type": "application/json"
}

payload = {
    "ShortCode": SHORTCODE,
    "ResponseType": "Completed",
    "ConfirmationURL": CALLBACK_URL,
    "ValidationURL": CALLBACK_URL
}

response = requests.post("https://sandbox.safaricom.co.ke/mpesa/c2b/v1/registerurl", headers=headers, json=payload)
print(response.json())
