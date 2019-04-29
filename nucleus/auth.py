import logging

import urllib, sys

from crequest.middleware import CrequestMiddleware
from nucleus import settings
from HTMLParser import HTMLParser

class UserCredentials():
    
    OUNetID = None
    FirstName = None
    LastName = None
    Email = None
    MemberOf = None
    
    AuthMemCookie = None
    SimpleSAML = None
    SimpleSAMLAuthToken = None
    
    def __init__(self):
        h = HTMLParser()
        request = CrequestMiddleware.get_request()
        
        if request is None:
        
            self.AuthMemCookie = None
            self.SimpleSAML = None
            self.SimpleSAMLAuthToken = None
            self.OUNetID = None
            self.FirstName = None
            self.LastName = None
            self.Email = None
            self.MemberOf = None
            
        else:

            self.AuthMemCookie = request.COOKIES["AuthMemCookie"]
            self.SimpleSAML = request.COOKIES["SimpleSAML"]
            self.SimpleSAMLAuthToken = request.COOKIES["SimpleSAMLAuthToken"]
    
            self.OUNetID = urllib.unquote(request.COOKIES["OUNetID"]) if ("OUNetID" in request.COOKIES) else "" 
            self.FirstName = urllib.unquote(request.COOKIES["FirstName"]) if ("FirstName" in request.COOKIES) else "" 
            self.LastName = urllib.unquote(request.COOKIES["LastName"]) if ("LastName" in request.COOKIES) else ""
            self.Email = urllib.unquote(request.COOKIES["Email"]) if ("Email" in request.COOKIES) else ""
            
            groups = urllib.unquote(request.COOKIES["MemberOf"]) 
            self.MemberOf = groups.split(":")

        
    def get_AuthMemCookie(self):
        return self.AuthMemCookie
    
    def get_SimpleSAML(self):
        return self.SimpleSAML
    
    def get_SimpleSAMLAuthToken(self):
        return self.SimpleSAMLAuthToken
    
    def get_OUNetID(self):
        return self.OUNetID
    
    def get_FirstName(self):
        return self.FirstName
    
    def get_LastName(self):
        return self.LastName
    
    def get_Email(self):
        return self.Email
    
    def get_MemberOf(self):
        return self.MemberOf
    
    def is_member(self, groups):
        result = False
        if isinstance(groups, list):
            if any(group in groups for group in self.MemberOf):
                result = True
        else:
            if any(groups == s for s in self.MemberOf):
                result = True
        return result

    def is_admin(self):
        if any("PACSATAdmin" in s for s in self.MemberOf):
            return True
        else :
            return False
        
     

