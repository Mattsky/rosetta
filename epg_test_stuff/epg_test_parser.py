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

    def epg_chunker(self):
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
            for q in p.findall('.//icon'):
                print(q.get('src'))