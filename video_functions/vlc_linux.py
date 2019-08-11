import platform
import os
import sys
from whichcraft import which
from file_functions.parsers import M3U_Parser, EPG_Parser
from net_functions.net_basics import m3u_prep, xml_prep
from PySide2 import QtWidgets, QtGui, QtCore
import vlc

class PlayerNG(QtWidgets.QMainWindow):

    def closeEvent(self, event):
        self.mediaplayer.stop()


#class Player(QtWidgets.QMainWindow):
class Player(PlayerNG):

    def __init__(self, master=None):
        self.syscheck()
        QtWidgets.QMainWindow.__init__(self, master)
        self.appInfo = "Rosetta v0.3.1"     
        self.setWindowTitle(self.appInfo)
        self.m3uUri = None
        self.m3udata = None
        self.m3uParser = M3U_Parser()
        # Channel / Playlist dock
        self.dock = None
        # EPG dock
        self.epgdock = None

        # Create a basic vlc instance
        self.instance = vlc.Instance()

        self.media = None

        # Create an empty vlc media player
        self.mediaplayer = self.instance.media_player_new()

        self.create_ui()

        self.is_paused = False

    def syscheck(self):

        # Check VLC's installed. Kinda need it to do, well, anything.
        vlc_location = which('vlc')
        if vlc_location == None:
            warningBox = QtWidgets.QMessageBox()
            warningBox.setWindowTitle("CRITICAL: VLC not installed!")
            warningBox.setText("VLC is required for this to work. Please install it and retry.")
            warningBox.exec()
            sys.exit(1)

    def set_video_stream(self, selected_item):
        ## DEBUG
        ## Get name of tab based on tab index
        #print(self.playlists.currentIndex())
        #print(self.playlists.tabText(self.playlists.currentIndex()))
        #print(self.playlists.currentWidget())
        ## The text from the widget window that got chosen
        #print(selected_item.text())

        ## Set vars for lookup ops
        currentCategory = self.playlists.tabText(self.playlists.currentIndex())
        currentChannel = selected_item.text()
        # Now we can do a k/v check and pull the URI to set!
        # Spits out the stream URI from the m3u dict
        #print(self.m3udict[currentCategory][currentChannel])

        # Assign the MRL
        videoStreamUri = self.m3udict[currentCategory][currentChannel]
        # Set the MRL
        self.media = self.mediaplayer.set_mrl(videoStreamUri)
        # Set the Player instance's media - the MRL
        self.mediaplayer.set_media(self.media)
        # Play the media in the instance window, otherwise we get a popout
        self.mediaplayer.set_xwindow(int(self.videoframe.winId()))
        # Update the main window title
        self.setWindowTitle("{0} - {1}".format(self.appInfo, currentChannel))
        self.mediaplayer.play()

    def mouseDoubleClickEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            if self.windowState() == QtGui.Qt.WindowNoState:
                # There has to be a better way to just fullscreen the video player. >:(
                self.widget.setStyleSheet("background-color:black")
                self.dock.hide()
                self.volumeslider.hide()
                self.playbutton.hide()
                self.stopbutton.hide()
                self.menu_bar.hide()
                self.videoframe.showFullScreen()
                self.setWindowState(QtGui.Qt.WindowFullScreen)
            else:
                self.widget.setStyleSheet("background-color:None")
                self.dock.show()
                self.volumeslider.show()
                self.playbutton.show()
                self.stopbutton.show()
                self.menu_bar.show()
                self.videoframe.showNormal()
                self.setWindowState(QtGui.Qt.WindowNoState)

    def onTabChange(self, i):
        ##print("TAB IS NOW: {0}".format(i))
        self.playlists.setCurrentIndex(i)

        ##print("CURRENT INDEX IS: {0}".format(self.playlists.currentIndex()))
        
        key = self.playlists.tabText(self.playlists.currentIndex())
        ##print(key)
        ##print(self.listWidgets[key])

        self.playlists.setCurrentWidget(self.listWidgets[key])
        
        ##print(self.playlists.currentWidget())
        self.playlists.currentWidget().itemDoubleClicked.connect(self.set_video_stream)

    def create_playlist_ui(self, m3udict):
        
        self.listWidgets = {}

        if self.dock != None:
            self.dock.deleteLater()
        
        # Create DockWidget with Tabs for categories
        self.dock = QtWidgets.QDockWidget("Categories", self)
        self.dock.setAllowedAreas(QtCore.Qt.RightDockWidgetArea)
        # Disable close button (X)
        self.dock.setFeatures(QtWidgets.QDockWidget.DockWidgetFloatable | QtWidgets.QDockWidget.DockWidgetMovable)
        self.m3udict = m3udict
        self.playlists = QtWidgets.QTabWidget(self.dock)

        # Progress indentation ends here

        # Create ListWidgets here based on keys from m3u data

        if self.m3udict != None :
            for key in self.m3udict.keys():
                #print(key)
                self.listWidgets[key] = QtWidgets.QListWidget()
                for key2 in self.m3udict[key].keys():
                    self.listWidgets[key].addItem(key2)


            # Then create the tab in the DockWidget
            for key in self.listWidgets.keys():
                self.playlists.addTab(self.listWidgets[key], "{0}".format(key))

            self.dock.setWidget(self.playlists)
            
            self.addDockWidget(QtCore.Qt.RightDockWidgetArea, self.dock)

            # Start it undetached
            self.dock.setFloating(False)
                
            ### Set up connections
            # Pick up tab change in playlists widget
            self.playlists.currentChanged.connect(self.onTabChange)
            

            self.playlist_view_action.setCheckable(True)
            self.playlist_view_action.setChecked(True)
            
            # Is this interfering with the video player maximise on doubleclick?
            self.playlists.currentWidget().itemDoubleClicked.connect(self.set_video_stream)

    def create_epg_ui(self):

        if not self.m3uParser.channel_list:
            print("CHANNEL DATA DOES NOT EXIST YET!")
            return

        self.epgListWidgets = {}
        if self.epgdock != None:
            self.epgdock.deleteLater()

        self.epgdock = QtWidgets.QDockWidget("Categories", self)

        self.epgplaylists = QtWidgets.QTabWidget(self.dock)


    def create_ui(self):
        """Set up the user interface, signals & slots
        """
        self.widget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.widget)
        
        # In this widget, the video will be drawn
        self.videoframe = QtWidgets.QFrame()
        self.videoframe.setFrameShape(QtWidgets.QFrame.NoFrame)

        self.palette = self.videoframe.palette()
        self.palette.setColor(QtGui.QPalette.Window, QtGui.QColor(0, 0, 0))
        self.videoframe.setPalette(self.palette)
        self.videoframe.setAutoFillBackground(False)

        # Set up play button
        self.hbuttonbox = QtWidgets.QHBoxLayout()
        self.playbutton = QtWidgets.QPushButton("Play")
        self.hbuttonbox.addWidget(self.playbutton)
        self.playbutton.clicked.connect(self.play)

        # Set up stop button
        self.stopbutton = QtWidgets.QPushButton("Stop")
        self.hbuttonbox.addWidget(self.stopbutton)
        self.stopbutton.clicked.connect(self.stop)

        self.hbuttonbox.addStretch(1)

        # Set up volume slider
        self.volumeslider = QtWidgets.QSlider(QtCore.Qt.Horizontal, self)
        self.volumeslider.setMaximum(100)
        self.volumeslider.setValue(80)
        self.volumeslider.setToolTip("Volume")
        self.hbuttonbox.addWidget(self.volumeslider)
        self.volumeslider.valueChanged.connect(self.set_volume)

        self.vboxlayout = QtWidgets.QVBoxLayout()
        self.vboxlayout.addWidget(self.videoframe)
        self.vboxlayout.addLayout(self.hbuttonbox)

        self.widget.setLayout(self.vboxlayout)

        self.menu_bar = self.menuBar()

        # Build menus
        self.file_menu = self.menu_bar.addMenu("File")

        # Add actions to file menu
        open_action = QtWidgets.QAction("Open M3U File", self)
        m3u_action = QtWidgets.QAction("Open M3U URI", self)
        close_action = QtWidgets.QAction("Close App", self)
        self.file_menu.addAction(open_action)
        self.file_menu.addAction(m3u_action)
        self.file_menu.addAction(close_action)

        open_action.triggered.connect(self.open_file)
        # Activate prefs stuff when the method's ready
        m3u_action.triggered.connect(self.get_m3u)
        close_action.triggered.connect(sys.exit)

        # Add action(s) to view menu - TODO
        self.view_menu = self.menu_bar.addMenu("View")

        self.playlist_view_action = QtWidgets.QAction("View Playlist", self)
        self.epg_view_action = QtWidgets.QAction("View EPG", self)

        self.view_menu.addAction(self.playlist_view_action)
        self.view_menu.addAction(self.epg_view_action)

        self.playlist_view_action.triggered.connect(self.view_playlist)
        self.epg_view_action.triggered.connect(self.view_epg)

        self.timer = QtCore.QTimer(self)
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.update_ui)

    def play(self):
        """Play selected stream"""

        self.mediaplayer.play()
        self.timer.start()

    def stop(self):
        """Stop player
        """
        self.mediaplayer.stop()
        self.playbutton.setText("Play")

    def get_m3u(self):
        """Quick function to get a M3U URI from the user"""

        m3u_uri = QtWidgets.QInputDialog.getText(self, "M3U Loader","Link to your M3U:", QtWidgets.QLineEdit.Normal, "")
        if not m3u_uri:
            return
        else:
            self.m3uUri = m3u_uri
            # Progress bar to let folks know it hasn't locked up.
            #self.m3uProgress.setWindowTitle("Processing M3U data, please wait!")
            
            self.m3udata = m3u_prep(m3u_uri)

            self.m3uParser.m3u_chunker(self.m3udata)

            self.create_playlist_ui(self.m3uParser.channel_list)

     

    def open_file(self):
        """Open a local M3U file for processing"""

        dialog_txt = "Choose M3U File"
        filename = QtWidgets.QFileDialog.getOpenFileName(self, dialog_txt, os.path.expanduser('~'))
        if not filename:
            return

        # getOpenFileName returns a tuple, so use only the actual file name
        with open(filename[0], 'r') as m3udata_file:
            self.m3udata = m3udata_file.read()
            
        self.m3uParser.m3u_chunker(self.m3udata)

        self.create_playlist_ui(self.m3uParser.channel_list)

    def view_playlist(self):

        # If the menu's already been generated:
        if self.dock :

            if self.dock.isHidden():
                self.dock.show()
                self.playlist_view_action.setChecked(True)
            else:
                self.dock.hide()
                self.playlist_view_action.setChecked(False)

    def view_epg(self):

        if self.dock :
        # If channel list exists, then create the EPG panel data
            epg_parser = EPG_Parser()
            # Debug - provide the channel info
            epg_parser.m3u_chunker()
            epg_parser.epg_channel_chunker()
            epg_parser.epg_programme_chunker()
            #epg_parser.create_playlist_ui()

            # Then create the panel
            for key in epg_parser.channel_list.keys():
                # Build counter to figure out number of rows to create
                count = 0
                for item in epg_parser.channel_list[key]['programme_list'].items():
                    #print(item)
                    count += 1
                if count > 0:
                    epg_parser.listWidgets[key] = QtWidgets.QTableWidget(count, 3)
                    epg_parser.listWidgets[key].setHorizontalHeaderLabels(["Date / Time", "Title", "Description"])
                #print(count)
                
                
                # Only generate the page if actual data was found - count will be greater than zero
                if count > 0:
                    row = 0
                    for item in epg_parser.channel_list[key]['programme_list'].items():
                        # self.channel_list[channel_id]['programme_list'][start_time]['title']
                        # self.channel_list[channel_id]['programme_list'][start_time]['desc']
                        # Extract timestamp, e.g. 20190727230000
                        timestamp = str(item[0])
                        epg_parser.listWidgets[key].setItem(row, 0, QtWidgets.QTableWidgetItem(timestamp))
                        epg_parser.listWidgets[key].setItem(row, 1, QtWidgets.QTableWidgetItem(str(item[1]['title'])))
                        epg_parser.listWidgets[key].setItem(row, 2, QtWidgets.QTableWidgetItem(str(item[1]['desc'])))
                        # self.listWidgets[key].addItem(str(item))
                        row += 1
                    # Resize tables to match content size
                    epg_parser.listWidgets[key].resizeColumnsToContents()
                    # Make it all read only
                    epg_parser.listWidgets[key].setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
                

            
            ### OLD CODE THAT WORKS FOR CHANNEL GEN
            # Then create the tab in the DockWidget
            #for key in self.listWidgets.keys():
                # Tabs = channel_ids
                #self.playlists.addTab(self.listWidgets[key], "{0}".format(key))

            ## NEW CODE THAT USES CATEGORIES MASTER TABS
            for tab in epg_parser.category_list.keys():
                # TAB will equal the cat - e.g. KIDS, CANADA, INDIAN
                epg_parser.categories[tab] = QtWidgets.QTabWidget(self.dock)
                epg_parser.playlists.addTab(epg_parser.categories[tab], "{0}".format(tab))
                for subtab in epg_parser.listWidgets.keys():
                    # subtab is the channel ID, e.g. spike.ca, space.ca, tlc.ca
                    if epg_parser.channel_list[subtab]['channel_display_name'] in epg_parser.category_list[tab]: 
                        epg_parser.categories[tab].addTab(epg_parser.listWidgets[subtab], "{0}".format(subtab))
                    
            # DEBUG
            self.epgdock = QtWidgets.QDockWidget("Categories", self)

            # NOT DEBUG
            self.epgdock.setWidget(epg_parser.playlists)
            
            self.addDockWidget(QtCore.Qt.RightDockWidgetArea, self.epgdock)

            # Start it undetached
            self.epgdock.setFloating(False)

        # else create a dialogue box saying EPG can't be created before channel data
        else:
            print("No channel data! Skipping EPG.")
            return


    def set_volume(self, volume):
        """Set the volume
        """
        self.mediaplayer.audio_set_volume(volume)

    def update_ui(self):
        """Updates the user interface"""

        # Set the slider's position to its corresponding media position
        # Note that the setValue function only takes values of type int,
        # so we must first convert the corresponding media position.
        #media_pos = int(self.mediaplayer.get_position() * 1000)
        #self.positionslider.setValue(media_pos)

        # No need to call this function if nothing is played
        if not self.mediaplayer.is_playing():
            self.timer.stop()

            # After the video finished, the play button stills shows "Pause",
            # which is not the desired behavior of a media player.
            # This fixes that "bug".
            if not self.is_paused:
                self.stop()