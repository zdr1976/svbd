# svbd
`svbd` is small python script acting as a Safari video book downloader.
If you have Safari Books online subscription, you can use this script to save videos
to your disk to watch them later offline or on bigger screen.

The actual download is executed by [youtube-dl](https://ytdl-org.github.io/youtube-dl/)
which need to be installed before.
```
curl -L https://yt-dl.org/downloads/latest/youtube-dl -o ~/bin/youtube-dl
```

### Options
* `-u`, `--url` - URL of Video book to download. *[Mandatory]*
* `-l`, `--login` - Your Safari Book account. *[Mandatory]*
* `-p`, `--password` - Don't type password! You will be prompted for. *[Mandatory]*
* `-d`, `--dir`- Location where book will bo downloaded. *[Optional]*

If you don't specidied with `-d`, `--dir` option defaul location will be
`Videos/SafariBooks` under your home directory.

### Example
```
./svbd.py -u https://learning.oreilly.com/videos/python-for-beginners/9781838552787 -l my@email.com -p
```
