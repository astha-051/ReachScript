from reachscript.email_sender import EmailSender
from reachscript.errors import RuntimeError

import os

print("Email:", os.getenv("EMAIL_ADDRESS"))
print("App password loaded:", bool(os.getenv("EMAIL_APP_PASSWORD")))

sender = EmailSender()

lead = {
    "name": "Rahul",
    "company": "Google",
    "email": ""
}

email = """Hi Rahul,

This is a real email test from ReachScript.

Best,
ReachScript AI
"""

try:
    sender.send(
        lead,
        email,
        subject="Test",
        sender_name="ReachScript AI",
        dry_run=True
    )

except RuntimeError as error:
    print("\nReachScript Error:")
    print(error)