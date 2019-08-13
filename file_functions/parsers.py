import os
import sys
import re
from xml.etree import ElementTree as ET
from PySide2 import QtWidgets, QtGui, QtCore
from collections import OrderedDict

class M3U_Parser():
    """Class to hold m3u info in memory."""

    def __init__(self):
        self.channel_list = {}


    def m3u_chunker(self, m3udata):
        
        # Get rid of #EXTM3U line in returned data
        formatted_m3u = m3udata.splitlines()[1:]

        for index in range(0, len(formatted_m3u)):
            if "#EXTINF" in formatted_m3u[index]:
                line = formatted_m3u[index]
                uri_line = formatted_m3u[index+1]
                # Extract group title from returned result
                group_title = re.search('group-title="(.+?)"', line).group(1)
                # Get the channel name as well
                channel_name = re.search('tvg-name="(.+?)"', line).group(1)
                #print(group_title)
                
                if group_title not in self.channel_list:
                    self.channel_list[group_title] = {}
                self.channel_list[group_title][channel_name] = uri_line



class EPG_Parser():
    """Class to hold EPG XML info in memory."""

    def __init__(self, master=None):
        self.category_list = {}
        self.channel_list = {}
        self.programme_dict = {}
        #QtWidgets.QMainWindow.__init__(self, master)
        self.tree = ET.parse('/home/matt/Documents/xmltv.xml')
        self.root = self.tree.getroot()
        self.listWidgets = {}
        self.categories = {'test1' : {}, 'test2' : {}, 'test3' : {}}
        #self.playlists = QtWidgets.QTabWidget(self.dock)
        self.playlists = QtWidgets.QTabWidget()
        self.categorytabs = QtWidgets.QTabBar(self.playlists)

    # NOT REQUIRED - here for debug and testing
    def m3u_chunker(self):
        
        m3u_file = open(os.path.expanduser('~/Documents/iptv.m3u'), 'r')
        m3udata = m3u_file.read()
        m3u_file.close()
        

        # Get rid of #EXTM3U line in returned data
        formatted_m3u = m3udata.splitlines()[1:]

        for index in range(0, len(formatted_m3u)):
            if "#EXTINF" in formatted_m3u[index]:
                line = formatted_m3u[index]
                
                uri_line = formatted_m3u[index+1]
                #print(uri_line)
                # Extract group title from returned result
                group_title = re.search('group-title="(.+?)"', line).group(1)
                # Get the channel name as well
                channel_name = re.search('tvg-name="(.+?)"', line).group(1)
                #print(group_title)
                
                if group_title not in self.category_list:
                    self.category_list[group_title] = {}
                self.category_list[group_title][channel_name] = uri_line

        #for key in self.channel_list.keys():
            #print(key)

        #print(self.category_list['CANADA'])

    def epg_channel_chunker(self):
        #tree = ET.parse(xmldata)
        #print(self.root)
        for p in self.root.findall('.//channel'):
            #print(p)
            #for elem in p.iter():
                #print(elem.tag)
            #print(p.tag)
            #print(p.attrib)
            #<channel id="3352.stations.xmltv.tvmedia.ca">
            #<display-name>FOX COLLEGE ATLANTIC Local</display-name>
            #<icon src="http://ik.imagekit.io/ulangotv/image/upload/3783575_logo_fox_college_sports_atlantic.png" />
            #</channel>
            # display-name is unique - use for Channel list
            # channel id is common to both channels and programmes (can find 'cartoonnetwork.us' in both, use for creating datasets)
            channel_display_name = p.find('display-name').text
            #print("%s" % (channel_display_name))
            channel_id = p.get('id')

            # THIS WORKS
            #try: 
            #    print(p.find('.//icon').get('src'))
            #except:
            #    pass
            
            if channel_display_name not in self.channel_list:
                # Formatted as:
                # 'BET HER | VIP': {'channel_id': 'BET Her US'}
                self.channel_list[channel_id] = {}
                self.channel_list[channel_id]['channel_display_name'] = channel_display_name
                self.channel_list[channel_id]['programme_list'] = {}
                try:
                    self.channel_list[channel_id]['logo'] = p.find('.//icon').get('src')
                except:
                    self.channel_list[channel_id]['logo'] = "None"

            #print(self.channel_list)

    def epg_programme_chunker(self):

        # Generate programme info lists
        for p in self.root.findall('.//programme'):
            #<programme start="20190729043000 -0400" stop="20190729044500 -0400" channel="cartoonnetwork.us" >
            # <title>Lazor Wulf</title>
            # <desc>Lazor Wulf decides he is just going to starve to death when his favorite food place gets wrecked. Stupid Horse tries to recreate the menu because he&apos;s good like that.</desc>
            # </programme>
            #programme
            #title
            #desc
            #programme
            #print(p)
            ## <Element 'programme' at 0x7f554c6b8688>
            #print(p.attrib)
            ## {'start': '20190729210000 -0400', 'stop': '20190729220000 -0400', 'channel': 'TeenNick US'}
            #print(p.get('start').strip('-0400'))
            ## 20190728220000
            #print(p.get('stop').strip('-0400'))
            ## 20190729220000
            #print(p.find('.//title').text)
            ## Teen Wolf
            #print(p.find('.//desc').text)
            ## A young outsider wanders into the woods in search of dead body and encounters a beast. After fighting for his life and escaping a deep bite, Scott's wound changes his life forever(n)
            #print(p.get('channel'))
            ## TeenNick US
            channel_id = p.get('channel')
            

            #if channel_id not in self.programme_dict:
                # 'TeenNick US': 'TeenNick US'
                #self.programme_dict[channel_id] = channel_id

            start_time = int(p.get('start').strip('-0400').strip(' '))
            #print(type(start_time))

            if channel_id not in self.channel_list:
                self.channel_list[channel_id] = channel_id
            
            #if start_time not in self.programme_dict[channel_id] list of keys:
            #    self.programme_dict['channel'] = channel_id

            # Proposed solution:
            # self.programme_dict[channel_id][start_time]['title'] = p.find('.//title').text
            # self.programme_dict[channel_id][start_time]['desc'] = p.find('.//desc').text
            # Integrated with existing channel list?
            # self.channel_list[channel_id][start_time] = start_time
            # if start_time not in self.channel_list[channel_id][start_time] list of keys:
            if start_time not in self.channel_list[channel_id]['programme_list'] :
                self.channel_list[channel_id]['programme_list'][start_time] = {}

            self.channel_list[channel_id]['programme_list'][start_time]['title'] = p.find('.//title').text
            self.channel_list[channel_id]['programme_list'][start_time]['desc'] = p.find('.//desc').text

            # Sort it by times
            # THIS WORKS FOR ONE CHANNEL
            # testparser.channel_list['wapatv.us']['programme_list'] = OrderedDict(sorted(testparser.channel_list['wapatv.us']['programme_list'].items()))
            self.channel_list[channel_id]['programme_list'] = OrderedDict(sorted(self.channel_list[channel_id]['programme_list'].items()))
            
            
            # print(sorted(testparser.channel_list['wapatv.us']['programme_list'].items()))

            #for x in testparser.channel_list['wapatv.us']['programme_list']:
            #    print("start time: {0} - info:{1}".format(x, testparser.channel_list['wapatv.us']['programme_list'][x]))