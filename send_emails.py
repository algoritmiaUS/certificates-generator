import base64
import csv
import os
import re
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv

from Google import Create_Service

load_dotenv()

# Google
CLIENT_SECRET_FILE = "auth.json"
API_NAME = "gmail"
API_VERSION = "v1"
SCOPES = ["https://www.googleapis.com/auth/gmail.send"]

# Personalize
EMAIL = os.getenv("EMAIL", "")
SUBJECT = os.getenv("SUBJECT", "")
MESSAGE = os.getenv("MESSAGE", "")
CSV_FILE_PATH = os.getenv("CSV_FILE_PATH", "./data/participants.csv")
DATE = os.getenv("DATE", "2026-02-13")
OUTPUT_DIR = os.getenv("OUTPUT_DIR", "./out/")


def process_mailing_list(file_name: str):
    """Process the mailing list file and yield dicts with email and file_path."""
    if not os.path.exists(file_name):
        return

    with open(file_name, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row.get("name", "").strip()
            email = row.get("email", "").strip()
            if not name or not email:
                continue

            position = str(row.get("position", "")).strip()
            if position in ("1", "2", "3"):
                prefix = position
            else:
                prefix = "0"

            kebab_name = re.sub(r"\W+", "-", name.casefold()).strip("-")
            filename = f"{prefix}_{DATE}_{kebab_name}_signed.pdf"
            file_path = os.path.join(OUTPUT_DIR, filename)

            if os.path.exists(file_path):
                yield {"email": email, "file_path": file_path}


def send_email(service, to: str, file_path: str):
    """Send an email with the given file attached."""
    filename = os.path.basename(file_path)

    mime_message = MIMEMultipart()
    mime_message["to"] = to
    mime_message["from"] = EMAIL
    mime_message["subject"] = SUBJECT
    mime_message.attach(MIMEText(MESSAGE, "plain"))

    with open(file_path, "rb") as attachment:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())
        encoders.encode_base64(part)

        part.add_header("Content-Disposition", "attachment", filename=filename)
        mime_message.attach(part)

    raw_string = base64.urlsafe_b64encode(mime_message.as_bytes()).decode()
    try:
        m = (
            service.users()
            .messages()
            .send(userId="me", body={"raw": raw_string})
            .execute()
        )
        print(m)
    except Exception as e:
        print(f"Failed to send email to {to}: {e}")


if __name__ == "__main__":
    service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)
    if service is None:
        raise RuntimeError(
            "Failed to create Gmail service. Check authentication, API configuration, and network connectivity."
        )

    for row in process_mailing_list(CSV_FILE_PATH):
        send_email(service, row["email"], row["file_path"])
