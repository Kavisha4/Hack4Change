from pymongo import MongoClient
from datetime import datetime, timezone

client = MongoClient('mongodb+srv://admin:admin@cluster0.tp23edu.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
db = client['anki_clone']
cards_collection = db['cards']

cards_collection.delete_many({})
cards = [
    {
        "question": "What is the capital of France?",
        "options": ["Paris", "London", "Berlin", "Madrid"],
        "correct_option": "Paris",
        "next_review": datetime.now(timezone.utc),  # Ensure this is due or past
        "interval": 1,
        "ease_factor": 2.5,
        "repetitions": 0
    },
    {
        "question": "What is the largest planet in our Solar System?",
        "options": ["Earth", "Mars", "Jupiter", "Saturn"],
        "correct_option": "Jupiter",
        "next_review": datetime.now(timezone.utc),  # Ensure this is due or past
        "interval": 1,
        "ease_factor": 2.5,
        "repetitions": 0
    },
    {
        "question": "What is 2+2?",
        "options": ["1", "2", "3", "4"],
        "correct_option": "4",
        "next_review": datetime.now(timezone.utc),  # Ensure this is due or past
        "interval": 1,
        "ease_factor": 2.5,
        "repetitions": 0
    },
    {
        "question": "What is the smallest prime number ?",
        "options": ["1", "2", "3", "4"],
        "correct_option": "1",
        "next_review": datetime.now(timezone.utc),  # Ensure this is due or past
        "interval": 1,
        "ease_factor": 2.5,
        "repetitions": 0
    }
]

cards_collection.insert_many(cards)
print("Data inserted successfully!")


from pymongo import MongoClient

# client = MongoClient('localhost', 27017)
# db = client['anki_clone']
# history_collection = db['history']

# history_collection.insert_one({
#     'card_id': 'sample_card_id',
#     'selected_option': 'Paris',
#     'correct_option': 'Paris',
#     'is_correct': True,
#     'timestamp': datetime.now(timezone.utc)
# })
# print("Sample history inserted successfully!")
