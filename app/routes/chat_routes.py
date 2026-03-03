from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from app.models.ticket import Ticket
from app.models.message import Message
from app.services.rag_service import generate_answer
from app.services.rules_engine import classify_tier, classify_severity, escalation_needed
import uuid

router = APIRouter()


@router.post("/chat")
def chat(request: dict, db: Session = Depends(get_db)):

    session_id = request["sessionId"]
    message = request["message"]
    user_role = request["userRole"]
    context = request.get("context", {})

    # Create ticket if not exists
    ticket = db.query(Ticket).filter_by(session_id=session_id).first()
    if not ticket:
        ticket = Ticket(
            session_id=session_id,
            user_role=user_role,
            context=context
        )
        db.add(ticket)
        db.commit()

    # Save user message
    user_msg = Message(
        id=str(uuid.uuid4()),
        session_id=session_id,
        role="user",
        content=message
    )
    db.add(user_msg)
    db.commit()

    # Generate answer using KB + session
    rag_response = generate_answer(message, session_id, db)

    # Deterministic classification
    tier = classify_tier(user_role, context.get("module"))
    severity = classify_severity(message)
    needs_escalation = escalation_needed(severity)

    response = {
        "answer": rag_response["answer"],
        "kbReferences": rag_response["kbReferences"],
        "confidence": rag_response["confidence"],
        "tier": tier,
        "severity": severity,
        "needsEscalation": needs_escalation,
        "guardrail": {
            "blocked": False,
            "reason": None
        }
    }

    # Save assistant message
    assistant_msg = Message(
        id=str(uuid.uuid4()),
        session_id=session_id,
        role="assistant",
        content=response["answer"]
    )
    db.add(assistant_msg)
    db.commit()

    return response