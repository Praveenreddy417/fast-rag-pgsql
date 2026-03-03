from app.models.ticket import Ticket

def create_ticket(db, question, answer):
    ticket = Ticket(question=question, answer=answer)
    db.add(ticket)
    db.commit()
