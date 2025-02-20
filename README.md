# local-mail
A local mail management agent that fetches and manages emails from your existing email accounts

## Main Components

### 1. Client Layer
- Web Interface

### 2. Core Services
- **Mail Fetcher**
  - Connects to remote email servers (IMAP/POP3)
  - Fetches new emails periodically
  - Manages email synchronization
- **IMAP/POP3 Server**
  - Local mail access
  - Folder management
  - State synchronization

### 3. Storage Layer
- **Primary Database**
  - Email metadata
  - Account configurations
  - Sync status
- **Cache Layer**
  - Frequently accessed emails
  - Search indices
- **File Storage**
  - Email bodies
  - Attachments
  - Backup storage

## Diagram
```mermaid
graph TB
subgraph Client["Client Layer"]
WC["Web Client"]
end

subgraph Core["Core Services"]
MF["Mail Fetcher"]
IMAP["IMAP/POP3 Server"]
INDEX["Search/Index Service"]
end

subgraph Storage["Storage Layer"]
DB[(Primary Database)]
CACHE["Cache Layer"]
FS["File Storage"]
end

subgraph Remote["Remote Mail Servers"]
RS["Gmail/Outlook/etc"]
end

Remote --> MF
MF --> Storage
Client --> IMAP
IMAP --> Storage
```

## TODOS
- [ ] Implementation of mail fetcher
- [ ] Storage system design
- [ ] Client interface development
- [ ] Email provider integration
- [ ] Sync status tracking
