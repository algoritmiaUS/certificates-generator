import base64
import os
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path

import polars as pl

from Google import Create_Service
from create_certificates import DATE, OUTPUT_DIR

# Google
CLIENT_SECRET_FILE = "auth.json"
API_NAME = "gmail"
API_VERSION = "v1"
SCOPES = ["https://mail.google.com/"]

# Personalize
EMAIL = ""
SUBJECT = ""
MESSAGE = ""
MAILING_LIST_FILE = "archivo.xlsx"
COLUMNS = [0, 1]


def process_mailing_list(file_name: str) -> pl.DataFrame:
    """Process the mailing list file and return a DataFrame with key and email columns."""
    path = Path(file_name)
    if path.suffix == ".csv":
        df = pl.read_csv(path, columns=COLUMNS)
    else:
        df = pl.read_excel(path, columns=COLUMNS)

    cols = df.columns
    df_names = pl.concat(
        [
            df.select([pl.col(cols[0]).alias("key"), pl.col(cols[1]).alias("email")]),
        ]
    )

    df_processed = (
        df_names.drop_nulls(subset=["key"])
        .with_columns(
            pl.col("key")
            .cast(pl.Utf8)
            .str.strip_chars()
            .str.to_lowercase()
            .str.replace_all(r"\W+", "-")
            .str.strip_chars("-")
            .alias("key_clean")
        )
        .with_columns(
            file_path=pl.lit(OUTPUT_DIR + DATE)
            + "_"
            + pl.col("key_clean")
            + "_signed.pdf"
        )
        .with_columns(
            exists=pl.col("file_path").map_elements(
                lambda p: Path(p).exists(), return_dtype=pl.Boolean
            )
        )
        .filter(pl.col("exists"))
        .unique(subset=["key_clean"])
    )

    return df_processed


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
    m = service.users().messages().send(userId="me", body={"raw": raw_string}).execute()
    print(m)


if __name__ == "__main__":
    service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)
    df_mailings = process_mailing_list(MAILING_LIST_FILE)
    for row in df_mailings.iter_rows(named=True):
        send_email(service, row["email"], row["file_path"])
