import imaplib
import email
import os
from email.header import decode_header
from datetime import datetime
from typing import Dict, List, Optional
from dotenv import load_dotenv

class MailFetcher:
    def __init__(self, email_addr: str, password: str, imap_server: str = "imap.gmail.com"):
        self.email = email_addr
        self.password = password
        self.imap_server = imap_server
        self.connection: Optional[imaplib.IMAP4_SSL] = None

    def connect(self) -> bool:
        """Establish connection to IMAP server"""
        try:
            self.connection = imaplib.IMAP4_SSL(self.imap_server)
            self.connection.login(self.email, self.password)
            return True
        except Exception as e:
            print(f"Connection failed: {str(e)}")
            return False

    def disconnect(self):
        """Close IMAP connection"""
        if self.connection:
            try:
                self.connection.close()
                self.connection.logout()
            except:
                pass

    def fetch_emails(self, folder: str = "INBOX", limit: int = 10) -> List[Dict]:
        """Fetch emails from specified folder"""
        if not self.connection:
            if not self.connect():
                return []

        emails = []
        try:
            # Select the mailbox
            self.connection.select(folder)

            # Search for all emails
            _, message_numbers = self.connection.search(None, "ALL")
            
            # Get the list of email IDs
            email_ids = message_numbers[0].split()
            
            # Fetch last 'limit' number of emails
            for num in email_ids[-limit:]:
                _, msg_data = self.connection.fetch(num, "(RFC822)")
                email_body = msg_data[0][1]
                email_message = email.message_from_bytes(email_body)

                # Extract basic email information
                subject = decode_header(email_message["subject"])[0][0]
                if isinstance(subject, bytes):
                    subject = subject.decode()
                
                from_ = email_message["from"]
                date_str = email_message["date"]
                
                # Get email content
                body = ""
                if email_message.is_multipart():
                    for part in email_message.walk():
                        if part.get_content_type() == "text/plain":
                            body = part.get_payload(decode=True).decode()
                            break
                else:
                    body = email_message.get_payload(decode=True).decode()

                emails.append({
                    "id": num.decode(),
                    "subject": subject,
                    "from": from_,
                    "date": date_str,
                    "body": body
                })

            return emails

        except Exception as e:
            print(f"Error fetching emails: {str(e)}")
            return []
        finally:
            self.disconnect()

# Example usage
if __name__ == "__main__":
    load_dotenv()  # Add this line to load .env file
    
    # For Gmail, you need to create an App Password if 2FA is enabled
    # Go to Google Account > Security > 2-Step Verification > App passwords
    EMAIL = os.getenv("EMAIL")
    PASSWORD = os.getenv("EMAIL_PASSWORD")  # App password for Gmail

    fetcher = MailFetcher(EMAIL, PASSWORD)
    emails = fetcher.fetch_emails(limit=5)
    
    for email in emails:
        print(f"\nSubject: {email['subject']}")
        print(f"From: {email['from']}")
        print(f"Date: {email['date']}")
        print("-" * 50) 