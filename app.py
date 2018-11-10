from flask import Flask, jsonify, request, abort
from algor1 import *
from NextUp import reorder_by_votes

app = Flask(__name__)


@app.route('/')
def home():
    return "Hello World"


@app.route('/songs/votes')
def song_dict():
    songs = get_votes()
    return jsonify(songs)


@app.route('/songs/ordered')
def ordered_songs():
    songs = best_songs()
    return jsonify(songs)


@app.route('/songs/best')
def best_song():
    songs = most_popular()
    return jsonify(songs)


@app.route('/reset')
def reset_songs():
    songs = clear_songs()
    return jsonify(songs)


@app.route('/vote', methods=['POST'])
def cast_vote():
    song = request.args.get('song')
    try:
        vote_for(song)
    except KeyError:
        abort(400)

    reorder_by_votes()
    return "Voted for song"
