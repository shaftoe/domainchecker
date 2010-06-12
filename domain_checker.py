#/usr/bin/env python
import subprocess
import os.path
import time

zonefileextention = ".sh"

class Domain:
    """Domain(str "domainname")
    It is meant to give access to whois database in a object-oriented way
    Interface:
    is_expired() - boolean: return yes if domain is EXPIRED
    getkind() - string: tells what kind of domain it is (.com, .org, etc)
    setkind(str "kind") - sets the domain kind
    getdomainname() - str: returns the domain name"""

    __alloweddomains__ = ("com", "info", "it", "org", "net", "biz")

    def checkdomainname(self, domainname):
        """checkdomainname(self, domainname):
        return a boolean, true if domain is syntactically correct
        Unfortunately for now works just with secondLevel domains..."""
        splitteddomain = domainname.split(".")
        if len(splitteddomain) != 2 or splitteddomain[1] not in self.__alloweddomains__:
            return False
        return True

    def whoisresponse(self, domainname):
        """Query the whois database via "whois" command end returns a list
        with lines"""
        try:
            r = subprocess.Popen(['whois', domainname], stdout=subprocess.PIPE)
        except OSError:
            print "Someting wrong... make sure WHOIS is installed and in $PATH"
            quit()
        return r.stdout.readlines()


    def is_expired(self, domainname=""):
        """is_expired() - boolean: return yes if domain is EXPIRED"""
        if domainname == "":
            print "no domain defined"
            return False
        # need to query the whois at this stage
        if self.checkdomainname(domainname):
            splitteddomain = domainname.split(".")
            test = self.whoisresponse(domainname)
            if splitteddomain[1] in ("com","net"):
                if test[7][0:12] == "No match for" :
                    print "%s is EXPIRED" % domainname
                    return True
            if splitteddomain[1] in ("org", "info", "biz"):
                if test[0][0:9].upper() == "NOT FOUND":
                    print "%s is EXPIRED" % domainname
                    return True
            if splitteddomain[1] == "it":
                if test[1][20:29] == "AVAILABLE":
                    print "%s is EXPIRED" % domainname
                    return True
        else:
            print "%s domain not valid" % domainname
        return False

d = Domain()
print "Running domain-expired check on directory %s/" % os.path.abspath(".")
for domainzonefiles in os.listdir("."):
    domainextention = domainzonefiles[-3:]
    if os.path.isfile(domainzonefiles) and domainextention == zonefileextention:
        domainname = domainzonefiles[:-3]
        print "\nFound domain zonefile %s" % domainzonefiles
        d.is_expired(domainname)
        time.sleep(5)
print "\nDone"
