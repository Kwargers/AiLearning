from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3


# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)

#instantiate database
database = 'stw3.db'

GlobalID = []
# enable CORS
CORS(app, resources={r'/*': {'origins': '*'}})

GlobalPoints = []

@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    response_object = {}
    if request.method == 'POST':
        print('this is a post method')
    else:
        conn = sqlite3.connect(database)
        cursor = conn.cursor()
        sql_quizzes = cursor.execute('SELECT QuizName FROM Quiz;')
        quizzes = []
        for quiz in sql_quizzes:
            quizzes.append(quiz)
        conn.commit()
        conn.close()
        print(quizzes)
        response_object['quizzes'] = quizzes
        print(response_object)
    return jsonify(response_object)

@app.route('/receiveAnswers', methods=['GET', 'POST'])
def receiveAnswers():
    response_questions = {}
    if request.method == 'POST':
        quizID = request.get_json()
        ID = quizID.get('quizID') + 1
        GlobalID.insert(0, ID)
    else:
        conn = sqlite3.connect(database)
        cursor = conn.cursor()
        #sql_questions = cursor.execute('SELECT Question FROM QuizQuestion WHERE QuizID = {ID};'.format(ID=GlobalID[0]))
        sql_answers = cursor.execute('SELECT Choice1, Choice2, Choice3, Choice4 FROM QuizQuestion WHERE QuizID = {ID};'.format(ID=GlobalID[0]))
        #questions = []
        answers = []
        #for question in sql_questions:
            #questions.append(question)
            #print(question)
        for answer in sql_answers:
            answers.append(answer)
            print(answer)
        conn.commit()
        conn.close()
        #print(questions)
        print(GlobalID)
        #response_questions['questions'] = questions
        response_questions['answers'] = answers
        print(response_questions)
    return jsonify(response_questions)

@app.route('/receiveQuestions', methods=['GET', 'POST'])
def IDreceive():
    response_questions = {}
    if request.method == 'POST':
        quizID = request.get_json()
        ID = quizID.get('quizID') + 1
        GlobalID.insert(0, ID)
    else:
        conn = sqlite3.connect(database)
        cursor = conn.cursor()
        sql_questions = cursor.execute('SELECT Question FROM QuizQuestion WHERE QuizID = {ID};'.format(ID=GlobalID[0]))
        #sql_answers = cursor.execute('SELECT Choice1, Choice2, Choice3, Choice4 FROM QuizQuestion WHERE QuizID = {ID};'.format(ID=GlobalID[0]))
        questions = []
        for question in sql_questions:
            questions.append(question)
            print(question)
        conn.commit()
        conn.close()
        print(questions)
        print(GlobalID)
        response_questions['questions'] = questions
        #response_questions['answers'] = answers
        print(response_questions)
    return jsonify(response_questions)

@app.route('/receiveAnswersSubmitted', methods=['GET', 'POST'])
def receiveAnswersSubmitted():
    response_object = {}
    if request.method == 'POST':
        answersJson = request.get_json()
        userAnswers = answersJson.get('answers')
        conn = sqlite3.connect(database)
        cursor = conn.cursor()
        sql_answers = cursor.execute('SELECT Answer FROM QuizQuestion WHERE QuizID = {ID};'.format(ID=GlobalID[0]))
        answers = []
        for answer in sql_answers:
            answers.append(answer)
            print(answer)
        conn.commit()
        conn.close()
        counter = 0
        pointCounter = 0
        actualAnswers = []
        for item in answers:
            print('sql item')
            print(str(item[0]))
            actualAnswers.append(str(item[0]))
        print(actualAnswers)
        print('answers without u above')
        while counter < len(answers):
            if actualAnswers[counter] == str(userAnswers[counter]):
                print(answers[counter])
                pointCounter = pointCounter + 1
                counter = counter + 1
            else:
                print(answers[counter])
                print('not')
                print(userAnswers[counter])
                pointCounter = pointCounter
                counter = counter + 1
                print('no count')
        print("your points = " + str(pointCounter))
        GlobalPoints.insert(0, pointCounter)
        print(GlobalPoints)
        print('global points above')
    else:
        response_object['points'] = GlobalPoints[0]
    return jsonify(response_object)

@app.route('/receiveUsername', methods=['GET', 'POST'])
def receiveUsername():
    response_object = {}
    if request.method == 'POST':
        print('recieving username')
        post = request.get_json()
        username = post.get('username')
        print('username')
        print(username)
        conn = sqlite3.connect(database)
        cursor = conn.cursor()
        quizName_sql = cursor.execute('SELECT QuizName FROM Quiz WHERE QuizID={quizID};'.format(quizID=GlobalID[0]))
        quizName = []
        for quiz in quizName_sql:
            quizName.append(str(quiz[0]))
        cursor.execute('INSERT INTO Players(Username, QuizName, Points) VALUES ("{username}", "{quizName}", "{points}");'.format(username=username, quizName=quizName[0], points=GlobalPoints[0]))
        conn.commit()
        conn.close()
    else:
        print('getting')
        conn = sqlite3.connect(database)
        cursor = conn.cursor()
        sql_players = cursor.execute('SELECT Username, QuizName, Points FROM Players;')
        players = []
        for player in sql_players:
            players.append(player)
            response_object['users'] = players
    return jsonify(response_object)
# sanity check route

@app.route('/', methods=['GET', 'POST'])
def index():
    response_object = {'status': 'success'}
    if request.method == 'POST':
        post = request.get_json()
        print(post)
        actual_post = post.get('post')
        conn = sqlite3.connect(database)
        cursor = conn.cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS post(postID INTEGER PRIMARY KEY AUTOINCREMENT, post TEXT);')
        cursor.execute('INSERT INTO post(post) VALUES ("{post}");'.format(post=actual_post))

        conn.commit()
        conn.close()
    else:
        conn = sqlite3.connect(database)
        cursor = conn.cursor()
        sql_posts = cursor.execute('SELECT post FROM post;')
        posts = []
        for post in sql_posts:
            posts.append(post)
        conn.commit()
        conn.close()
        print(posts)
        response_object['posts'] = posts
        print(response_object)
    return jsonify(response_object)


if __name__ == '__main__':
    app.run()