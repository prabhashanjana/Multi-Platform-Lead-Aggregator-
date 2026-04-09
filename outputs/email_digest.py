import pandas as pd
from config import GMAIL_ADDRESS, GMAIL_APP_PASSWORD
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from config import logger


def build_html(df: pd.DataFrame) -> str:
    rows = ""
    for _, row in df.iterrows():
        rows += f"""
        <tr>
            <td>{row['source']}</td>
            <td>{row['title']}</td>
            <td>{row['price']}</td>
            <td>{row['location']}</td>
            <td>{row['posted_at']}</td>
            <td><a href="{row['url']}">View</a></td>
        </tr>
        """
    html = f"""
    <html><body>
    <h2>🏠 Morning Lead Digest — {len(df)} new leads</h2>
    <table border="1" cellpadding="6">
        <tr>
            <th>Source</th><th>Title</th><th>Price</th>
            <th>Location</th><th>Posted At</th><th>URL</th>
        </tr>
        {rows}
    </table>
    </body></html>
    """
    return html


def build_email(html: str, count: int):
    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"🏠 Morning Lead Digest — {count} new leads"
    msg["From"] = GMAIL_ADDRESS
    msg["To"] = GMAIL_ADDRESS
    msg.attach(MIMEText(html, "html"))
    return msg


def send_email(msg):
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(GMAIL_ADDRESS, GMAIL_APP_PASSWORD)
            server.sendmail(GMAIL_ADDRESS, GMAIL_ADDRESS, msg.as_string())
            logger.info(f"Email sent to {GMAIL_ADDRESS}")
    except Exception as e:
        logger.exception(f"Failed to send email: {e}")
        raise


def send_digest(df: pd.DataFrame) -> None:
    if df.empty:
        logger.info("No leads to send")
        return
    html = build_html(df)
    msg = build_email(html, len(df))
    send_email(msg)
