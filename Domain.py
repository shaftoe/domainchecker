#/usr/bin/env python
import subprocess
import os.path
import time

class Domain:
    """Domain(str "domainname")
    It is meant to give access to whois database in a object-oriented way
    Interface:
    isExpired() - boolean: return yes if a domain is EXPIRED
    """
    
    alloweddomains = ("com", "info", "it", "org", "net", "biz") # allowed domain extentions available for checking

    def checkDomainName(self, domainname):
        """checkDomainName(self, domainname):
        return a boolean, true if domain is syntactically correct
        Unfortunately till now works just with secondLevel domains...
        """
        splitteddomain = domainname.split(".")
        if len(splitteddomain) != 2 or splitteddomain[1] not in self.alloweddomains:
            return False
        return True

    def whoisResponse(self, domainname):
        """Query the whois database via "whois" command end returns a list
        with lines
        """
        try:
            r = subprocess.Popen(['whois', domainname], stdout=subprocess.PIPE)
        except OSError:
            print "Someting wrong... make sure WHOIS is installed and in $PATH"
            quit()
        return r.stdout.readlines()


    def isExpired(self, domainname=""):
        """isExpired() - boolean: return True if domain is EXPIRED, False otherwise
        Rises a TypeError if no domain is defined
        """
        if domainname == "":
            raise TypeError, "no domain defined"
            return False
        # need to query the whois at this stage
        if self.checkDomainName(domainname):
            splitteddomain = domainname.split(".")
            test = self.whoisResponse(domainname)
            if splitteddomain[1] in ("com","net"):
                if test[7][0:12] == "No match for" :
                    return True
            if splitteddomain[1] in ("org", "info", "biz"):
                if test[0][0:9].upper() == "NOT FOUND":
                    return True
            if splitteddomain[1] == "it":
                if test[1][20:29] == "AVAILABLE":
                    return True
        else:
            print "%s domain not valid" % domainname
        return False
