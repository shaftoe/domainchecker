#/usr/bin/env python
"""Script to make the Domain class actually usable.
This is used to check expired domains from every file with given extention
in a given directory 
"""
import os.path
import time
from Domain import Domain

d = Domain()

def scanDirectory(directory, fileextention=""):
    """Fetches files with given extentions from given directory
    Returns a domain list
    Prints out discovered files and statistics
    """
    if not os.path.exists(directory):
        raise OSError, "Directory %s doesn't exist" % directory
    extentionlenght = len(fileextention) # check extention lenght cause it will be stripped from the filename to get real domain name
    for domainzonefilename in os.listdir(directory):
        domainextention = domainzonefilename[-extentionlenght:]
        counter = 0
        if os.path.isfile(directory + "/" + domainzonefilename) and domainextention == fileextention:
            domainname = domainzonefilename[:-extentionlenght]
            print "\nFound domain zonefile %s" % domainzonefilename
            if d.isExpired(domainname):
                print "Domain %s is expired!" % domainname
            time.sleep(5)
    print "\nDone"
