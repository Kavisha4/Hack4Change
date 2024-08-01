from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient
from datetime import datetime, timedelta, timezone
from bson import ObjectId
from googletrans import Translator

app = Flask(__name__)

client = MongoClient('mongodb+srv://admin:admin@cluster0.tp23edu.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
db = client['anki_clone']
cards_collection = db['cards']
history_collection = db['history']
translator = Translator()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/start_quiz', methods=['POST'])
def start_quiz():
    language = request.json.get('language', 'en')
    card = get_due_card()
    if card:
        question = translate_text(card['question'], language)
        options = [translate_text(option, language) for option in card['options']]
        return jsonify({
            'success': True,
            'question': question,
            'options': options,
            'card_id': str(card['_id']),
            'language': language
        })
    else:
        return jsonify({'success': False, 'message': 'No cards to review!'})

@app.route('/answer', methods=['POST'])
def answer():
    data = request.json
    card_id = data['card_id']
    selected_option = data['selected_option']
    language = data['language']
    card = cards_collection.find_one({'_id': ObjectId(card_id)})

    if card:
        is_correct = selected_option == translate_text(card['correct_option'], language)
        update_card(card, is_correct)
        history_collection.insert_one({
            'card_id': card_id,
            'selected_option': selected_option,
            'correct_option': translate_text(card['correct_option'], language),
            'is_correct': is_correct,
            'timestamp': datetime.now(timezone.utc)
        })

        next_card = get_due_card()
        if next_card:
            question = translate_text(next_card['question'], language)
            options = [translate_text(option, language) for option in next_card['options']]
            return jsonify({
                'success': True,
                'question': question,
                'options': options,
                'card_id': str(next_card['_id']),
                'language': language
            })
        else:
            return jsonify({'success': True, 'message': 'No more cards to review!'})
    return jsonify({'success': False, 'error': 'Card not found'})

@app.route('/history')
def answer_history():
    today = datetime.now(timezone.utc).date()
    start_of_day = datetime.combine(today, datetime.min.time(), timezone.utc)
    end_of_day = start_of_day + timedelta(days=1)

    history_dates = list(history_collection.aggregate([
        {
            '$project': {
                'date': {
                    '$dateToString': {
                        'format': '%d-%m-%Y',
                        'date': '$timestamp'
                    }
                }
            }
        },
        {
            '$group': {
                '_id': '$date',
                'count': {'$sum': 1}
            }
        },
        {
            '$sort': {'_id': 1}
        }
    ]))

    answered_today_count = history_collection.count_documents({
        'timestamp': {'$gte': start_of_day, '$lt': end_of_day}
    })
    correct_answers = history_collection.count_documents({
        'timestamp': {'$gte': start_of_day, '$lt': end_of_day},
        'is_correct': True
    })
    wrong_answers = history_collection.count_documents({
        'timestamp': {'$gte': start_of_day, '$lt': end_of_day},
        'is_correct': False
    })

    return render_template('history.html', history_dates=history_dates, total_answered_today=answered_today_count, correct_answers=correct_answers, wrong_answers=wrong_answers)

@app.route('/scheduled')
def scheduled_cards():
    now = datetime.now(timezone.utc)
    
    future_cards = list(cards_collection.aggregate([
        {
            '$match': {
                'next_review': {'$gt': now}
            }
        },
        {
            '$project': {
                'date': {
                    '$dateToString': {
                        'format': '%d-%m-%Y',
                        'date': '$next_review'
                    }
                }
            }
        },
        {
            '$group': {
                '_id': '$date',
                'count': {'$sum': 1}
            }
        },
        {
            '$sort': {'_id': 1}
        }
    ]))
    
    return render_template('scheduled.html', future_cards=future_cards)

def get_due_card():
    now = datetime.now(timezone.utc)
    card = cards_collection.find_one({'next_review': {'$lte': now}})
    return card

def update_card(card, is_correct):
    if is_correct:
        card['repetitions'] += 1
        card['interval'] = card['interval'] * card['ease_factor']
        card['next_review'] = datetime.now(timezone.utc) + timedelta(days=card['interval'])
    else:
        card['repetitions'] = 0
        card['interval'] = 1
        card['ease_factor'] = max(1.3, card['ease_factor'] - 0.2)
        card['next_review'] = datetime.now(timezone.utc) + timedelta(days=card['interval'])
    
    cards_collection.update_one({'_id': card['_id']}, {'$set': card})

def translate_text(text, target_language):
    if target_language == 'en':
        return text  # No translation needed
    return translator.translate(text, dest=target_language).text

if __name__ == '__main__':
    app.run(debug=True)
