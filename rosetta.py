#!/usr/bin/env python

import os
import re
import sys
from net_functions.net_basics import m3u_prep, xml_prep
from video_functions.vlc_linux import Player
from file_functions.parsers import M3U_Parser
from PySide2 import QtWidgets, QtGui, QtCore
import vlc

userName = os.environ['ROSETTA_USER']
passWord = os.environ['ROSETTA_PASS']

def main():
    #print("DEBUG: M3U download")
    #m3u_data = m3u_prep(userName, passWord)
    #xml_prep(userName, passWord)

    #print("DEBUG: Parsing M3U data")
    #m3uparser = M3U_Parser()
    #m3uparser.m3u_chunker(m3u_data)

    app = QtWidgets.QApplication(sys.argv)
    player = Player()

    player.show()
    player.resize(1200, 600)

    sys.exit(app.exec_())
    

if __name__ == "__main__":
    main()