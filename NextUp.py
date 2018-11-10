import sys
import spotipy
import json
import spotipy.util as util


def show_tracks(tracks):
    lst = []
    lst2 = []
    for i, item in enumerate(tracks['items']):
        track = item['track']
        lst += [track["id"]]
        lst2 += [track["name"]]
    return lst, lst2


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


if len(sys.argv) > 3:
    username = sys.argv[1]
    playlist = sys.argv[2]
    track_ids = sys.argv[3:]
else:
    print("Usage: %s username playlist_id track_id ..." % (sys.argv[0],))
    sys.exit()

scope = 'playlist-modify-public'
token = util.prompt_for_user_token(username, scope, client_id='171b3cdfebb344ba9772c6859136c2d4',
                                   client_secret='Fca0bb0ea99f493d987b27c9568b79ee',
                                   redirect_uri='http://www.google.com/')

if token:
    sp = spotipy.Spotify(auth=token)
    sp.trace = False
    results = sp.user_playlist(username, playlist, fields="tracks,next")
    tracks = results['tracks']
    playlist_songs=show_tracks(tracks)[0]
    names = show_tracks(tracks)[1]
    for track in track_ids:
        if track in playlist_songs:
            track_ids.remove(track)
    if len(track_ids) >= 1:
        results = sp.user_playlist_add_tracks(username, playlist, track_ids)
    update_list(names)
else:
    print("Can't get token for", username)