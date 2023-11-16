from googleapiclient.discovery import build
import re
from math import ceil, floor
import time
from progress.bar import Bar
from progress.spinner import Spinner

# it's pretty hard to make an empty playlist on purpose, and even if
# you did, you're probably not trying to measure it's duration. so if
# we get this error, it means there's probably something wrong with
# the playlist. (i.e. it's private)
class EmptyPlaylistError(Exception): pass
class InvalidYouTubeURLError(Exception): pass

def videoLength(video_id):
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

def parseURL(url):
    import urllib.parse
    parsed = urllib.parse.urlparse(url)
    query = urllib.parse.parse_qs(parsed.query)
    match parsed.path:
        case "/playlist":
            return {"type": "playlist", "id": query['list'][0]}
        case "/watch":
            return {"type": "video", "id": query['v'][0]}
        case _:
            raise InvalidYouTubeURLError

def magicGetLength(url):
    stuff = parseURL(url)
    funcs = {"playlist": lambda x: playlistLength(x),
             "video": lambda x: videoLength(x)}
    return funcs[stuff["type"]](stuff["id"])

loud = __name__ == "__main__"

_key = 'AIzaSyBozcYO6eF75fXGXVpGD_-DfzgmwI7wa8o'
youtube = build('youtube', 'v3', developerKey=_key)

if __name__ == "__main__":
    import argparse
    from sys import argv, exit
    if len(argv) < 2: argv.append("-h") 
    parser = argparse.ArgumentParser(prog="How Long Is My Watch Later?",
                                     description="Name is a misnomer, this program cannot actually get the length of your watch later. But at least it can get the length of other playlists!",
                                     epilog="Available on https://gitea.com/yabobay/hlimwl. Thank you! :)")
    parser.add_argument("url", help="playlist or video to measure")
    parser.add_argument("-q", "--quiet", help="only print length", action='store_true')
    parser.add_argument("-s", "--seconds", help="don't format timestamp (implies -q)", action='store_true')
    args = parser.parse_args()
    try:
        useSeconds = args.seconds
        loud = not(useSeconds or args.quiet)
        seconds = magicGetLength(args.url)
        if useSeconds:
            print(seconds)
        else:
            print(formatTime(seconds))
    except InvalidYouTubeURLError:
        print("That doesn't look like a valid video or playlist URL. :/")
    except EmptyPlaylistError:
        print("Empty Playlist!\nMaybe the playlist is private?")

youtube.close()
