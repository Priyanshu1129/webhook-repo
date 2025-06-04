# Webhook Server (Flask + MongoDB)

This backend receives GitHub Webhook events (`push`, `pull_request`, `merge`) from a GitHub repository, processes the data, and stores it in MongoDB.

---

## 🚀 Features

- Receives GitHub webhook events via `/webhook/receiver`
- Handles `push`, `pull_request`, and `merge` events
- Stores structured data in MongoDB
- Exposes a `/webhook/notifications` API for frontend polling

---

## 🔧 Setup Instructions

### 1. Navigate to the server folder

```bash
cd webhook/webhook-server
```

### 2. Create and activate a virtual environment

```bash
# Install virtualenv if not already installed
pip install virtualenv

# Create virtual environment
virtualenv venv

# Activate virtual environment (Linux/macOS)
source venv/bin/activate

# On Windows (use this instead)
venv\Scripts\activate
```

---

### 3. Create a `.env` file

Add your MongoDB connection string:

```env
MONGO_URI=mongodb://localhost:27017/webhook_db
```

If you're using MongoDB Atlas, replace the URI accordingly.

---

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

---

### 5. Start the Flask server

```bash
python run.py
```

Server will start at:

```
http://localhost:5000
```

---

## 🌐 Expose Server Publicly via Ngrok

Use [Ngrok](https://ngrok.com/) to expose your local Flask server to GitHub:

```bash
ngrok http 5000
```

Copy the HTTPS URL it gives (e.g., `https://abc.ngrok-free.app`).

---

## 🔁 Configure GitHub Webhook

In your GitHub repository:

1. Go to **Settings → Webhooks → Add webhook**
2. Set:

   * **Payload URL:** `https://abc.ngrok-free.app/webhook/receiver`
   * **Content type:** `application/json`
   * **Events:** Choose `Just the push event` and `Pull requests`
3. Click **Add Webhook**

> GitHub will now send webhook events to your Flask server via Ngrok.

---

## 🧾 MongoDB Schema (Example Document)

```json
{
  "author": "Travis",
  "action": "PUSH",
  "from_branch": null,
  "to_branch": "main",
  "timestamp": "2021-04-01T21:30:00Z"
}
```

---

## 📡 API Endpoint for Frontend

The frontend polls this endpoint every 15 seconds:

```http
GET /webhook/notifications
```

---

## ✅ Summary

* Flask backend to receive and process GitHub webhooks
* Stores structured data in MongoDB
* Exposed to GitHub via Ngrok
* Frontend polls `/webhook/notifications` to display data


