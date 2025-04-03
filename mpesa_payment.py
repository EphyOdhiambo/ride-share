import requests
import base64
import datetime

# 🔹 M-Pesa API Credentials (Replace with your actual credentials)
CONSUMER_KEY = "ABXKNk8886Mxg83352DQLMayPmxJEctmAHv1JSCQ7artGAml"
CONSUMER_SECRET = "MtLmIHFR5HvNLQ6r7Jry4R7JAn8sJADjkCmGLnEtjzraMppo0ShlJ7eGfanfgoCC"
BUSINESS_SHORTCODE = "0717289262"
LIPA_NA_MPESA_PASSKEY = "bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919"

# 🔹 Safaricom API URLs
TOKEN_URL = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
STK_PUSH_URL = "https://sandbox.safaricom.co.ke/mpesa/b2c/v3/paymentrequest"
CALLBACK_URL = "https://6500-197-232-62-237.ngrok-free.app"  # Replace with Ngrok URL

# 🔹 Function to Get M-Pesa Access Token
def get_access_token():
    credentials = f"{CONSUMER_KEY}:{CONSUMER_SECRET}"
    encoded_credentials = base64.b64encode(credentials.encode()).decode()

    headers = {
        "Authorization": f"Basic {encoded_credentials}"
    }

    response = requests.get(TOKEN_URL, headers=headers)
    
    if response.status_code == 200:
        access_token = response.json().get("access_token")
        return access_token
    else:
        print("❌ Failed to get access token:", response.text)
        raise Exception("Failed to get access token")

# 🔹 Function to Format Phone Number Correctly (07XX... → 2547XX...)
def format_phone_number(phone):
    phone = phone.strip()  # Remove spaces
    if phone.startswith("0"):  
        phone = "254" + phone[1:]
    elif phone.startswith("+254"):  
        phone = phone[1:]
    return phone

# 🔹 Function to Generate Timestamp & Password
def generate_password():
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")  # Generate dynamic timestamp
    data_to_encode = BUSINESS_SHORTCODE + LIPA_NA_MPESA_PASSKEY + timestamp
    encoded_password = base64.b64encode(data_to_encode.encode()).decode()
    return encoded_password, timestamp

# 🔹 Function to Send STK Push Request
def send_stk_push(phone, amount):
    try:
        access_token = get_access_token()  # Get the access token
        phone = format_phone_number(phone)  # Format phone number correctly
        password, timestamp = generate_password()  # Generate password and timestamp

        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }

        payload = {
    "BusinessShortCode": 174379,
    "Password": "MTc0Mzc5YmZiMjc5ZjlhYTliZGJjZjE1OGU5N2RkNzFhNDY3Y2QyZTBjODkzMDU5YjEwZjc4ZTZiNzJhZGExZWQyYzkxOTIwMjUwMzEzMTc0MDUx",
    "Timestamp": "20250313174051",
    "TransactionType": "CustomerPayBillOnline",
    "Amount": 1,
    "PartyA": 254708374149,
    "PartyB": 174379,
    "PhoneNumber": 254717289262,
    "CallBackURL": "https://mydomain.com/path",
    "AccountReference": "CompanyXLTD",
    "TransactionDesc": "Payment of X" 
  }

        response = requests.post(STK_PUSH_URL, json=payload, headers=headers)

        if response.status_code == 200:
            return response.json()
        else:
            print("❌ STK Push Request Failed:", response.text)
            return None
    except Exception as e:
        print(f"❌ Error in STK Push: {e}")
        return None

# 🔹 Example: Initiate Payment (Test)
if __name__ == "__main__":
    phone = "0717289262"  # Replace with actual phone number
    amount = 100  # Example amount

    print("📤 Sending STK Push Request...")
    response = send_stk_push(phone, amount)

    if response:
        print("✅ STK Push Response:", response)
    else:
        print("❌ Payment Failed! Check logs.")
