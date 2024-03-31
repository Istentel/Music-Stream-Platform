from flask import Flask, jsonify, send_file
import pymongo
from pymongo import MongoClient

app = Flask(__name__)

def get_db():
    client = MongoClient(host='mongo_db',
                         port=27017,
                         username='root',
                         password='pass',
                         authSource='admin')
    
    db = client["songs_db"]
    return db

@app.route('/song')
def post_song():
    db = get_db()
    song = db.songs.find_one({"id": "1"})
    if(song):
        file_path = song["path"]
        return send_file(file_path, mimetype='audio/mpeg')
    else:
        return jsonify({'message': 'Song is not valid'}) 

@app.route('/songs')
def fetch_songs():
    db = get_db()
    _songs = db.songs.find()
    songs = [{"id": song["id"], "name": song["name"], "path": song["path"] } for song in _songs]
    return jsonify({"songs": songs})

@app.route('/')
def ping_server():
    return "Ping!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)