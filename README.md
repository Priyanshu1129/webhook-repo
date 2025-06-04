# GitHub Webhook Event Monitor

## 📌 Overview

A real-time system that captures GitHub events (push, pull requests, merges) via webhooks, stores them in MongoDB, and displays them in a clean UI. Implements smart polling to only show new events without duplicates.

## 🏗️ Architecture

```
GitHub Repository (action-repo)
       ↓ (Webhook)
Flask Backend (webhook-server)
       ↓ (MongoDB)
React Frontend (webhook-client)
```

## ✨ Key Features

### 1. Smart Event Tracking
- **last_fetch_timestamp System**  
  - Tracks the most recent event timestamp sent to the frontend inside database.  
  - Ensures only new events are returned on each poll  
  - Prevents duplicate notifications  

### 2. Efficient Data Flow
- Backend only processes essential fields  
- Frontend polls every 15 seconds for updates  
- Timestamps are consistently handled in UTC  

### 3. Precise Event Display
Formats events exactly as required:

```
"User" pushed to "main" on 3rd June 2025 - 6:22 PM UTC  
"User" merged "feature" to "main" on 3rd June 2025 - 6:25 PM UTC  
```

---

## 📂 Repository Structure

```
webhook/
├── webhook-server/   → Flask backend
├── webhook-client/   → React frontend
└── README.md          → (This file)
```

- **action-repo** (external GitHub repo)  
  GitHub repo that triggers webhook events (push, PR, merge)

- **webhook-repo** (this repo)  
  Contains both frontend and backend apps working together

---

## 🛠️ Project Setup

Each part has its own setup guide:

- 🔧 **[Backend Setup Instructions →](./webhook-server/README.md)**
- 💻 **[Frontend Setup Instructions →](./webhook-client/README.md)**

---

## ⚙️ How It Works

1. **Webhook Reception**
   - GitHub sends events to `/webhook/receiver`
   - Backend parses and stores event data in MongoDB

2. **Smart Polling**
   - Frontend polls `/webhook/notifications` every 15 seconds
   - Backend returns only new events using `last_fetch_timestamp`

3. **UI Display**
   - Clean display of events in desired formats
   - Newest events on top, no duplicates shown on refresh

---

## ✅ Requirements Met

- [x] Minimal data extracted from webhooks  
- [x] Precise UTC time handling  
- [x] No duplicate events displayed  
- [x] Clean, auto-updating frontend UI  
- [x] Smart polling strategy  
- [x] Clear separation between client and server  

---
