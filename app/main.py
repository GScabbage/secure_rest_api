from flask import Flask, make_response, request, render_template, redirect, jsonify
from random import random
import jwt
import datetime
import sqlite3
from contextlib import closing
import time
import operations
import calc_functions as calc_functions

SECRET_KEY = "54F192A913832BACAEDCCBBE6BE15"
flaskapp = Flask(__name__)

def newuser(username, password):
    with closing(sqlite3.connect("users.db")) as connection:
        with closing(connection.cursor()) as cursor:
            cursor.execute(f"INSERT INTO user_info (username, password) VALUES (?,?);",(str(username), str(password),))
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

def is_token_banned(token):
    if token:
        with closing(sqlite3.connect("bannedtokens.db")) as connection:
            with closing(connection.cursor()) as cursor:
                cursor.execute("SELECT * FROM token_list WHERE token=?", (str(token),))
                tokencheck= cursor.fetchone()
                print(tokencheck)
        if tokencheck != None:
            return True
        else:
            return False
    else:
        return False

@flaskapp.route('/')
def index_page():
    try:
        with closing(sqlite3.connect("bannedtokens.db")) as connection:
            with closing(connection.cursor()) as cursor:
                cursor.execute("CREATE TABLE token_list (id INTEGER PRIMARY KEY, token TEXT);")
                connection.commit()
    except:
        pass
    print(request.cookies)
    isUserLoggedIn = False

    if 'token' in request.cookies:
        tokenbanned=is_token_banned(request.cookies['token'])
        if tokenbanned == False:
            isUserLoggedIn = verify_token(request.cookies['token'])
        else:
            isUserLoggedIn = False

    if isUserLoggedIn:
        return render_template('calculator.html')
    else:
        return render_template('main.html')

# @flaskapp.route('/index')
# def index2_page():
#     return render_template('index.html')

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
            cursor.execute("SELECT * FROM user_info WHERE username=? and password=?", (str(username),str(password),))
            udat= cursor.fetchone()
    if udat == None:
        return render_template('newaccount.html')
    else:
        user_token = create_token(username, password)
        resp = make_response(render_template('loginredirect.html'))
        resp.set_cookie('token', user_token, httponly=True, secure=True, samesite='Strict')
        return resp

@flaskapp.route('/calculator', methods=['POST','GET'])
def send(sum=sum):
    print(request.cookies)
    isUserLoggedIn = False

    if 'token' in request.cookies:
        tokenbanned=is_token_banned(request.cookies['token'])
        if tokenbanned == False:
            isUserLoggedIn = verify_token(request.cookies['token'])
        else:
            isUserLoggedIn = False

    if isUserLoggedIn:
        return render_template('calculator.html')
    else:
        return render_template('nocalc.html')

    # if isUserLoggedIn:
    #     if request.method == 'POST':
    #         num1 = request.form['num1']
    #         num2 = request.form['num2']
    #         operation = request.form['operation']
    #
    #         if operation == 'add':
    #             sum = float(num1) + float(num2)
    #             return render_template('calculator.html', sum=sum)
    #
    #         elif operation == 'subtract':
    #             sum = float(num1) - float(num2)
    #             return render_template('calculator.html', sum=sum)
    #
    #         elif operation == 'multiply':
    #             sum = float(num1) * float(num2)
    #             return render_template('calculator.html', sum=sum)
    #
    #         elif operation == 'divide':
    #             if float(num2) != 0:
    #                 sum = float(num1) / float(num2)
    #                 return render_template('calculator.html', sum=sum)
    #             else:
    #                 return render_template('calculator.html', sum="That's a zero division error")
    #         else:
    #             return render_template('calculator.html')
    #     else:
    #         return render_template('calculator.html')
    # else:
    #     return render_template('nocalc.html')

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
    resp.set_cookie('token', user_token, httponly=True, secure=True, samesite='Strict')
    return resp

@flaskapp.route('/calculate2', methods = ['POST'])
def calculate_post2():
    print(request.form)
    number_1 = request.form.get('number_1', type = float)
    number_2 = request.form.get('number_2', type = float)
    operation= request.form.get('operation', type= str)

    result = calc_functions.process(number_1, number_2, operation)

    print(result)
    response_data = {
        'data': result
    }
    return make_response(jsonify(response_data))

@flaskapp.route('/logout')
def logout():
    token = request.cookies['token']
    with closing(sqlite3.connect("bannedtokens.db")) as connection:
        with closing(connection.cursor()) as cursor:
            cursor.execute(f"INSERT INTO token_list (token) VALUES (?);",(str(token),))
            connection.commit()
    resp = make_response(render_template('logout.html'))
    resp.delete_cookie('token')
    return resp

@flaskapp.after_request
def apply_caching(response):
    response.headers["X-Frame-Options"] = "SAMEORIGIN"
    response.headers['X-Content-Type-Options'] = "nosniff"
    return response

if __name__ == "__main__":
    flaskapp.run(host='0.0.0.0', debug = True, ssl_context = ('cert/cert.pem', 'cert/key.pem'))
