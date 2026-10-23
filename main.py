from flask import Flask, render_template, request, jsonify, send_from_directory
import os, json

app = Flask(__name__)


def load_json(file, default):
    try:
        if os.path.exists(file):
            with open(file, 'r') as f: return json.load(f)
    except:
        pass
    return default


def save_json(file, data):
    with open(file, 'w') as f: json.dump(data, f)


messages = load_json('messages.json', [])
users_db = load_json('users.json', [])


@app.route('/api/register', methods=['POST'])
def register():
    data = request.json
    if data:
        users_db.append(data);
        save_json('users.json', users_db)
        return jsonify({"status": "ok"})
    return jsonify({"status": "error"})


@app.route('/api/users', methods=['GET'])
def get_users(): return jsonify(users_db)


@app.route('/api/messages', methods=['GET'])
def get_messages(): return jsonify(messages)


@app.route('/api/send', methods=['POST'])
def send():
    data = request.json
    if data:
        messages.append(data);
        save_json('messages.json', messages)
        return jsonify({"status": "ok"})
    return jsonify({"status": "error"})


@app.route('/')
def index(): return render_template('chat.html')


@app.route('/manifest.json')
def manifest(): return send_from_directory('static', 'manifest.json')


@app.route('/static/<path:path>')
def static_files(path): return send_from_directory('static', path)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
