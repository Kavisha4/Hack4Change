from flask import Flask, render_template, request, session, redirect, url_for

app = Flask(__name__)

questions = [
    {
        'question': 'What is the capital of France?',
        'options': ['Paris', 'London', 'Berlin', 'Madrid'],
        'answer': 'Paris'
    },
    {
        'question': 'Which planet is known as the Red Planet?',
        'options': ['Earth', 'Mars', 'Jupiter', 'Saturn'],
        'answer': 'Mars'
    },
    {
        'question': 'Who wrote "To Kill a Mockingbird"?',
        'options': ['Harper Lee', 'Mark Twain', 'Ernest Hemingway', 'F. Scott Fitzgerald'],
        'answer': 'Harper Lee'
    }
]

recommendations = {
    'Python': {
        'Beginner': ['Introduction to Python', 'Python for Beginners'],
        'Intermediate': ['Intermediate Python', 'Python Data Structures'],
        'Advanced': ['Advanced Python Programming', 'Python Machine Learning']
    },
    'JavaScript': {
        'Beginner': ['JavaScript Basics', 'JavaScript for Beginners'],
        'Intermediate': ['Intermediate JavaScript', 'JavaScript and DOM'],
        'Advanced': ['Advanced JavaScript', 'JavaScript Frameworks']
    },
    'Data Structures': {
        'Beginner': ['Introduction to Data Structures', 'Basic Data Structures'],
        'Intermediate': ['Intermediate Data Structures', 'Data Structures in Practice'],
        'Advanced': ['Advanced Data Structures', 'Data Structures and Algorithms']
    }
}

@app.route('/')
def home():
    return render_template('index.html', subjects=recommendations.keys())

@app.route('/start_quiz')
def start_quiz():
    session['question_index'] = 0
    session['score'] = 0
    return redirect(url_for('quiz'))

@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    question_index = session.get('question_index', 0)
    score = session.get('score', 0)

    if request.method == 'POST':
        selected_option = request.form.get('option')
        if selected_option == questions[question_index]['answer']:
            session['score'] = score + 1
        session['question_index'] = question_index + 1
        if question_index + 1 >= len(questions):
            return redirect(url_for('result'))
        else:
            return redirect(url_for('quiz'))

    if question_index >= len(questions):
        return redirect(url_for('result'))

    question = questions[question_index]
    return render_template('quiz.html', question=question, question_index=question_index)

@app.route('/result')
def result():
    score = session.get('score', 0)
    return render_template('result.html', score=score, total=len(questions))

@app.route('/analysis', methods=['GET', 'POST'])
def analysis():
    if request.method == 'POST':
        subject = request.form.get('subject')
        skill_level = request.form.get('skill_level')
        recommended_content = recommendations.get(subject, {}).get(skill_level, [])
        return render_template('analysis.html', subjects=recommendations.keys(), recommended_content=recommended_content, selected_subject=subject, selected_skill_level=skill_level)
    return render_template('analysis.html', subjects=recommendations.keys())

if __name__ == '__main__':
    app.run(debug=True)
