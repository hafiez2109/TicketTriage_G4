import json
import os
import uuid
from datetime import datetime, timezone
from azure.cosmos import CosmosClient, exceptions

endpoint = os.getenv("COSMOS_ENDPOINT")
key = os.getenv("COSMOS_KEY")
database_name = os.getenv("COSMOS_DATABASE")
container_name = os.getenv("COSMOS_CONTAINER")

# Creating Cosmos Client
client = CosmosClient(endpoint, key)

# Getting the Cosmos Database and the Container inside the Database
database = client.get_database_client(database_name)
container = database.get_container_client(container_name)

def to_ticket_response(item):
    return {
        "id": item["id"],
        "name": item["name"],
        "email": item["email"],
        "title": item["title"],
        "description": item["description"],
        "priority": item["priority"],
        "category": item["category"],
        "status": item["status"],
        "created_date": item["created_date"],
    }

def get_tickets():
    try:
        items = list(container.read_all_items())
        return [to_ticket_response(item) for item in items]
    except exceptions.CosmosHttpResponseError as e:
        print(f"Error reading tickets from Cosmos DB: {e}")
        return []

def add_ticket(name, email, title, description, priority, category):
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
    ticket_created = container.create_item(body=ticket)
    return to_ticket_response(ticket_created)

def update_ticket_status(ticket_id, new_status):
    try:
        updated = container.patch_item(
            item=ticket_id,
            partition_key=ticket_id,
            patch_operations=[
                {
                    "op": "set",
                    "path": "/status",
                    "value": new_status
                }
            ]
        )
        return to_ticket_response(updated)
    except exceptions.CosmosResourceNotFoundError:
        return None
