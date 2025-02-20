from dataclasses import dataclass
from typing import Dict

@dataclass
class EmailConfig:
    email: str
    password: str
    imap_server: str
    port: int = 993

@dataclass
class Config:
    accounts: Dict[str, EmailConfig]
    fetch_interval: int = 300  # seconds
    max_emails_per_fetch: int = 100
    storage_path: str = "./storage" 