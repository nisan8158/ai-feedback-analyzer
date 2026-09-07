import sqlite3

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from transformers import pipeline


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


sentiment_analyzer = pipeline(
    "sentiment-analysis",
    model="distilbert/distilbert-base-uncased-finetuned-sst-2-english"
)


def create_database():
    connection = sqlite3.connect("feedback.db")
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL,
            sentiment TEXT NOT NULL,
            confidence REAL NOT NULL,
            category TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()


create_database()


def save_feedback(text, sentiment, confidence, category):
    connection = sqlite3.connect("feedback.db")
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO feedback (text, sentiment, confidence, category)
        VALUES (?, ?, ?, ?)
        """,
        (text, sentiment, confidence, category)
    )

    connection.commit()
    connection.close()


def detect_category(text: str):
    text = text.lower()

    if any(word in text for word in ["payment", "card", "charged", "billing", "refund"]):
        return "payment"

    if any(word in text for word in ["crash", "bug", "error", "slow", "login", "technical"]):
        return "technical_issue"

    if any(word in text for word in ["delivery", "order", "shipping", "arrived"]):
        return "delivery"

    if any(word in text for word in ["support", "customer service", "agent", "helpful"]):
        return "customer_service"

    if any(word in text for word in ["design", "interface", "ui", "feature"]):
        return "product"

    return "other"


class Feedback(BaseModel):
    text: str


@app.get("/")
def home():
    return {"message": "AI Feedback Analyzer is running!"}


@app.post("/feedback")
def receive_feedback(feedback: Feedback):
    result = sentiment_analyzer(feedback.text)[0]
    category = detect_category(feedback.text)

    sentiment = result["label"].lower()
    confidence = round(result["score"], 4)

    save_feedback(
        feedback.text,
        sentiment,
        confidence,
        category
    )

    return {
        "text": feedback.text,
        "sentiment": sentiment,
        "confidence": confidence,
        "category": category
    }
@app.get("/feedback")
def get_feedback():
    connection = sqlite3.connect("feedback.db")
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, text, sentiment, confidence, category
        FROM feedback
        ORDER BY id DESC
    """)

    rows = cursor.fetchall()
    connection.close()

    return [
        {
            "id": row[0],
            "text": row[1],
            "sentiment": row[2],
            "confidence": row[3],
            "category": row[4]
        }
        for row in rows
    ]
@app.get("/stats")
def get_stats():
    connection = sqlite3.connect("feedback.db")
    cursor = connection.cursor()

    cursor.execute("SELECT COUNT(*) FROM feedback")
    total = cursor.fetchone()[0]

    cursor.execute("""
        SELECT sentiment, COUNT(*)
        FROM feedback
        GROUP BY sentiment
    """)
    sentiment_rows = cursor.fetchall()

    cursor.execute("""
        SELECT category, COUNT(*)
        FROM feedback
        GROUP BY category
    """)
    category_rows = cursor.fetchall()

    connection.close()

    sentiments = {}
    for sentiment, count in sentiment_rows:
        sentiments[sentiment] = count

    categories = {}
    for category, count in category_rows:
        categories[category] = count

    return {
        "total_feedback": total,
        "sentiments": sentiments,
        "categories": categories
    }