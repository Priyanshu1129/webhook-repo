```markdown
# Webhook Client (React)

This React frontend polls the backend every 15 seconds to display GitHub webhook events such as `push`, `pull_request`, and `merge` in a clean format.
Only fetch the new events and maintain history of events on frontend until page not refreshed. Also ensure no re-displaying of same notification.

## 🎯 Features

- Polls backend `/webhook/notifications` every 15 seconds
- Displays real-time GitHub activity updates
- Clean and minimal UI with React + Tailwind CSS

---

## 🔧 Setup Instructions

### 1. Navigate to the client folder

```bash
cd webhook/webhook-client
````

### 2. Install dependencies

```bash
npm install
```

---

### 3. Update Backend API URL (if using Ngrok)

By default, the frontend fetches data from:

```js
http://localhost:5000/webhook/notifications
```

If you're using Ngrok, replace it with your public URL:

In `src/App.jsx` or wherever the API call is defined:

```js
const API_URL = "https://your-ngrok-url/webhook/notifications";
```

---

### 4. Start the development server

```bash
npm run dev
```

The app will be available at `http://localhost:5173` (or similar).

---

## 🧪 Output Format in UI

Displayed formats for GitHub events:

* `"Travis" pushed to "staging" on 1st April 2021 - 9:30 PM UTC`
* `"Travis" submitted a pull request from "staging" to "master" on 1st April 2021 - 9:00 AM UTC`
* `"Travis" merged branch "dev" to "master" on 2nd April 2021 - 12:00 PM UTC`

---

## 🔁 Polling Strategy

The app uses a 15-second polling interval to fetch only new events:

```
GET /webhook/notifications
```

---

## ✅ Summary

* React frontend with periodic data polling
* Displays GitHub webhook activity live
* Works with the Flask backend exposed via Ngrok

---

```