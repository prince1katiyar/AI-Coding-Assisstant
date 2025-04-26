#!/bin/bash
echo "Starting AI-Based Coding Assistant for Students..."

# Start Backend
echo "Starting FastAPI Backend..."
cd backend
uvicorn main:app --reload 

# Start Frontend
echo "Starting Streamlit Frontend..."
cd ../frontend
streamlit run app.py
