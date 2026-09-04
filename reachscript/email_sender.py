import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from .errors import RuntimeError

from dotenv import load_dotenv

load_dotenv()


class EmailSender:

    def send(
        self,
        lead,
        email,
        subject="",
        sender_name="ReachScript",
        dry_run=True
    ):

        if not lead:
            print("✗ No lead available")
            return False

        if not email:
            print("✗ No email available")
            return False

        recipient = lead.get("email", "").strip()

        if not recipient:
            lead_name = lead.get("name", "Unknown")

            raise RuntimeError(
                f"Lead '{lead_name}' does not have an email address. "
                f"Add an 'email' column to your leads CSV."
            )

        # -------------------------
        # DRY RUN
        # -------------------------

        if dry_run:

            print("\n📧 EMAIL READY TO SEND")
            print(f"From: {sender_name}")
            print(f"To: {recipient}")
            print(f"Subject: {subject}")
            print("Status: DRY RUN")
            print("Email was NOT actually sent.")

            return True

        # -------------------------
        # REAL EMAIL
        # -------------------------

        email_address = os.getenv("EMAIL_ADDRESS")
        app_password = os.getenv("EMAIL_APP_PASSWORD")

        if not email_address or not app_password:
            print(
                "✗ Email credentials are not configured"
            )
            return False

        try:

            message = MIMEMultipart()

            message["From"] = f"{sender_name} <{email_address}>"
            message["To"] = recipient
            message["Subject"] = subject

            message.attach(
                MIMEText(email, "plain")
            )

            with smtplib.SMTP(
                "smtp.gmail.com",
                587
            ) as server:

                server.starttls()

                server.login(
                    email_address,
                    app_password
                )

                server.send_message(message)

            print("\n📧 EMAIL SENT SUCCESSFULLY")
            print(f"From: {sender_name}")
            print(f"To: {recipient}")
            print(f"Subject: {subject}")

            return True

        except Exception as error:

            print(
                f"✗ Email sending failed: {error}"
            )

            return False