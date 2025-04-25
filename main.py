from flask import Flask, jsonify, request  # добавлен request
from model.twit import Twit  # раскомментировать, если файл model/twit.py существует
import json

twits = []  # исправлено с {} на []

app = Flask(__name__)

class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Twit):
            return {'body': obj.body, 'user': obj.user}
        return super().default(obj)

app.json_encoder = CustomJSONEncoder  # можно заменить на JSONProvider в новых версиях

@app.route('/ping', methods=['GET'])
def ping():
    return jsonify({'response': 'pong'})

@app.route('/twit', methods=['POST'])
def create_twit():
    '''{"body": "Hello World", "author": "@aqaguy"}'''
    twit_json = request.get_json()
    twit = Twit(twit_json['body'], twit_json['author'])
    twits.append(twit)
    return jsonify({'status': 'success'})

@app.route('/twit', methods=['GET']) 
def read_twits():
    return jsonify({'twits': [vars(t) for t in twits]})

@app.route('/twit/<int:index>', methods=['PUT'])
def update_twit(index):
    '''Пример запроса:
    PUT /twit/0
    {
        "body": "Updated text",
        "author": "@newauthor"
    }
    '''
    if index < 0 or index >= len(twits):
        return jsonify({'error': 'Twit not found'}), 404

    data = request.get_json()
    twits[index].body = data.get('body', twits[index].body)
    twits[index].author = data.get('author', twits[index].author)
    return jsonify({'status': 'updated', 'twit': vars(twits[index])})

@app.route('/twit/<int:index>', methods=['DELETE'])
def delete_twit(index):  #Postman localhost:5000/twit/1
    if index < 0 or index >= len(twits):
        return jsonify({'error': 'Twit not found'}), 404

    deleted = twits.pop(index)
    return jsonify({'status': 'deleted', 'twit': vars(deleted)})

if __name__ == '__main__':
    app.run(debug=True) # запускает встроенный сервер Flask в режиме отладки
