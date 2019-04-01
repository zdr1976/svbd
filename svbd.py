#!/usr/bin/env python3
import requests
import os
import subprocess
import unicodedata
import string
import argparse
import getpass
from bs4 import BeautifulSoup
from pathlib import Path

# Path to 'youtube-dl' binary.
# You can also consider update it by running 'youtube-dl -U'.
DOWNLOADER = 'youtube-dl'
PARRENT_DIR = str(Path.home()) + '/Videos/SafariBooks'


class Password(argparse.Action):
    def __call__(self, parser, namespace, values, option_string):
        if values is None:
            values = getpass.getpass()

        setattr(namespace, self.dest, values)


def correct_name(video_name):
    valid_chars = '-_.() {}{}'.format(string.ascii_letters, string.digits)
    valid_chars = frozenset(valid_chars)
    # Replaces accented characters with the unaccented equivalents.
    cleaned_filename = unicodedata.normalize('NFKD', video_name).encode('ASCII', 'ignore').decode('ASCII')  # noqa
    return ''.join(c for c in cleaned_filename if c in valid_chars)


def main():
    argpars = argparse.ArgumentParser(description='Safari video book downloader.')  # noqa
    argpars.add_argument('-u', '--url', required=True, dest='url',
                         help='URL to download')
    argpars.add_argument('-l', '--login', required=True, dest='login')
    argpars.add_argument('-p', '--password', required=True, action=Password,
                         nargs='?', dest='password',
                         help='Enter your password')
    argpars.add_argument('-d', '--dir', dest='directory',
                         help='Directory to save content')
    args = argpars.parse_args()
    parrent_dir = args.directory if args.directory else PARRENT_DIR

    req = requests.get(args.url)
    bs = BeautifulSoup(req.text, 'html.parser')
    title = bs.find_all('h1')[0].text.strip()
    contents = bs.find_all('li', class_='toc-level-1')
    chapter = 1

    for topic in contents:
        topic_name = topic.a.text
        # Creating folder to put the videos in.
        book_dir = '{}/{}/Chapter{:02d} : {}'.format(parrent_dir, title,
                                                     chapter, topic_name)
        print(book_dir)
        os.makedirs(book_dir, exist_ok=True)

        for index, video in enumerate(topic.ol.find_all('a'), start=1):
            video_name = '{:03d} - {}'.format(index, video.text)
            video_name = correct_name(video_name)
            video_url = video.get('href')
            video_f2s = '{}/{}.mp4'.format(book_dir, video_name)
            # Check if file already exists
            if os.path.isfile(video_f2s):
                print("File {} already exists! Skipping...".format(video_f2s))
                continue
            print("Downloading {} ...".format(video_name))
            subprocess.run([DOWNLOADER, "-u", args.login, "-p", args.password, "--output", video_f2s, video_url])  # noqa
        chapter += 1


if __name__ == '__main__':
    main()
