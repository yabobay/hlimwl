from googleapiclient.discovery import build
import re
from math import ceil, floor
import time
from progress.bar import Bar
from progress.spinner import Spinner

# it's pretty hard to make an empty playlist on purpose, and even if
# you did, you're probably not trying to measure it's duration. so if
# we get this, it means there's probably something wrong with the
# playlist.
class EmptyPlaylistError(Exception): pass

def videoLength(video_id):
    # TODO: add converting from URL
    length = youtube\
        .videos().list(part='contentDetails', id=video_id).execute()\
        ['items'][0]['contentDetails']['duration']
    conversions = {"D": 86400, "H": 3600, "M": 60, "S": 1}
    return sum([int(i[:-1]) * conversions[i[-1]]
                for i in re.compile(r"\d+[DHMS]").findall(length)])

def playlistVids(playlist_id):
    if loud: spinner = Spinner("Counting vids... ")
    vids = []
    page = ''
    while True:
        result = youtube.playlistItems()\
                        .list(part='snippet,status',
                              playlistId=playlist_id,
                              pageToken=page)\
                        .execute()
        if result['items'] == []:
            raise EmptyPlaylistError
        vids += [vid['snippet']['resourceId']['videoId'] for vid in result['items']
                 if vid['status']['privacyStatus'] != "private"]
        try:
            page = result['nextPageToken']
        except KeyError:
            break
        if loud: spinner.next()
    if loud: print('', len(vids))
    return vids

def playlistLength(playlist_id):
    vids = playlistVids(playlist_id)
    if loud: bar = Bar("Getting length of vids...", max=len(vids))
    seconds = 0
    for vid in vids:
        seconds += videoLength(vid)
        if loud: bar.next()
    if loud: print()
    return seconds

def formatTime(seconds):
    s = time.strftime('%H:%M:%S', time.gmtime(seconds))
    days = floor(seconds / 86400)
    if days:
        s = f"{days} days, {s}"
    return s

loud = __name__ == "__main__"

_key = 'AIzaSyBozcYO6eF75fXGXVpGD_-DfzgmwI7wa8o'
youtube = build('youtube', 'v3', developerKey=_key)

if __name__ == "__main__":
    try:
        print(formatTime(playlistLength('WL')))
    except EmptyPlaylistError:
        print("Empty Playlist!\nMaybe the playlist is private?")

youtube.close()
