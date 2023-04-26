from yt_dlp import YoutubeDL
from datetime import timedelta

print("Please wait...")

# try and find cookies from *some* browser so we can use them for
# authentication. also make a YoutubeDL object whatever
browsers = 'firefox', 'brave', 'opera', 'vivaldi', 'safari', 'edge', 'chromium', 'chrome'
for browser in browsers:
    browserTuple = (browser, )
    if browser == 'firefox':
        # this is unreliable & BS but it "works"
        import os
        from re import search
        # TODO: read some firefox config and get the profile name that
        # way instead
        try:
            profileName = [
                x for x in
                os.listdir(os.path.expanduser('~/.mozilla/firefox/'))
                if search('default-release', x)
            ] [0]
            browserTuple += (profileName, None, 'none')
        except FileNotFoundError:
            # happens when we don't have firefox. TODO: account for
            # windows and flatpak.
            continue
    elif browser == 'safari':
        from sys import platform
        if platform != "darwin":
            continue
    try:
        ytdl = YoutubeDL ({
            'quiet': True,
            'no_warnings': True,
            'extract_flat': 'in_playlist',
            'cookiesfrombrowser': browserTuple
        })
        break
    except FileNotFoundError:
        pass

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

try:
    length = duration(':ytwatchlater')
    plength = str(timedelta(seconds=length))
    message = f"Your Watch Later playlist is {plength} long."
    if length > 36000: # 10 hours
        message += " Yikes!"
    print(message)
except NameError:
    print("No browser found :(",
          "You need to login to YouTube in some web browser.",
          sep="\n")
