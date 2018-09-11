from flask import Flask, request, make_response, send_from_directory, abort
import jwt
import json
from auth import auth
import userdb

# For jwt
key = 'lknawevuiasodnv'

app = Flask(__name__, static_url_path='')
db = userdb.userdb('users.db')

@app.route('/', methods=['GET'])
def index():
    return send_from_directory('public', 'index.html')

@app.route('/static/<path:path>', methods=['GET'])
def static_assets(path):
    return send_from_directory('public/static', path)

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    if data:
        res = db.login(data['username'], data['password'])
        if res:
            resp = make_response(json.dumps({ 'success': True }))
            token = jwt.encode({ 'user': data['username'] }, key, algorithm='HS256')
            resp.set_cookie('token', token)
            return resp
    return json.dumps({ 'success': False })

@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    if data:
        res = db.register(data['username'], data['password'])
        if res:
            return json.dumps({ 'success': True })
        else:
            return json.dumps({ 'success': False, 'data': 'User already exists'})
    return json.dumps({ 'success': False, 'data': 'No available info'})

@app.route('/api/logout', methods=['GET'])
def logout():
    resp = make_response(json.dumps({ 'success': True }))
    resp.set_cookie('token', '', expires=0)
    return resp

@app.route('/api/user', methods=['GET'])
def get_user():
    token = request.cookies.get('token')
    if token:
        try:
            user = jwt.decode(token, key, algorithm='HS256')['user']
            return json.dumps({ 'success': True, 'data': user })
        except:
            pass
    return json.dumps({ 'success': False })

