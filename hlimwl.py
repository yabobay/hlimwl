from yt_dlp import YoutubeDL
from datetime import timedelta

# try and find cookies from *some* browser so we can use them for
# authentication. also make a YoutubeDL object whatever
browsers = 'firefox', 'brave', 'opera', 'vivaldi', 'safari', 'edge', 'chromium', 'chrome'
for browser in browsers:
    word = (browser, )
    if browser == 'firefox':
        # this is unreliable & BS but it "works"
        import os
        from re import search
        # TODO: read some firefox config and get the profile name that
        # way instead
        profileName = [
            x for x in
            os.listdir(os.path.expanduser('~/.mozilla/firefox/'))
            if search('default-release', x)
        ] [0]
        word += (profileName, None, 'none')
    try:
        ytdl = YoutubeDL ({
            'quiet': True,
            'no_warnings': True,
            'extract_flat': 'in_playlist',
            'cookiesfrombrowser': word
        })
        break
    except FileNotFoundError:
        exit()
        pass

def prettyTime(secs):
    return str(timedelta(seconds=secs))

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

def prettyDuration(video): # can be playlist also
    return prettyTime(duration(video))

print("Please wait...")

print(
    "Your Watch Later playlist is",
    prettyDuration(':ytwatchlater'),
    "long."
)
