#/usr/bin/env python
"""Script to make the Domain class actually usable.
This is used to check expired domains from every file with given extention
in a given directory 
"""
import os.path
import time
from Domain import Domain

d = Domain()

def scanDirectory(directory, fileextension=""):
    """Fetches files with given extentions from given directory
    Returns a domain list
    Prints out discovered files and statistics
    """
    checkArgumentsValidity(directory,fileextension)
    extentionlenght = len(fileextension) # check extention lenght cause it will be stripped from the filename to get real domain name
    for domainzonefilename in os.listdir(directory):
        domainextension = os.path.splitext(domainzonefilename)[1]
        #counter = 0 TODO...
        #check if files are not directories instead, and if they match fileextension too
        if os.path.isfile(os.path.join(directory,domainzonefilename)) and domainextension == fileextension:
            if extentionlenght != 0:
                domainname = domainzonefilename[:-extentionlenght]
            else:
                domainname = domainzonefilename
            print "\nFound domain zonefile %s\nProcessing %s..." % (domainzonefilename,domainname)
            if d.isExpired(domainname):
                print "Domain %s is expired!" % domainname
            time.sleep(5)
    print "\nDone"

def checkArgumentsValidity(directory,fileextension):
    if not os.path.exists(directory):
       raise OSError, "Directory %s doesn't exist" % directory
    if len(fileextension) == 1:
        raise TypeError, "Extension %s is not valid" % fileextension
    if len(fileextension) != 0 and fileextension[0:1] != "." :
            raise TypeError, "Extension %s is not valid. Needs to start with a dot." % fileextension
