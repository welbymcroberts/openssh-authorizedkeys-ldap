#!/usr/bin/python

import ldap, sys, os, pwd

LDAPURI = ''
LDAPDN = ''
LDAPPW = ''
LDAPBASE = ''

user = pwd.getpwuid( os.getuid() )[ 0 ]

class SSHKey:
    """
    SSHKey
    """
    def __init__(self,key):
        self.key = key

class LDAPGet:
    def __init__(self,user):
        self.con = ldap.initialize(LDAPURI)
        self.user = user
    def get_keys(self):
        try:
            #self.con.start_tls_s()
            self.con.simple_bind_s(LDAPDN, LDAPPW)
            filter = '(sAMAccountName=%s)' % self.user
            result = self.con.search_s( LDAPBASE, ldap.SCOPE_ONELEVEL, filter, ['url'] )
            r = []
            if len(result) > 0:
                for key in result[0][1]['url']:
                    r.append(SSHKey(key))
            return r
        except ldap.INVALID_CREDENTIALS:
            print "Your username or password is incorrect."
            sys.exit()
        except ldap.LDAPError, e:
            print e.message['info']
            if type(e.message) == dict and e.message.has_key('desc'):
                print e.message['desc']
            else:
                print e
            sys.exit()


print "## LDAP search for sAMAccountName=%s against %s/%s" %(user, LDAPURI,LDAPBASE)
l = LDAPGet(user)
for key in l.get_keys():
    print "%s" % ( key.key )
