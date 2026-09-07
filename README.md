# AI Feedback Analyzer

An AI-powered customer feedback analysis application that automatically analyzes customer feedback using Natural Language Processing (NLP).

The application detects sentiment, categorizes feedback, stores the results, and provides an interactive dashboard for analyzing customer feedback.

## Features

- AI-powered sentiment analysis
- Automatic feedback categorization
- Confidence score for AI predictions
- Feedback storage using SQLite
- REST API built with FastAPI
- Customer feedback submission interface
- Analytics dashboard
- Sentiment distribution visualization
- Category distribution visualization
- Recent feedback overview

## Technologies

- Python
- FastAPI
- Hugging Face Transformers
- PyTorch
- SQLite
- HTML
- CSS
- JavaScript
- Chart.js

## AI Model

The project uses the following pretrained Hugging Face model for sentiment analysis:

`distilbert-base-uncased-finetuned-sst-2-english`

The model classifies customer feedback as **positive** or **negative** and returns a confidence score.

## How It Works

Customer Feedback  
↓  
FastAPI Backend  
↓  
AI Sentiment Analysis  
↓  
Automatic Category Detection  
↓  
SQLite Database  
↓  
Analytics Dashboard

## Feedback Categories

Feedback is automatically classified into categories such as:

- Payment
- Delivery
- Technical Issue
- Customer Service
- Product
- Other

## Project Structure

```text
ai-feedback-analyzer/
├── main.py
├── index.html
├── dashboard.html
├── requirements.txt
├── README.md
└── .gitignore
```

## Installation

1. Clone the repository:

```bash
git clone <repository-url>
cd ai-feedback-analyzer
```

2. Create a virtual environment:

```bash
python3.12 -m venv .venv
source .venv/bin/activate
```

3. Install the required dependencies:

```bash
pip install -r requirements.txt
```

4. Start the FastAPI server:

```bash
uvicorn main:app --reload
```

5. Open the customer feedback interface:

```text
index.html
```

6. Open the analytics dashboard:

```text
dashboard.html
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Check whether the API is running |
| POST | `/feedback` | Submit and analyze customer feedback |
| GET | `/feedback` | Retrieve stored feedback |
| GET | `/stats` | Retrieve feedback statistics |

## Dashboard

The analytics dashboard provides:

- Total feedback count
- Positive and negative feedback counts
- Sentiment distribution chart
- Category distribution chart
- Recent feedback with sentiment, category, and confidence score

## Future Improvements

- Support for neutral sentiment
- More advanced AI-based category classification
- Multilingual feedback analysis
- Search and filtering
- User authentication for the analytics dashboard
- Cloud deployment

## Author

Developed as a personal AI and software engineering project.