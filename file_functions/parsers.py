import os
import sys
import re

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
