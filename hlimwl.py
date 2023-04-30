from datetime import timedelta
from ytdl_object import ytdl

print("Please wait...")

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
