import requests
import os

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
    m3u_file = open(os.path.expanduser('~/Documents/iptv.m3u'), 'w')
    m3u_file.write(r.text)
    m3u_file.close()
    return(r.text)

def xml_prep(epg_uri):
    """Download xml and write to file."""
    # NOT FUNCTIONAL YET. I mean, it'll work, but we're not using it. Yet.
    r = requests.get('{0}'.format(epg_uri[0]))
    print(r.status_code)
    print(r.headers)
    print(r.encoding)
    #print(r.text)

    #file = open(os.getcwd() + "/xmltv.xml", "w+")
    #file.write(r.text)
    #file.close()
    return(r.text)