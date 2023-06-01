from yt_dlp import YoutubeDL

# try and find cookies from *some* browser so we can use them for
# authentication. also make a YoutubeDL object whatever
def makeYtdlObject(verbose=False):
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
                'quiet': not verbose,
                'no_warnings': True,
                'extract_flat': 'in_playlist',
                'cookiesfrombrowser': browserTuple
            })
            return ytdl
            break
        except FileNotFoundError:
            pass
