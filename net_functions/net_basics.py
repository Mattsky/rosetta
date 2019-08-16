import requests
import os
from pathlib import Path

def m3u_prep(m3u_uri):
    """Download m3u and write to file."""
    print(m3u_uri)
    r = requests.get('{0}'.format(m3u_uri[0]))
    # DEBUG GOODNESS!
    #print(r.status_code)
    #print(r.headers)
    #print(r.encoding)
    #print(r.text)

    # Write this stuff to file to save constantly hitting the URI
    # Change to custom directory
    #m3u_file = open(os.path.expanduser('~/rosetta/iptv.m3u'), 'w')
    m3u_file = open(Path.home().joinpath('rosetta', 'iptv.m3u'), 'w')
    m3u_file.write(r.text)
    m3u_file.close()
    return(r.text)

def xml_prep(xml_uri):
    """Download xml and write to file."""
    # NOT FUNCTIONAL YET. I mean, it'll work, but we're not using it. Yet.
    r = requests.get('{0}'.format(xml_uri[0]))
    #print(r.status_code)
    #print(r.headers)
    #print(r.encoding)
    #print(r.text)

    # Change to custom directory
    #filepath = os.path.expanduser('~/rosetta/xmltv.xml')
    filepath = Path.home().joinpath('rosetta', 'xmltv.tv')
    xml_file = open(filepath, 'w')
    xml_file.write(r.text)
    xml_file.close()
    return(filepath)