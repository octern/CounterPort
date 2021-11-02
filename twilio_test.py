from twilio.rest import Client

# Your Account SID from twilio.com/console
account_sid = "AC2a66527d72862390f682c06f675e5f2f"
# Your Auth Token from twilio.com/console
auth_token  = "2458cecfa7f30c0138d1d2ff5038af37"

client = Client(account_sid, auth_token)

message = client.messages.create(
    to="+17348461308",
    from_="+17344188998",
    body="Hello from Python!")

print(message.sid)
