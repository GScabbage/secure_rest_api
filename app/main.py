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

# @component External:Guest (#guest)
# @threat SQL Injection (#sqli)
# @threat DDOS Attack  (#ddos)
# @threat MITM Attack (#mitm)
# @threat Token Forgery (#faketoken)
# @threat Token Theft (#stolentoken)
# @threat Clickjack Attack (#clickjack)
# @threat MIME Sniffing (#mime)
def newuser(username, password):
    with closing(sqlite3.connect("users.db")) as connection:
        with closing(connection.cursor()) as cursor:
            cursor.execute(f"INSERT INTO user_info (username, password) VALUES (?,?);",(str(username), str(password),))
            connection.commit()

# @component CalcApp:Web:Server:TokenCheck (#tokencheck)
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
        with closing(sqlite3.connect("tokens.db")) as connection:
            with closing(connection.cursor()) as cursor:
                cursor.execute("SELECT * FROM banned_tokens WHERE token=?", (str(token),))
                tokencheck= cursor.fetchone()
                print(tokencheck)
        if tokencheck != None:
            return True
        else:
            return False
    else:
        return False

# @component CalcApp:Web:Server:Main (#main)
# @connects #guest to #main with HTTPS-Get
# @connects #main to #guest with HTTPS-Get
# @component CalcApp:Database:TokenDatabase:BannedToken (#bannedtokens)
# @connects #main to #calculator with User has valid token
# @connects #main to #tokencheck with Validate User Token
# @connects #tokencheck to #main with Token Validity Response
# @connects #tokencheck to #bannedtokens with SQL Query
# @connects #bannedtokens to #tokencheck with SQL Response
# @connects #tokencheck to #userdb with SQL Query
# @connects #userdb to #tokencheck with SQL Response
@flaskapp.route('/')
def index_page():
    try:
        with closing(sqlite3.connect("tokens.db")) as connection:
            with closing(connection.cursor()) as cursor:
                cursor.execute("CREATE TABLE banned_tokens (id INTEGER PRIMARY KEY, token TEXT);")
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

# @component CalcApp:Web:Server:Login (#login)
# @connects #main to #login with User Proceed to Login
# @connects #guest to #login with HTTPS-GET
# @connects #login to #guest with HTTPS-GET
@flaskapp.route('/login')
def login_page():#
    return render_template('login.html')

def create_token(username, password):
    validity = datetime.datetime.utcnow() + datetime.timedelta(days=15)
    token = jwt.encode({'user_id': 12345, 'username': username, 'expiry': str(validity)}, SECRET_KEY, "HS256")
    return token

# @component CalcApp:Web:Server:Authenticate (#authenticate)
# @connects #login to #authenticate with User Data Check
# @component CalcApp:Database:UserDatabase (#userdb)
# @connects #authenticate to #userdb with SQL Query
# @connects #userdb to #authenticate with SQL Response
# @connects #authenticate to #guest with HTTPS-GET
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
# @component CalcApp:Web:Server:Calculator (#calculator)
# @connects #authenticate to #calculator with Successful Login so Redirects to Calculator
# @connects #calculator to #tokencheck with Validate User Token
# @connects #tokencheck to #calculator with Token Validity Response
# @connects #guest to #calculator with HTTPS-GET
# @connects #calculator to #guest with HTTPS-GET
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

# @component CalcApp:Web:Server:NewUser (#newuser)
# @connects #authenticate to #newuser with User Data not in Database
# @connects #newuser to #main with User does not wish to create new account
# @connects #guest to #newuser with HTTPS-GET
# @connects #newuser to #guest with HTTPS-GET
@flaskapp.route('/newuser')
def newlogin():
    return render_template('newuser.html')

# @component CalcApp:Web:Server:NewUserAuthenticate (#newauth)
# @connects #newuser to #newauth with User wishes to creat a New account
# @connects #newauth to #userdb with SQL Insert
# @connects #newauth to #calculator with New User redirect to Calculator
# @connects #newauth to #guest with HTTPS-GET
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

# @component CalcApp:Web:Server:Calculator:Operations (#operations)
# @connects #calculator to #operations with User calculation request
# @connects #operations to #calculator with User calculation results
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

# @component CalcApp:Web:Server:Logout (#logout)
# @connects #calculator to #logout with User Logout Request
# @connects #logout to #main with Return to Main Page
# @connects #logout to #guest with HTTPS-GET
@flaskapp.route('/logout')
def logout():
    token = request.cookies['token']
    with closing(sqlite3.connect("tokens.db")) as connection:
        with closing(connection.cursor()) as cursor:
            cursor.execute(f"INSERT INTO banned_tokens (token) VALUES (?);",(str(token),))
            connection.commit()
    resp = make_response(render_template('logout.html'))
    resp.delete_cookie('token')
    return resp

# @connects #logout to #bannedtokens with SQL Insert current User Token
@flaskapp.after_request
def apply_caching(response):
    response.headers["X-Frame-Options"] = "SAMEORIGIN"
    response.headers['X-Content-Type-Options'] = "nosniff"
    return response

if __name__ == "__main__":
    flaskapp.run(host='0.0.0.0', debug = True, ssl_context = ('cert/cert.pem', 'cert/key.pem'))
# @exposes CalcApp:Web:Server to DDOS Attack with flooding the servers with too many requests
# @mitigates #main against #stolentoken with checking token with previously assigned tokens database
# @mitigates #calculator against #stolentoken with checking token with previously assigned tokens database
# @exposes #main to #faketoken with forging fake tokens
# @exposes #calculator to #faketoken with forging fake tokens
# @mitigates #login against #sqli with entering information to database as strings in a tuple so SQL code cannot be run by accident
# @mitigates #newuser against #sqli with entering information to database as strings in a tuple so SQL code cannot be run by accident
# @mitigates CalcApp:Web:Server against #clickjack with X-Frame options response header
# @mitigates CalcApp:Web:Server against #mime with X-Frame no sniff option enabled
