from datetime import timedelta
from ytdl_object import ytdl
import argparse
from sys import argv

def duration(video): # can be playlist also
    vid = ytdl.extract_info(video, download=False)
    if 'duration' in vid.keys(): # its a single video
        dur = vid['duration']
    elif 'entries' in vid.keys(): # it's a playlist
        dur = 0
        for i in vid['entries']:
            try:
                dur += i['duration']
            except TypeError:
                # its a private video i guess :P
                pass
    return dur

def printPlaylistDuration(playlist=':ytwatchlater'):
    try:
        length = duration(playlist)
        plength = str(timedelta(seconds=length))
        message = f"Your Watch Later playlist is {plength} long."
        if length > 36000: # 10 hours
            message += " Yikes!"
        print(message)
    except NameError:
        print("No browser found :(",
              "You need to login to YouTube in some web browser.",
              sep="\n")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='HLIMWL',
                                     description='How Long Is My Watch Later?')
    parser.add_argument('playlist',
                        help='check the length of any playlist')
    if len(argv[1:]) == 0:
        printPlaylistDuration()
    else:
        args = parser.parse_args()
        printPlaylistDuration(args.playlist)
