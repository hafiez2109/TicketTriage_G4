import azure.functions as func
import json
import logging

from shared.data_store import get_tickets, add_ticket, update_ticket_status
from shared.classifier import classify_ticket

app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)


@app.route(route="SubmitTicket", methods=["POST"])
def SubmitTicket(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("SubmitTicket triggered")
    try:
        body = req.get_json()
    except ValueError:
        return func.HttpResponse(
            json.dumps({"error": "Invalid JSON body"}),
            status_code=400,
            mimetype="application/json",
        )

    name = body.get("name")
    email = body.get("email")
    title = body.get("title")
    description = body.get("description", "")
    priority = body.get("priority", "Medium")
    category = body.get("category", "Auto-classify")

    if not name or not email or not title:
        return func.HttpResponse(
            json.dumps({"error": "name, email, and title are required"}),
            status_code=400,
            mimetype="application/json",
        )

    if category == "Auto-classify":
        category = classify_ticket(title, description)

    ticket = add_ticket(name, email, title, description, priority, category)

    return func.HttpResponse(
        json.dumps(ticket),
        status_code=201,
        mimetype="application/json",
    )


@app.route(route="GetTickets", methods=["GET"])
def GetTickets(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("GetTickets triggered")
    tickets = get_tickets()

    status_filter = req.params.get("status")
    category_filter = req.params.get("category")
    email_filter = req.params.get("email")

    if status_filter:
        tickets = [t for t in tickets if t["status"].lower() == status_filter.lower()]
    if category_filter:
        tickets = [t for t in tickets if t["category"].lower() == category_filter.lower()]
    if email_filter:
        tickets = [t for t in tickets if t["email"].lower() == email_filter.lower()]

    return func.HttpResponse(
        json.dumps(tickets),
        status_code=200,
        mimetype="application/json",
    )


@app.route(route="UpdateTicket/{ticket_id}", methods=["PUT"])
def UpdateTicket(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("UpdateTicket triggered")
    ticket_id = req.route_params.get("ticket_id")

    try:
        body = req.get_json()
    except ValueError:
        return func.HttpResponse(
            json.dumps({"error": "Invalid JSON body"}),
            status_code=400,
            mimetype="application/json",
        )

    new_status = body.get("status")
    if not new_status:
        return func.HttpResponse(
            json.dumps({"error": "status is required"}),
            status_code=400,
            mimetype="application/json",
        )

    updated = update_ticket_status(ticket_id, new_status)
    if not updated:
        return func.HttpResponse(
            json.dumps({"error": "Ticket not found"}),
            status_code=404,
            mimetype="application/json",
        )

    return func.HttpResponse(
        json.dumps(updated),
        status_code=200,
        mimetype="application/json",
    )