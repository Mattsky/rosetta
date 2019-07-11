import os
from whichcraft import which

def vlc_check():
    vlc_location = which('vlc')
    if vlc_location == None:
        raise(Exception("CRITICAL: VLC not found. Please install it and try again."))
    else:
        print("VLC found at {0} - OK!".format(vlc_location))
        return