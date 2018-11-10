# README: The purpose of this file is to update the local json file to include all the songs in the Spotify playlist,
# and then reorder the playlist to have the songs with the most votes appear first on the playlist.
# Note this file does NOT add votes to the json file
# For this file to work in conjunction with the app you MUST call the file, then add a username ("diegofinni" in our
# case), followed by an id of the playlist and then the ids of all the tracks you want to add to the playlist
# Example of calling file on terminal: python3 NextUp.py diegofinni 5K3rtFT1Tq19lJ04wjuVBV 59WN2psjkt1tyaxjspN8fp
# The client data needed for this file to work (CLIENT ID, SECRET, and REDIRECT_URI) are already given

import sys
import spotipy
import spotipy.util as util
from algor1 import *

#######################################################################################################################
# These functions fetch a json file and then add any song to the json
# file that is not already on it and gives it a default value of 0

filename = "votes.json"


def get_list():
    with open(filename) as file:
        return json.load(file)


def update_list(lst):
    dic = get_list()
    for song in lst:
        if song not in dic:
            dic[song] = 0

    set_list(dic)


def set_list(dic):
    with open(filename, 'w') as file:
        return json.dump(dic, file, indent=2)


def read_playlist():
    with open(filename, "r") as file:
        return json.load(file)


########################################################################################################################

# This function sorts through the playlist to make
# a list of the ids and a list of the song titles
def show_tracks(tracks):
    names = []
    ids = []
    for i, item in enumerate(tracks['items']):
        track = item['track']
        names += [track["id"]]
        ids += [track["name"]]
    return names, ids


# This function reorders the Spotify playlist
# based on votes found in the json file
def reorder_playlist(sp, names):
    new_order = best_songs()
    for i in range(len(new_order) -1, -1, -1):
        for j in range(len(names)):
            if new_order[i][0] == names[j]:
                names.insert(0, names[j])
                names.pop(j + 1)
                sp.user_playlist_reorder_tracks(username, playlist, j, 0, 1)


# This if/else makes sure all the Spotify data (id, secret, uri) are inputted
# Note that it is assumed you are inputting a username, playlist, and a list of track_ids
# HACK
username = "diegofinni"
playlist = "5K3rtFT1Tq19lJ04wjuVBV"
track_ids = ["59WN2psjkt1tyaxjspN8fp"]
# HACK

scope = 'playlist-modify-public'
# Example data
token = util.prompt_for_user_token(username, scope, client_id='171b3cdfebb344ba9772c6859136c2d4',
                                   client_secret='Fca0bb0ea99f493d987b27c9568b79ee',
                                   redirect_uri='http://www.google.com/')

# If a valid token is used, this if statement compiles all of the helper
#  functions to execute the purpose of this file(read README if confused)
def reorder_by_votes():
    sp = spotipy.Spotify(auth=token)
    sp.trace = False
    results = sp.user_playlist(username, playlist, fields="tracks,next")
    tracks = results['tracks']
    song_ids = show_tracks(tracks)[0]
    names = show_tracks(tracks)[1]
    for track in track_ids:
        if track in song_ids:
            track_ids.remove(track)
    if len(track_ids) >= 1:
        results = sp.user_playlist_add_tracks(username, playlist, track_ids)
    update_list(names)
    reorder_playlist(sp, names)

########################################################################################################################
