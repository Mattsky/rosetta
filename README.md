# Rosetta

Rosetta is a Python 3 project used for playing streaming video.

## Features!

  - Load an M3U file from disk
  - Import M3U data from a URI (and then save it to disk)
  - Categorisation of streams into tabs in a playlist
  - VLC integration for quality viewing

### Tech

Rosetta uses a number of open source projects to work properly:

* [VLC] - The most immense video player you ever did see
* [PySide2] - QT5 bindings for Python, for the fancy UI stuff
* [Whichcraft] - Handy library for checking stuff's installed and available

And of course Rosetta itself is open source.

### Installation

The dependencies are specified in the project setup.py; all you need is Python 3. Clone the project, change to the directory, and run pip install in dev mode:

```sh
pip3 install -e .
```

### Usage

Once installed, just invoke it from the command line:

```sh
rosetta
```

You can either load an M3U file from disk, or paste the URI given to you and it'll be imported (and then saved to disk at ~/Documents/iptv.m3u)

### Development

Want to contribute? Great! Hack away and submit a PR.

### Todos

 - Write tests
 - Fix the damn fullscreen video border
 - EPG support?
 - God knows

License
----

MIT

[//]: # (These are reference links used in the body of this note and get stripped out when the markdown processor does its job. There is no need to format nicely because it shouldn't be seen. Thanks SO - http://stackoverflow.com/questions/4823468/store-comments-in-markdown-syntax)


   [VLC]: <https://www.videolan.org/vlc/index.html>
   [PySide2]: <https://pypi.org/project/PySide2/>
   [Whichcraft]: <https://pypi.org/project/whichcraft/>
