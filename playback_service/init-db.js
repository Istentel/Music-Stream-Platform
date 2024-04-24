db = db.getSiblingDB("songs_db");
db.songs.drop();

db.songs.insertMany([
    {
        "id": 1,
        "name": "Allie_X_Downtown",
        "path": "/var/lib/songs/data/Allie_X_Downtown.mp3",
    },
    {
        "id": 2,
        "name": "song2",
        "path": "..."
    },
]);