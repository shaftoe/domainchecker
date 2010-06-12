#/usr/bin/env python
"""Script to make the Domain class actually usable.
This is used to check expired domains from every file with given extention
in a given directory 
"""
import os.path
import time
from Domain import Domain

def scanDirectory(directory, extension=""):
    """Fetches files with given extentions from given directory
    Returns a domain list
    Prints out discovered files and statistics
    """
    if not os.path.exists(directory):
        raise OSError, "Directory %s doesn't exist" % directory
    extentionlenght = len(extension)
    # os.path.abspath(directory)
    domainextention = domainzonefiles[-extentionlenght:]
    for domainzonefiles in os.listdir(directory):
        if os.path.isfile(domainzonefiles) and domainextention == zonefileextention:
            domainname = domainzonefiles[:-extentionlenght]
            print "\nFound domain zonefile %s" % domainzonefiles
            d.isExpired(domainname)
            time.sleep(5)
    print "\nDone"
