from flask import Flask, jsonify, send_file
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC
from io import BytesIO
from flask_cors import CORS, cross_origin
import base64, pymongo, os, requests
from pymongo import MongoClient
from uuid import uuid4

app = Flask(__name__)

app.config['SECRET_KEY'] = 'this is the secret'
app.config['CORS_HEADERS'] = 'Content-Type'

# Directory containing songs
directory = '/var/lib/songs/data'

cors = CORS(app, resources={r"/foo": {"origins": "http://localhost:port"}})

def get_db():
    client = MongoClient(host='mongo_db',
                         port=27017,
                         username='root',
                         password='pass',
                         authSource='admin')
    
    db = client["songs_db"]
    return db

def convert(seconds):
    minutes = seconds // 60
    seconds %= 60

    return "%02d:%02d" % (minutes, seconds)

# Function to recursively traverse a directory and get list of songs
def get_songs_from_directory(directory):
    songs = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.mp3'):
                song_path = os.path.join(root, file)
                song_name = os.path.splitext(file)[0]
                songs.append({'id': str(uuid4()), 'name': song_name, 'path': song_path})
    return songs

# Function to sync songs with MongoDB
def sync_songs_with_mongodb(directory):
    db = get_db()

    # Get list of songs from file system
    file_system_songs = get_songs_from_directory(directory)
    
    # Get list of songs from MongoDB
    mongo_songs = [song['path'] for song in db.songs.find({}, {'_id': 0, 'path': 1})]
    
    # Songs to be inserted into MongoDB
    new_songs = [song for song in file_system_songs if song['path'] not in mongo_songs]
    
    # Songs to be removed from MongoDB
    removed_songs = [song['path'] for song in db.songs.find({'path': {'$nin': [song['path'] for song in file_system_songs]}}, {'_id': 0, 'path': 1})]
    
    # Insert new songs into MongoDB
    if new_songs:
        db.songs.insert_many(new_songs)
        print(f'{len(new_songs)} new songs inserted into MongoDB.')
    else:
        print("No new songs added!")
    
    # Remove songs from MongoDB
    if removed_songs:
        db.songs.delete_many({'path': {'$in': removed_songs}})
        print(f'{len(removed_songs)} songs removed from MongoDB.')
    else:
        print("No songs deleted!")

@app.route('/song/<song_id>', methods=['GET'])
@cross_origin(origin='localhost',headers=['Content- Type','Authorization'])
def post_song(song_id):
    db = get_db()
    song = db.songs.find_one({"id": song_id})

    if(song):
        file_path = song["path"]
        return send_file(file_path, mimetype='audio/mpeg')
    else:
        return jsonify({'error': 'Song not found'}), 404
    
@app.route('/songs')
def fetch_songs():
    db = get_db()
    _songs = db.songs.find()
    songs = [{"id": song["id"], "name": song["name"], "path": song["path"] } for song in _songs]
    return jsonify({"songs": songs})

@app.route('/api/songs/<string:email>')
def get_songs(email):
    db = get_db()
    songs = db.songs.find()
    song_list = []

    # Fetch the list of favorite song IDs for the user
    response = requests.get(f'http://auth_service:5001/favourites/{email}')
    if response.status_code == 200:
        favourite_songs = response.json()['song_ids']
    else:
        favourite_songs = []

    for song in songs:
        # Extract image from MP3 file
        mp3 = MP3(song['path'], ID3=ID3)

        # Extract artist and album from MP3 tags
        artist = mp3.tags.get('TPE1').text[0] if 'TPE1' in mp3 else None
        album = mp3.tags.get('TALB').text[0] if 'TALB' in mp3 else None
        duration = convert(int(mp3.info.length))

        if 'APIC:' in mp3:
            apic = mp3.tags.get('APIC:')
            image_data = BytesIO(apic.data)
            image_data.seek(0)
            # Convert image to base64
            image_base64 = base64.b64encode(image_data.read()).decode('utf-8')
            song_info = {
                'id': song['id'],
                'name': song['name'],
                'artist': artist,
                'album': album,
                'duration': duration,
                'image': image_base64
            }
        else:
            # If no image is found, include only ID and name
            song_info = {
                'id': song['id'],
                'name': song['name'],
                'artist': artist,
                'album': album,
                'duration': duration
            }

        # Check if the song is a favorite
        if song['id'] in favourite_songs:
            song_info['favourite'] = True
        else:
            song_info['favourite'] = False

        song_list.append(song_info)

    return jsonify(song_list)

@app.route('/')
def ping_server():
    return "Ping!"

if __name__ == '__main__':
    # Sync songs with MongoDB
    sync_songs_with_mongodb(directory)
    
    app.run(host='0.0.0.0', port=5000)