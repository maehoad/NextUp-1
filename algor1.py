
import json

FILENAME = "votes.json"


def get_votes():
    with open(FILENAME) as file:
        return json.load(file)


def set_votes(votes):
    with open(FILENAME, 'w') as file:
        return json.dump(votes, file, indent=2)


def vote_for(song):
    votes = get_votes()
    votes[song]['votes'] += 1
    set_votes(votes)


def add_song(song):
    votes = get_votes()
    votes[song]['votes'] = 0
    set_votes(votes)


def clear_songs(): # sets all song votes to zero
    votes = get_votes()
    for song in votes:
        votes[song] = 0
    set_votes(votes)


def most_popular():
    votes = get_votes()
    popularVote = 0
    popular = None
    for song in votes:
        if popular == None: # for first song in the list, sets to best
            popular = song
            popularVote = votes[song]
        # if equal votes, returns first song in list (ie higher in queue)
        if votes[song] > popularVote: # if song has more votes, sets to best
            popularVote = votes[song]
            popular = song
    return popular #returns the string


def best_songs():
    votes = get_votes()
    # finList = []
    # for key in votes:
    #     if finList == []:
    #         finList.append((key, votes[key]))
    #     else:
    #         x = len(finList)
    #         for i in range(len(finList)):
    #             if finList[i][1] < votes[key]:
    #                 finList.insert(i, (key, votes[key]))
    #                 break
    #         y = len(finList)
    #         if x == y:
    #             finList.append((key, votes[key]))
    # return finList

    result = list(votes.values())
    result.sort(key=lambda song: song['votes'])
    result.reverse()
    return result

