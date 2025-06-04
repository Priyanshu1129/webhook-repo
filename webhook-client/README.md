# Webhook Client (React)

This React frontend polls the backend every 15 seconds to display GitHub webhook events such as `push`, `pull_request`, and `merge` in a clean, real-time feed.

It receives only **new events**, maintains a **local event history** (until page refresh), and ensures **no duplicate notifications** are displayed.

---

## 🎯 Features

- Polls backend `/webhook/notifications` every 15 seconds
- Displays real-time GitHub activity updates
- Clean and minimal UI using React + Tailwind CSS
- Stores new events locally to avoid re-displaying the same notifications

---

## 🔧 Setup Instructions

### 1. Navigate to the client folder

```bash
cd webhook/webhook-client
````

---

### 2. Install dependencies

```bash
npm install
```

---

### 3. Update Backend API URL (if using Ngrok)

By default, the frontend fetches from:

```js
http://localhost:5000/webhook/notifications
```

If you're using Ngrok, replace it with your public URL:

In `src/App.jsx` (or the file where the fetch call is made):

```js
const API_URL = "https://abc.ngrok-free.app/webhook/notifications";
```

---

### 4. Start the development server

```bash
npm run dev
```

The app will typically run at:

```
http://localhost:5173
```

---

## 🧪 Output Format in UI

Sample display formats for GitHub events:

* `"Travis" pushed to "staging" on 1st April 2021 - 9:30 PM UTC`
* `"Travis" submitted a pull request from "staging" to "master" on 1st April 2021 - 9:00 AM UTC`
* `"Travis" merged branch "dev" to "master" on 2nd April 2021 - 12:00 PM UTC`

---

## 🔁 Polling Strategy

The frontend polls this endpoint every 15 seconds:

```http
GET /webhook/notifications
```

It only adds **new events** based on time and content to avoid duplicates.

---

## ✅ Summary

* React frontend with real-time GitHub webhook updates
* Periodic polling of Flask backend
* Works seamlessly with Flask server exposed via Ngrok


