# NLP_API_task

This is a simple Text Analysis API built using FastAPI. The API analyzes text from a given URL, extracts named entities of specified types, and provides information about people mentioned in the text and their associated places.

Getting Started
To run the Text Analysis API locally, follow the steps below:

Prerequisites
Python 3.x
SpaCy NER model (en_core_web_sm)
FastAPI
tqdm
uvicorn

Installation
Clone the repository:

bash
git clone https://github.com/your-username/text-analysis-api.git
cd text-analysis-api

Install the required dependencies:

bash
pip install -r requirements.txt


Usage
Run the FastAPI server:
uvicorn api:app --host 0.0.0.0 --port 8000

bash
Copy code
uvicorn main:app --reload
Open your browser or use an API testing tool (e.g., curl, Postman).

Make a POST request to http://localhost:8000/analyze/ with a JSON payload containing the URL of the text you want to analyze. For example:

$Headers = @{
    "Content-Type" = "application/json"
}

$Body = @{
    "URL" =  "https://www.gutenberg.org/cache/epub/2447/pg2447.txt"
    "value" = "10"
} | ConvertTo-Json

Invoke-WebRequest `
    -Uri http://localhost:8000/analyze/ `
    -Method POST `
    -Headers $Headers `
    -Body $Body

The API will return a JSON response with information about people mentioned in the text and their associated places.
