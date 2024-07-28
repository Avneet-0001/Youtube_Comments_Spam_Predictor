# app/main.py

from fastapi import FastAPI
from pydantic import BaseModel
import pickle
import joblib
import pandas as pd
import re
from fastapi.middleware.cors import CORSMiddleware

# Initialize FastAPI app
app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Load the trained model and vectorizer
model = joblib.load("model.pkl")
vectorizer = joblib.load("vectorizer.pkl")

# with open("model.pkl", "rb") as f:
#     model = pickle.load(f)

# with open("vectorizer.pkl", "rb") as f:
#     vectorizer = pickle.load(f)

class Comment(BaseModel):
    content: str

def process_content(content):
    return " ".join(re.findall("[A-Za-z]+", content.lower()))

@app.get("/")
def read_root():
    return {"message": "Welcome to the YouTube Comments Spam Detector API!"}

@app.post("/predict")
def predict(comment: Comment):
    processed_content = process_content(comment.content)
    transformed_content = vectorizer.transform([processed_content])
    prediction = model.predict(transformed_content)
    result = "Spam" if prediction == 1 else "Ham"
    return {"content": comment.content, "prediction": result}
