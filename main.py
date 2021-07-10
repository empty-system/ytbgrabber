# -*- coding: utf-8 -*-

import argparse
import os
from datetime import date
import urllib.request
import re
import requests
from pathlib import Path
import pytube
import random

today = date.today()
date_file = today.strftime('%b-%d-%Y')
path = os.getcwd() + '/' + date_file
if not os.path.exists(date_file):
    os.makedirs(path)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('url', help='should be "https://www.youtube.com/xxx"')
    parser.add_argument('-t', help='get the thumbnail', action='store_true')
    parser.add_argument('-m', help='get the mp3', action='store_true')
    parser.add_argument('-a', help='get mp3 + thumbnail', action='store_true')
    options = parser.parse_args()

    try:
        go(options.url, options.t, options.m, options.a)
        current_path = Path(os.getcwd()).joinpath('ytbgrabber', date_file)
        print(f"Files are at {current_path}")
    except AttributeError:
        print("Requires at least one positional argument, see ytbgrabber -h")


def go(url, oT, oM, oA):
    r = urllib.request.urlopen(url)
    html = r.read().decode('utf8')

    if oT:
        img(url, html)

    elif oM:
        song(url)

    elif oA:
        img(url, html)
        song(url)


def img(url, html):
    img_url = re.search("(?P<url>https?://i.ytimg.com/vi/[\w]+/maxresdefault.jpg)", html).group("url")

    img = requests.get(img_url)

    f = open(date_file + '/' + random_name() + '.jpg', 'wb')
    f.write(img.content)
    f.close()


def song(url):
    yt = pytube.YouTube(url)
    mp3 = yt.streams.get_audio_only()
    mp3.download(date_file)

def random_name():
    n = random.randint(1, 99999)
    return str(n)

if __name__ == '__main__':
    main()
