from flask import Flask, render_template, request
import sqlite3

database = 'music.db'

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/createArtist", methods=["POST"])
def createArtist():
    #artistID = request.form.get("artistID")
    artistName = request.form.get("artistName")

    conn = sqlite3.connect(database)
    cursor = conn.cursor()

    cursor.execute('CREATE TABLE IF NOT EXISTS artist(artistID INTEGER PRIMARY KEY AUTOINCREMENT, artistName TEXT);')
    #cursor.execute('CREATE TABLE artist(ArtistID INTEGER, ArtistName TEXT, PRIMARY KEY(ArtistID) );')
    cursor.execute('INSERT INTO artist ( artistName) VALUES ( "{artistName}");'.format(artistName=artistName))

    conn.commit()
    conn.close()

    return render_template('index.html')
@app.route("/track")
def track():
    return render_template('track.html')

@app.route("/createTrack", methods=["POST"])
def createTrack():
    #trackID = request.form.get("trackID")
    trackName = request.form.get("trackName")
    artistName = request.form.get("artistName")

    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    artistIDList = []
    cursor.execute('CREATE TABLE IF NOT EXISTS track(trackID INTEGER PRIMARY KEY AUTOINCREMENT, trackName TEXT, trackArtistID INTEGER, FOREIGN KEY(trackArtistID) REFERENCES artist(artistID));')
    artistID = cursor.execute('SELECT artistID FROM artist WHERE artistName="{artistName}"'.format(artistName=artistName))
    print(artistID)
    for artist in artistID:
        print(artist)
        for ID in artist:
            artistID = [ID]
    cursor.execute('INSERT INTO track (trackName, trackArtistID) VALUES ("{trackName}", {trackArtistID});'.format(trackName=trackName, trackArtistID=artistID[0]))
    conn.commit()
    conn.close()

    return render_template('track.html')ts

@app.route("/trackdb", methods=["GET", "POST"])
def trackdb():
    trackArray = []

    conn = sqlite3.connect(database)
    cursor = conn.cursor()

    tracks = cursor.execute('SELECT * FROM track;')

    for track in tracks:
        trackArray.append(track)

    conn.close()

    return render_template('trackdb.html', trackArray=trackArray)

@app.route("/dbartist")
def dbartist():
    artistArray = []

    conn = sqlite3.connect(database)
    cursor = conn.cursor()

    artists = cursor.execute('SELECT * FROM artist')

    for artist in artists:
        artistArray.append(artist)

    conn.close()

    return render_template('artistdb.html', artistArray=artistArray)

@app.route("/db")
def db():
    return render_template('db.html')


@app.route("/queryartist", methods=["POST", "GET"])
def queryartist():
    artistName = request.form.get("artistName")

    artistSongList = []
    conn = sqlite3.connect(database)
    cursor = conn.cursor()
    artistID = cursor.execute('SELECT artistID FROM artist WHERE artistName="{artistName}"'.format(artistName=artistName))
    for artist in artistID:
        for ID in artist:
            artistID = [ID]
    artistSong = cursor.execute('SELECT * FROM track WHERE trackArtistID={artistID};'.format(artistID=artistID[0]))

    for info in artistSong:
        artistSongList.append(info)

    return render_template('db.html', infoList=artistSongList)
    conn.close()
app.run(host='0.0.0.0', port=5000)