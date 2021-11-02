from twilio.rest import client
import sys

# Your Account SID from twilio.com/console
account_sid = "AC2a66527d72862390f682c06f675e5f2f"
# Your Auth Token from twilio.com/console
auth_token  = sys.argv[1]

client = Client(account_sid, auth_token)

message = client.messages.create(
    to="+17348461308",
    from_="+17344188998",
    body="Hello from Python!")

print(message.sid)
