from flask import Blueprint, request, current_app, jsonify
from datetime import datetime
from dateutil import parser
from pymongo import DESCENDING
import pytz
import traceback

webhook = Blueprint('Webhook', __name__, url_prefix='/webhook')

# Constants
LAST_FETCH_COLLECTION = "last_fetch_timestamp"
EVENTS_COLLECTION = "webhook_events"


def to_utc(timestamp_str):
    """Convert GitHub timestamp to UTC (they're already UTC)"""
    try:
        if not timestamp_str:
            return None
            
        # Parse ISO format (handles Z timezone automatically)
        dt = parser.isoparse(timestamp_str)
        
        # If no timezone is present (unlikely for GitHub), assume UTC
        if dt.tzinfo is None:
            return dt.replace(tzinfo=pytz.UTC)
            
        # Convert to UTC (no-op if already UTC)
        return dt.astimezone(pytz.UTC)
    except Exception as e:
        current_app.logger.error(f"[Timestamp Conversion Error] {e}")
        return None
    
def update_last_fetch_timestamp(db, timestamp):
    """Store the last fetched timestamp in MongoDB"""
    try:
        db[LAST_FETCH_COLLECTION].update_one(
            {"_id": "last_fetch"},
            {"$set": {"timestamp": timestamp}},
            upsert=True
        )
    except Exception as e:
        current_app.logger.error(f"[Last Fetch Update Error] {e}")

def get_last_fetch_timestamp(db):
    """Retrieve the last fetched timestamp from MongoDB"""
    try:
        record = db[LAST_FETCH_COLLECTION].find_one({"_id": "last_fetch"})
        return record.get("timestamp") if record else None
    except Exception as e:
        current_app.logger.error(f"[Last Fetch Retrieve Error] {e}")
        return None

@webhook.route('/receiver', methods=["POST"])
def receiver():
    try:
        payload = request.json
        event_type = request.headers.get('X-GitHub-Event')
        mongo = current_app.extensions.get('pymongo')

        if not mongo:
            return jsonify({"error": "MongoDB not initialized"}), 500
        if not payload or not event_type:
            return jsonify({"error": "Invalid payload or event type"}), 400

        db = mongo.db
        action_doc = None

        # Handle push event
        if event_type == 'push':
            author = payload.get('pusher', {}).get('name')
            to_branch = payload.get('ref', '').split('/')[-1]
            timestamp = to_utc(payload.get('head_commit', {}).get('timestamp'))

            if not all([author, to_branch, timestamp]):
                return jsonify({"error": "Missing required push event data"}), 400

            action_doc = {
                "request_id": payload.get('head_commit', {}).get('id'),
                "author": author,
                "action": "PUSH",
                "from_branch": None,
                "to_branch": to_branch,
                "timestamp": timestamp,
            }

        # Handle pull request event
        elif event_type == 'pull_request':
            pr = payload.get('pull_request', {})
            author = pr.get('user', {}).get('login')
            from_branch = pr.get('head', {}).get('ref')
            to_branch = pr.get('base', {}).get('ref')

            if payload.get('action') == 'closed' and pr.get('merged'):
                timestamp = to_utc(pr.get('merged_at'))
                action_type = "MERGE"
            else:
                timestamp = to_utc(pr.get('created_at'))
                action_type = "PULL_REQUEST"

            if not all([author, from_branch, to_branch, timestamp]):
                return jsonify({"error": "Missing required PR event data"}), 400

            action_doc = {
                "request_id": str(pr.get('id')),
                "author": author,
                "action": action_type,
                "from_branch": from_branch,
                "to_branch": to_branch,
                "timestamp": timestamp,
            }

        if action_doc:
            db[EVENTS_COLLECTION].insert_one(action_doc)
            current_app.logger.info(f"Event stored: {action_doc}")
            return jsonify({"status": "success"}), 200

        return jsonify({"error": "Unsupported event type"}), 400

    except Exception as e:
        current_app.logger.error(f"[Webhook Error] {str(e)}")
        traceback.print_exc()
        return jsonify({"error": "Internal server error"}), 500

@webhook.route("/notifications", methods=["GET"])
def get_notifications():
    try:
        mongo = current_app.extensions.get('pymongo')
        if not mongo:
            return jsonify({"error": "MongoDB not initialized"}), 500

        db = mongo.db
        last_fetch = get_last_fetch_timestamp(db)
        
        # Build query for new events
        query = {}
        if last_fetch:
            query["timestamp"] = {"$gt": last_fetch}

        # Get new events sorted by timestamp (newest first)
        events = db[EVENTS_COLLECTION].find(query).sort("timestamp", DESCENDING)
        
        # Convert to list while it's still connected to DB
        events_list = list(events)
        
        # Update last fetch timestamp if we got new events
        if events_list:
            newest_timestamp = events_list[0]["timestamp"]
            update_last_fetch_timestamp(db, newest_timestamp)

        # Prepare response
        result = []
        for event in events_list:
            result.append({
                "action": event.get("action"),
                "author": event.get("author"),
                "from_branch": event.get("from_branch"),
                "to_branch": event.get("to_branch"),
                "timestamp": event["timestamp"].isoformat()  # Ensure ISO format
            })

        return jsonify(result)

    except Exception as e:
        current_app.logger.error(f"[Notification Fetch Error] {str(e)}")
        traceback.print_exc()
        return jsonify({"error": "Failed to fetch notifications"}), 500