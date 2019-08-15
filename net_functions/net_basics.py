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

def xml_prep(xml_uri):
    """Download xml and write to file."""
    # NOT FUNCTIONAL YET. I mean, it'll work, but we're not using it. Yet.
    r = requests.get('{0}'.format(xml_uri[0]))
    print(r.status_code)
    print(r.headers)
    print(r.encoding)
    #print(r.text)

    filepath = os.path.expanduser('~/Documents/xmltv.xml')
    xml_file = open(filepath, 'w')
    xml_file.write(r.text)
    xml_file.close()
    return(filepath)