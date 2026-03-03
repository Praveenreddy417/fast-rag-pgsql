from sqlalchemy.orm import Session
from app.models.ticket import Ticket
from app.models.message import Message
from sqlalchemy import func

def get_metrics(db: Session):
    # Total tickets
    total_tickets = db.query(func.count(Ticket.session_id)).scalar()

    # Total messages
    total_messages = db.query(func.count(Message.id)).scalar()

    # Messages per ticket
    messages_per_ticket = (
        db.query(Message.session_id, func.count(Message.id))
        .group_by(Message.session_id)
        .all()
    )
    messages_per_ticket_dict = {session_id: count for session_id, count in messages_per_ticket}

    # Example: last 5 tickets
    recent_tickets = (
        db.query(Ticket)
        .order_by(Ticket.created_at.desc())
        .limit(5)
        .all()
    )
    recent_tickets_data = [
        {"sessionId": t.session_id, "userRole": t.user_role, "createdAt": t.created_at.isoformat()}
        for t in recent_tickets
    ]

    return {
        "totalTickets": total_tickets,
        "totalMessages": total_messages,
        "messagesPerTicket": messages_per_ticket_dict,
        "recentTickets": recent_tickets_data
    }