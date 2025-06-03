import { useEffect, useState, useRef } from "react";

const POLL_INTERVAL = 15000; // 15 seconds
const API_URL = "http://localhost:5000/webhook/notifications";

function formatDate(isoString) {
  // 1. Force UTC interpretation
  if (!isoString.endsWith("Z") && !isoString.includes("+")) {
    isoString += "Z";
  }

  const date = new Date(isoString);

  if (isNaN(date.getTime())) {
    return "Invalid date";
  }

  const day = date.getUTCDate();
  const daySuffix =
    day % 10 === 1 && day !== 11
      ? "st"
      : day % 10 === 2 && day !== 12
      ? "nd"
      : day % 10 === 3 && day !== 13
      ? "rd"
      : "th";

  const month = date.toLocaleString("en-US", {
    month: "long",
    timeZone: "UTC",
  });

  const hours = date.getUTCHours();
  const minutes = date.getUTCMinutes().toString().padStart(2, "0");
  const ampm = hours >= 12 ? "PM" : "AM";
  const formattedHour = hours % 12 || 12;

  return `${day}${daySuffix} ${month} ${date.getUTCFullYear()} - ${formattedHour}:${minutes} ${ampm} UTC`;
}

function formatNotification(event) {
  const { action, author, from_branch, to_branch, timestamp } = event;

  // Skip if required fields are missing
  if (!author || !timestamp) return null;

  const time = formatDate(timestamp);

  switch (action) {
    case "PUSH":
      return to_branch
        ? `"${author}" pushed to "${to_branch}" on ${time}`
        : null;
    case "PULL_REQUEST":
      return from_branch && to_branch
        ? `"${author}" submitted a pull request from "${from_branch}" to "${to_branch}" on ${time}`
        : null;
    case "MERGE":
      return from_branch && to_branch
        ? `"${author}" merged branch "${from_branch}" to "${to_branch}" on ${time}`
        : null;
    default:
      return null;
  }
}

export default function App() {
  const [events, setEvents] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchEvents = async () => {
    try {
      setIsLoading(true);
      const response = await fetch(API_URL);

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();

      // Filter out any invalid or incomplete events
      const validEvents = data
        .map((event) => ({
          ...event,
          displayText: formatNotification(event),
        }))
        .filter((event) => event.displayText !== null);

      setEvents((prevEvents) => [...validEvents, ...prevEvents]);
      setError(null);
    } catch (err) {
      setError("Failed to load events. Please try again later.");
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    // Initial fetch
    fetchEvents();

    // Set up polling
    const interval = setInterval(fetchEvents, POLL_INTERVAL);

    // Cleanup
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="min-h-screen bg-gray-100 p-4">
      <h1 className="text-2xl font-bold text-blue-600 mb-4">
        GitHub Webhook Events
      </h1>

      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
          {error}
        </div>
      )}

      {isLoading && events.length === 0 ? (
        <p className="text-gray-500">Loading events...</p>
      ) : events.length === 0 ? (
        <p className="text-gray-500">No events yet.</p>
      ) : (
        <div className="space-y-3">
          {events.map((event) => (
            <div
              key={`${event.request_id}-${event.timestamp}`}
              className="bg-white shadow rounded-xl p-4 border border-gray-200"
            >
              <p className="text-gray-800">{event.displayText}</p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
