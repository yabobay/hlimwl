from datetime import timedelta
import ytdl_object
import argparse
from sys import argv

def main():
    parser = argparse.ArgumentParser(prog='HLIMWL',
                                     description='How Long Is My Watch Later?')
    parser.add_argument('-p', help='playlist to check the length of',
                        metavar='PLAYLIST', default=':ytwatchlater',
                        required=False)
    parser.add_argument('-v', help='verbose mode', action='store_true')
    parser.add_argument('--longest', help='also print the longest video', action='store_true')
    parser.add_argument('-c', '--channel', help='print all videos from this channel', action='store', required=False)
    global args, ytdl # this script is garbage
    args = parser.parse_args()
    ytdl = ytdl_object.makeYtdlObject(args.v)
    if args.channel != None:
        print(f'Printing all videos from channel: {args.channel}')
    printPlaylistDuration(args.p)

def duration(video): # can be playlist also
    obj = {}
    vid = ytdl.extract_info(video, download=False)
    if 'duration' in vid.keys(): # its a single video
        obj['type'] = 'video'
        dur = vid['duration']
    elif 'entries' in vid.keys(): # it's a playlist
        obj['type'] = 'playlist'
        obj['videos'] = len(vid['entries'])
        obj['max_dur'] = 0
        obj['channel_count'] = 0
        obj['channel_dur'] = 0
        dur = 0
        for i in vid['entries']:
            try:
                if args.channel != None and args.channel in [i['channel'], i['channel_id'], i['channel_url']]:
                    print(i['title'])
                    obj['channel_count'] += 1
                    obj['channel_dur'] += i['duration']
                dur += i['duration']
                if i['duration'] > obj['max_dur']:
                    obj['max_dur'] = i['duration']
                    obj['max_title'] = i['title']
            except TypeError:
                # its a private video i guess :P
                pass
            obj['duration'] = dur
    return obj

def formatSeconds(sec):
    return str(timedelta(seconds=sec))

def printPlaylistDuration(playlist):
    obj = duration(playlist)
    length = obj['duration']
    pvideos = obj['videos']
    plength = formatSeconds(length)
    message = f"Your playlist contains {pvideos} videos and is {plength} long."
    if length > 36000: # 10 hours
        message += " Yikes!"
    print(message)
    if (args.longest):
        print(f"The longest video was «{obj['max_title']}» at {formatSeconds(obj['max_dur'])}")
    if (args.channel != None):
        print(f"The {obj['channel_count']} videos from {args.channel} amount to {formatSeconds(obj['channel_dur'])}.")

if __name__ == '__main__':
    main()
