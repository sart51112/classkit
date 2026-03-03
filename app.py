from flask import Flask, render_template, request, jsonify
import json
import os

app = Flask(__name__)

CARDS_FILE = 'flashcards.json'
HOMEWORK_FILE = 'homework.json'

def load_cards():
    if os.path.exists(CARDS_FILE):
        with open(CARDS_FILE, 'r') as f:
            return json.load(f)
    return []

def save_cards(cards):
    with open(CARDS_FILE, 'w') as f:
        json.dump(cards, f)

def load_homework():
    if os.path.exists(HOMEWORK_FILE):
        with open(HOMEWORK_FILE, 'r') as f:
            return json.load(f)
    return []

def save_homework(tasks):
    with open(HOMEWORK_FILE, 'w') as f:
        json.dump(tasks, f)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/timetable')
def timetable():
    return render_template('timetable.html')

@app.route('/flashcards')
def flashcards():
    cards = load_cards()
    return render_template('flashcards.html', cards=cards)

@app.route('/flashcards/add', methods=['POST'])
def add_card():
    data = request.get_json()
    cards = load_cards()
    cards.append({'question': data['question'], 'answer': data['answer']})
    save_cards(cards)
    return jsonify({'success': True, 'cards': cards})

@app.route('/flashcards/delete/<int:index>', methods=['POST'])
def delete_card(index):
    cards = load_cards()
    if 0 <= index < len(cards):
        cards.pop(index)
        save_cards(cards)
    return jsonify({'success': True, 'cards': cards})

@app.route('/timer')
def timer():
    return render_template('timer.html')

@app.route('/homework')
def homework():
    tasks = load_homework()
    return render_template('homework.html', tasks=tasks)

@app.route('/homework/add', methods=['POST'])
def add_homework():
    data = request.get_json()
    tasks = load_homework()
    tasks.append({'subject': data['subject'], 'task': data['task'], 'due': data['due'], 'done': False})
    save_homework(tasks)
    return jsonify({'success': True, 'tasks': tasks})

@app.route('/homework/toggle/<int:index>', methods=['POST'])
def toggle_homework(index):
    tasks = load_homework()
    if 0 <= index < len(tasks):
        tasks[index]['done'] = not tasks[index]['done']
        save_homework(tasks)
    return jsonify({'success': True, 'tasks': tasks})

@app.route('/homework/delete/<int:index>', methods=['POST'])
def delete_homework(index):
    tasks = load_homework()
    if 0 <= index < len(tasks):
        tasks.pop(index)
        save_homework(tasks)
    return jsonify({'success': True, 'tasks': tasks})

if __name__ == '__main__':
    app.run(debug=True)