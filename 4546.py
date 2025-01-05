from flask import Flask, render_template, request, redirect, url_for, session
import random
import time
random.seed(time.time())

app = Flask(__name__)
app.secret_key = 'your_secret_key'

questions_123 = []
questions_456 = []
with open('123.txt', 'r', encoding='utf-8') as file:
    questions_123 = file.read().split('\n\n')[1:]

with open('456.txt', 'r', encoding='utf-8') as file:
    questions_456 = file.read().split('\n\n')[1:]

single_questions = []
multiple_questions = []
judgement_questions = []
single_answers=[]
multiple_answers=[]
judgement_answers = []

for question in questions_123:
    if question.startswith('【单选】'):
        single_questions.append(question)
    elif question.startswith('【多选】'):
        multiple_questions.append(question)
    elif question.startswith('【判断】'):
        judgement_questions.append(question)
for answer in questions_456:
    if answer.startswith('【单选】'):
        single_answers.append(answer)
    elif answer.startswith('【多选】'):
        multiple_answers.append(answer)
    elif answer.startswith('【判断】'):
        judgement_answers.append(answer)

modes = ['single', 'multiple', 'judgement']

@app.before_request
def before_request():
    if 'mode' not in session:
        session['mode']='single'
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        question_index = int(request.form.get('question_index'))
        selected_answers = request.form.getlist('answer')
        user_answers = ', '.join(selected_answers)
        question_list = single_questions if session['mode'] == 'single' else multiple_questions if session['mode'] == 'multiple' else judgement_questions
        answer_list = single_answers if session['mode'] == 'single' else multiple_answers if session['mode'] == 'multiple' else judgement_answers
        correct_question = answer_list[question_index]
        question = question_list[question_index]
        return render_template('index.html', question=question, correct_question=correct_question, question_index=question_index, user_answers=user_answers, mode=session['mode'])

    question_list = single_questions if session['mode'] == 'single' else multiple_questions if session['mode'] == 'multiple' else judgement_questions
    question_index = random.randint(0, len(question_list) - 1)
    question = question_list[question_index]
    return render_template('index.html', question=question, question_index=question_index, mode=session['mode'])

@app.route('/mode/<mode>')
def switch_mode(mode):
    if mode in modes:
        session['mode'] = mode
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)