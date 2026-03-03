import os
from openai import OpenAI
from config import OPENAI_API_KEY
from app.models.message import Message

client = OpenAI(api_key=OPENAI_API_KEY)

# Path to KB folder
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
KB_FOLDER = os.path.join(BASE_DIR, "kb")


def load_kb():
    """Load all KB files into memory"""
    docs = []
    if not os.path.exists(KB_FOLDER):
        raise FileNotFoundError(f"KB folder not found at {KB_FOLDER}")
    for file in os.listdir(KB_FOLDER):
        if file.endswith(".md"):
            with open(os.path.join(KB_FOLDER, file), "r", encoding="utf-8") as f:
                docs.append({"id": f"kb-{file}", "title": file, "content": f.read()})
    return docs


def generate_answer(question: str, session_id: str, db):
    """
    Generate answer from KB files and previous session context
    """

    # 1️⃣ Load KB documents
    docs = load_kb()

    # 2️⃣ Load previous messages for session
    history_msgs = db.query(Message).filter_by(session_id=session_id).order_by(Message.created_at).all()
    history = [{"role": msg.role, "content": msg.content} for msg in history_msgs]

    # 3️⃣ Find relevant KB chunks
    context = ""
    kb_refs = []
    for idx, doc in enumerate(docs):
        if question.lower() in doc["content"].lower():
            context += doc["content"][:1000] + "\n"
            kb_refs.append({"id": doc["id"], "title": doc["title"]})

    if not context:
        return {
            "answer": "The information is not available in the provided documents.",
            "kbReferences": [],
            "confidence": 0.4
        }

    # 4️⃣ Prepare messages for OpenAI
    messages = [{"role": "system", "content": "Answer strictly using KB content."}]
    messages.extend(history)
    messages.append({"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}"})

    # 5️⃣ Call OpenAI API
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0,
        messages=messages
    )

    answer_text = response.choices[0].message.content

    return {
        "answer": answer_text,
        "kbReferences": kb_refs,
        "confidence": 0.9
    }