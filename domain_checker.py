#/usr/bin/env python
import subprocess
import os.path
import time

zonefileextention = ".sh"

class Domain:
    """Domain(str "domainname")
    It is meant to give access to whois database in a object-oriented way
    Interface:
    isExpired() - boolean: return yes if domain is EXPIRED
    """
    
    alloweddomains = ("com", "info", "it", "org", "net", "biz")

    def checkDomainName(self, domainname):
        """checkDomainName(self, domainname):
        return a boolean, true if domain is syntactically correct
        Unfortunately for now works just with secondLevel domains..."""
        splitteddomain = domainname.split(".")
        if len(splitteddomain) != 2 or splitteddomain[1] not in self.alloweddomains:
            return False
        return True

    def whoisResponse(self, domainname):
        """Query the whois database via "whois" command end returns a list
        with lines"""
        try:
            r = subprocess.Popen(['whois', domainname], stdout=subprocess.PIPE)
        except OSError:
            print "Someting wrong... make sure WHOIS is installed and in $PATH"
            quit()
        return r.stdout.readlines()


    def isExpired(self, domainname=""):
        """isExpired() - boolean: return yes if domain is EXPIRED"""
        if domainname == "":
            print "no domain defined"
            return False
        # need to query the whois at this stage
        if self.checkDomainName(domainname):
            splitteddomain = domainname.split(".")
            test = self.whoisResponse(domainname)
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
        d.isExpired(domainname)
        time.sleep(5)
print "\nDone"
