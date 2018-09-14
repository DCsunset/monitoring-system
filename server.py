from flask import Flask, request, make_response, send_from_directory, abort, Response
import jwt
import json
from auth import auth
import userdb
from video import Video

# For jwt
key = 'lknawevuiasodnv'

app = Flask(__name__, static_url_path='')
db = userdb.userdb('users.db')

system_video = None
rstp_video = None
rstp_options = None

@app.route('/', methods=['GET'])
def index():
    return send_from_directory('public', 'index.html')

@app.route('/static/<path:path>', methods=['GET'])
def static_assets(path):
    return send_from_directory('public/static', path)

@app.route('/api/video/system', methods=['GET'])
def systemVideo():
    # Authorize first
    token = request.cookies.get('token')
    if not auth(token):
        abort(403)

    global system_video
    if not system_video:
        system_video = Video()

    # generator
    def generate_frame(video):
        while True:
            frame = video.get_frame()
            yield b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n'

    # Streaming contents
    return Response(generate_frame(system_video), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/api/video/rstp', methods=['GET', 'POST'])
def rstpVideo():
    # Authorize first
    token = request.cookies.get('token')
    if not auth(token):
        abort(403)

    global rstp_video
    global rstp_options

    if request.method == 'GET':
        if not rstp_options:
            return 'Configure RSTP first'
        if not rstp_video:
            rstp_video = Video(rstp_options)

        # generator
        def generate_frame(video):
            while True:
                frame = video.get_frame()
                yield b'--frame\r\nContent-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n'

        # Streaming contents
        return Response(generate_frame(rstp_video), mimetype='multipart/x-mixed-replace; boundary=frame')
    elif request.method == 'POST':
        rstp_options = request.get_json()
        return json.dumps({ 'success': True })

    return json.dumps({ 'success': False })

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

app.run('0.0.0.0', 5000)
