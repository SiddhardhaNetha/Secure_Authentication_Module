import random
from twilio.rest import Client

# Temporary OTP store
otp_store = {}

# Twilio credentials (replace with your own)
TWILIO_ACCOUNT_SID = "ACfeb8911748075308243e0e8ebaec754d"
TWILIO_AUTH_TOKEN = "acc8b29f0a336eb0c5da86f5c7229c0e"
TWILIO_PHONE = "+1 218 595 2039"  # Your Twilio number with +country code

client = Client("ACfeb8911748075308243e0e8ebaec754d", "acc8b29f0a336eb0c5da86f5c7229c0e")

def send_otp(mobile):
    otp = str(random.randint(100000, 999999))
    otp_store[mobile] = otp
    try:
        client.messages.create(
            body=f"Your OTP is: {otp}",
            from_=TWILIO_PHONE,
            to=mobile
        )
        print(f"OTP sent to {mobile}: {otp}") # debug in terminal
        return True
    except Exception as e:
        print("Failed to send OTP:", e)
        return False

def verify_otp(mobile, entered_otp):
    correct = otp_store.get(mobile)
    if correct and entered_otp == correct:
        del otp_store[mobile]
        return True
    return False

