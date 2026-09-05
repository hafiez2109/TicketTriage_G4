import json
import os
import uuid
from datetime import datetime, timezone

DATA_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "tickets.json")


def read_tickets():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8-sig") as f:
        return json.load(f)

def write_tickets(tickets):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(tickets, f, indent=2)


def add_ticket(name, email, title, description, priority, category):
    tickets = read_tickets()
    ticket = {
        "id": str(uuid.uuid4()),
        "name": name,
        "email": email,
        "title": title,
        "description": description,
        "priority": priority or "Medium",
        "category": category,
        "status": "New",
        "created_date": datetime.now(timezone.utc).isoformat(),
    }
    tickets.append(ticket)
    write_tickets(tickets)
    return ticket


def update_ticket_status(ticket_id, new_status):
    tickets = read_tickets()
    for t in tickets:
        if t["id"] == ticket_id:
            t["status"] = new_status
            write_tickets(tickets)
            return t
    return None