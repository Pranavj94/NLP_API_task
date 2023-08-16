from fastapi import FastAPI, HTTPException
import requests
import spacy
from collections import Counter
import nltk
from tqdm import tqdm
import uvicorn

app = FastAPI()

# Load spacy NER model
print(f'Loading spacy model')
nlp = spacy.load("en_core_web_sm")

def fetch_text(url):
    response = requests.get(url)
    return response.text

def extract_entities(text, entity_type):
    """
    Extracts entities of the specified type from the given text.
    
    Args:
        text (str): The input text to analyze.
        entity_type (str): The type of entity to extract (e.g., "PERSON", "GPE").
        
    Returns:
        list: A list of extracted entities of the specified type.
    """
    doc = nlp(text)
    entities = []
    for ent in doc.ents:
        if ent.label_ == entity_type:
            entities.append(ent.text)
    return entities

def find_text_span(position,max_len,check_range):
    """
    Returns the span of text to be checked based on current position.
    
    Args:
        position (int): position of the name
        max_len (int): Maximum length of text
        check_range (int): Range to be checked
        
    Returns:
        tuple : Start and end indexes
    """
    
    # Check if position is in the first n words
    if position - check_range < 0:
        start = 0
    else:
        start = position - check_range
        
    # Check if position is in the last n words
    if position + check_range > max_len:
        end = max_len
    else:
        end = position + check_range
    
    return(start,end)

@app.post('/analyze/')
def analyze_text(data: dict):
    if "URL" not in data:
        raise HTTPException(status_code=400, detail="URL key is missing")

    url = data["URL"]
    try:
        text = fetch_text(url)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch text from URL: {str(e)}")

    # Extract PERSON entities and count their occurrences
    people = extract_entities(text, "PERSON")
    people_counts = Counter(people)

    # Create a list of people with their counts and associated places
    sorted_people = [{"name": person, "count": count, "associated_places": []} for person, count in people_counts.most_common()]

    # Preprocess the text and split it into a list of words
    text = text.replace('\n', ' ')
    text_list = text.split(' ')

    # Specify the range of span
    check_range = 100

    # Analyze the context around each person

    # Iterate through each name
    for person in tqdm(sorted_people):

        # Check positions of occurance of name in text
        positions = [index for index, value in enumerate(text_list) if value == person['name']]
        check_horizon = list()

        # Iterate through each position
        for position in positions:

            # Find span of the position
            start,end = find_text_span(position,len(text_list),check_range)

            # Append the span 
            check_horizon.extend(text_list[start:end])

        # Extract GPE (geopolitical entity) entities from the context
        places = extract_entities((" ").join(check_horizon), "GPE")

        # Count the occurrences of associated places and sort them
        item_counts = Counter(places)
        sorted_counts_places = dict(sorted(item_counts.items(), key=lambda item: item[1], reverse=True))

        # Assign the sorted associated places to the person
        person['associated_places'] = sorted_counts_places

    result = {
        **data,
        "people": sorted_people
    }

    return result

if __name__ == '__main__':

    uvicorn.run(app, host="0.0.0.0", port=8000)
