import os
import sys
import re
from xml.etree import ElementTree as ET

class EPG_Parser():
    """Class to hold EPG XML info in memory."""

    def __init__(self):
        self.channel_list = {}
        self.tree = ET.parse('xmltv.xml')
        self.root = self.tree.getroot()

    def epg_channel_chunker(self):
        #tree = ET.parse(xmldata)
        print(self.root)
        for p in self.root.findall('.//channel'):
            print(p)
            for elem in p.iter():
                print(elem.tag)
            print(p.tag)
            print(p.attrib)
            #<channel id="3352.stations.xmltv.tvmedia.ca">
            #<display-name>FOX COLLEGE ATLANTIC Local</display-name>
            #<icon src="http://ik.imagekit.io/ulangotv/image/upload/3783575_logo_fox_college_sports_atlantic.png" />
            #</channel>
            print("%s" % (p.find('display-name').text))
            print(p.get('id'))
            #for q in p.findall('.//icon'):
                #print(q.get('src'))
            try: 
                print(p.find('.//icon').get('src'))
            except:
                pass


    def epg_programme_chunker(self):

        for p in self.root.findall('.//programme'):
            #<programme start="20190729043000 -0400" stop="20190729044500 -0400" channel="cartoonnetwork.us" >
            # <title>Lazor Wulf</title>
            # <desc>Lazor Wulf decides he is just going to starve to death when his favorite food place gets wrecked. Stupid Horse tries to recreate the menu because he&apos;s good like that.</desc>
            # </programme>
            #programme
            #title
            #desc
            #programme
            print(p)
            #for elem in p.iter():
            #    print(elem.tag)
            #print(p.tag)
            print(p.attrib)
            print(p.find('.//title').text)
            print(p.find('.//desc').text)
            