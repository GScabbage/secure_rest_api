from flask import Flask, make_response, request, render_template
from random import random
import jwt
import datetime
import sqlite3
from contextlib import closing
import time

SECRET_KEY = "54F192A913832BACAEDCCBBE6BE15"
flaskapp = Flask(__name__)

def newuser(username, password):
    with closing(sqlite3.connect("users.db")) as connection:
        with closing(connection.cursor()) as cursor:
            cursor.execute("INSERT INTO user_info (username, password) VALUES (?,?)",(username, password,))
            connection.commit()

def verify_token(token):
    if token:
        decoded_token = jwt.decode(token, SECRET_KEY, "HS256")
        with closing(sqlite3.connect("users.db")) as connection:
            with closing(connection.cursor()) as cursor:
                cursor.execute("SELECT * FROM user_info WHERE username=?", (decoded_token.get('username'),))
                udat= cursor.fetchone()
        if udat != None:
            return True
        else:
            return False
    else:
        return False

@flaskapp.route('/')
def index_page():
    print(request.cookies)
    isUserLoggedIn = False

    if 'token' in request.cookies:
        isUserLoggedIn = verify_token(request.cookies['token'])

    if isUserLoggedIn:
        return render_template('calculator.html')
    else:
        return render_template('main.html')

@flaskapp.route('/login')
def login_page():#
    return render_template('login.html')

def create_token(username, password):
    validity = datetime.datetime.utcnow() + datetime.timedelta(days=15)
    token = jwt.encode({'user_id': 12345, 'username': username, 'expiry': str(validity)}, SECRET_KEY, "HS256")
    return token

@flaskapp.route('/authenticate', methods = ['POST'])
def authenticate_users():
    try:
        with closing(sqlite3.connect("users.db")) as connection:
            with closing(connection.cursor()) as cursor:
                cursor.execute("CREATE TABLE user_info (id INTEGER PRIMARY KEY, username TEXT, password TEXT);")
                connection.commit()
    except:
        pass
    data=request.form
    username = data['username']
    password = data['password']
    with closing(sqlite3.connect("users.db")) as connection:
        with closing(connection.cursor()) as cursor:
            cursor.execute("SELECT * FROM user_info WHERE username=? and password=?", (username,password,))
            udat= cursor.fetchone()
    if udat == None:
        return render_template('newaccount.html')
    else:
        user_token = create_token(username, password)
        resp = make_response(render_template('loginredirect.html'))
        resp.set_cookie('token', user_token)
        return resp

@flaskapp.route('/calculator', methods=['POST','GET'])
def send(sum=sum):
    print(request.cookies)
    isUserLoggedIn = False

    if 'token' in request.cookies:
        isUserLoggedIn = verify_token(request.cookies['token'])

    if isUserLoggedIn:
        if request.method == 'POST':
            num1 = request.form['num1']
            num2 = request.form['num2']
            operation = request.form['operation']

            if operation == 'add':
                sum = float(num1) + float(num2)
                return render_template('calculator.html', sum=sum)

            elif operation == 'subtract':
                sum = float(num1) - float(num2)
                return render_template('calculator.html', sum=sum)

            elif operation == 'multiply':
                sum = float(num1) * float(num2)
                return render_template('calculator.html', sum=sum)

            elif operation == 'divide':
                if float(num2) != 0:
                    sum = float(num1) / float(num2)
                    return render_template('calculator.html', sum=sum)
                else:
                    return render_template('calculator.html', sum="That's a zero division error")
            else:
                return render_template('calculator.html')
        else:
            return render_template('calculator.html')
    else:
        return "Please login to access this page"

@flaskapp.route('/newuser')
def newlogin():
    return render_template('newuser.html')

@flaskapp.route('/newuserauthenticate', methods=['POST','GET'])
def authenticate_newuser():
    data=request.form
    username = data['username']
    password = data['password']
    newuser(username,password)
    user_token = create_token(username, password)
    resp = make_response(render_template('loginredirect.html'))
    resp.set_cookie('token', user_token)
    return resp

if __name__ == "__main__":
    flaskapp.run(debug = True, ssl_context = ('cert/cert.pem', 'cert/key.pem'))
