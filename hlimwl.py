import argparse

args = None

def main():
    global args
    from rich.console import Console
    parser = argparse.ArgumentParser(prog='HLIMWL',
                                     description='How Long Is My Watch Later?')
    parser.add_argument('-p', help='playlist to check the length of', metavar='PLAYLIST', default=':ytwatchlater', required=False)
    parser.add_argument('-v', help='verbose mode', action='store_true')
    parser.add_argument('--longest', help='print the longest video', action='store_true')
    parser.add_argument('--average', '--avg', help='print the average length', action='store_true')
    parser.add_argument('-s', '--skip', help="don't count the first N videos", action='store', type=int, default=0)
    parser.add_argument('-c', '--channel', help='print all videos from this channel', action='store', required=False)
    parser.add_argument('-C', '--cookie', help='cookie file you can get from your browser', action='store', required=False) # 🍪🍪🍪
    global args, ytdl, console # this script is garbage
    console = Console(highlight=False)
    args = parser.parse_args()
    ytdl = makeYtdlObject(verbose=args.v, cookie=args.cookie)
    if args.channel != None:
        print(f'Printing all videos from channel: {args.channel}')
    printPlaylistDuration(args.p)

def makeYtdlObject(**kwargs):
    from yt_dlp import YoutubeDL
    import os.path
    verbose = kwargs.pop('verbose', False)
    cookie = kwargs.pop('cookie')
    if cookie == None:
        defaultCookiePath = os.path.join(os.path.dirname(__file__), 'cookies.txt')
        if os.path.isfile(defaultCookiePath):
            cookie = defaultCookiePath
    ytdl_keys = {
        'quiet': not verbose,
        'no_warnings': True,
        'extract_flat': 'in_playlist',
        'cookiefile': cookie
    }
    return YoutubeDL(ytdl_keys)

def duration(video): # can be playlist also
    global args
    obj = {}
    vid = ytdl.extract_info(video, download=False)
    if 'duration' in vid.keys(): # its a single video
        obj['type'] = 'video'
        obj['duration'] = vid['duration']
    elif 'entries' in vid.keys(): # it's a playlist
        obj['type'] = 'playlist'
        obj['videos'] = len(vid['entries'])
        obj['max_dur'] = 0
        obj['channel_count'] = 0
        obj['channel_dur'] = 0
        obj['duration'] = 0
        skipped = 0
        for i in vid['entries']:
            if skipped < args.skip:
                skipped += 1
                continue
            try:
                if args.channel != None and args.channel in [i['channel_id'], i['channel_url'], i['uploader_id']] or caseInsensitiveStringComparison(args.channel, i['channel']):
                    console.print(f"[italic]{i['title']}[/]")
                    obj['channel_count'] += 1
                    obj['channel_dur'] += i['duration']
                obj['duration'] += i['duration']
                if i['duration'] > obj['max_dur']:
                    obj['max_dur'] = i['duration']
                    obj['max_title'] = i['title']
            except TypeError:
                # its a private video i guess :P
                pass
        if obj['videos'] != 0:
            obj['average'] = obj['duration'] / (obj['videos'] - args.skip)
    return obj

def caseInsensitiveStringComparison(a, b):
    try:
        return a.lower() == b.lower()
    except AttributeError:
        return False

def formatSeconds(sec):
    from datetime import timedelta
    from math import floor
    return str(timedelta(seconds=floor(sec)))

def printPlaylistDuration(playlist):
    global args
    obj = duration(playlist)
    length = obj['duration']
    pvideos = obj['videos']
    plength = formatSeconds(length)
    message = f"Your playlist contains {pvideos-args.skip}{f"/{pvideos}" if args.skip > 0 else ''} videos and is {plength} long."
    if args.skip >= pvideos:
        print('Congratulations! You skipped everything!')
        return
    if length > 36000: # 10 hours
        message += " Yikes!"
    print(message)
    if (args.longest and 'max_title' in obj):
        console.print(f"The longest video is [italic]{obj['max_title']}[/] at {formatSeconds(obj['max_dur'])}")
    if (args.average):
        console.print(f"The average length of a video is {formatSeconds(obj['average'])}.")
    if (args.channel != None):
        if obj['channel_count'] > 0:
            console.print(f"The {obj['channel_count']} videos from [italic]{args.channel}[/] amount to {formatSeconds(obj['channel_dur'])}.")
        else:
            console.print(f"There are 0 videos from [italic]{args.channel}[/].")

if __name__ == '__main__':
    main()
