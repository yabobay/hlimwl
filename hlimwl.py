from datetime import timedelta
import ytdl_object
import argparse
from sys import argv

def main():
    parser = argparse.ArgumentParser(prog='HLIMWL',
                                     description='How Long Is My Watch Later?')
    parser.add_argument('-p', help='playlist to check the length of',
                        metavar='playlist', default=':ytwatchlater',
                        required=False)
    parser.add_argument('-v', help='verbose mode', action='store_true')
    args = parser.parse_args()
    global ytdl # this script is garbage
    ytdl = ytdl_object.makeYtdlObject(args.v)
    printPlaylistDuration(args.p)

def duration(video): # can be playlist also
    物件 = {} # it means object
    vid = ytdl.extract_info(video, download=False)
    if 'duration' in vid.keys(): # its a single video
        物件['type'] = 'video'
        dur = vid['duration']
    elif 'entries' in vid.keys(): # it's a playlist
        物件['type'] = 'playlist'
        物件['videos'] = len(vid['entries'])
        dur = 0
        for i in vid['entries']:
            try:
                dur += i['duration']
            except TypeError:
                # its a private video i guess :P
                pass
    物件['duration'] = dur
    return 物件

def printPlaylistDuration(playlist):
    try:
        pl = duration(playlist)
        length = pl['duration']
        pvideos = pl['videos']
        plength = str(timedelta(seconds=length))
        message = f"Your playlist contains {pvideos} videos and is {plength} long."
        if length > 36000: # 10 hours
            message += " Yikes!"
        print(message)
    except NameError:
        print("No browser found :(",
              "You need to login to YouTube in some web browser.",
              sep="\n")

if __name__ == '__main__':
    main()
