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
    物件 = {} # it means object
    vid = ytdl.extract_info(video, download=False)
    if 'duration' in vid.keys(): # its a single video
        物件['type'] = 'video'
        dur = vid['duration']
    elif 'entries' in vid.keys(): # it's a playlist
        物件['type'] = 'playlist'
        物件['videos'] = len(vid['entries'])
        物件['max_dur'] = 0
        物件['channel_count'] = 0
        物件['channel_dur'] = 0
        dur = 0
        for i in vid['entries']:
            try:
                if args.channel != None and args.channel in [i['channel'], i['channel_id'], i['channel_url']]:
                    print(i['title'])
                    物件['channel_count'] += 1
                    物件['channel_dur'] += i['duration']
                dur += i['duration']
                if i['duration'] > 物件['max_dur']:
                    物件['max_dur'] = i['duration']
                    物件['max_title'] = i['title']
            except TypeError:
                # its a private video i guess :P
                pass
            物件['duration'] = dur
    return 物件

def formatSeconds(sec):
    return str(timedelta(seconds=sec))

def printPlaylistDuration(playlist):
    pl = duration(playlist)
    length = pl['duration']
    pvideos = pl['videos']
    plength = formatSeconds(length)
    message = f"Your playlist contains {pvideos} videos and is {plength} long."
    if length > 36000: # 10 hours
        message += " Yikes!"
    print(message)
    if (args.longest):
        print(f"The longest video was «{pl['max_title']}» at {formatSeconds(pl['max_dur'])}")
    if (args.channel != None):
        print(f"The {pl['channel_count']} videos from {args.channel} amount to {formatSeconds(pl['channel_dur'])}.")

if __name__ == '__main__':
    main()
