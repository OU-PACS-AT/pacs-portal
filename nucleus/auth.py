import logging

from crequest.middleware import CrequestMiddleware
from nucleus import settings

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
    
            self.OUNetID = request.COOKIES["OUNetID"]
            self.FirstName = request.COOKIES["FirstName"]
            self.LastName = request.COOKIES["LastName"]
            self.Email = request.COOKIES["Email"]
            
            groups = request.COOKIES["MemberOf"]
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
    
    def is_staff(self):
        if any("Staff" in s for s in self.MemberOf):
            return True
        else :
            return False
        
    def is_faculty(self):
        if any("Faculty" in s for s in self.MemberOf):
            return True
        else :
            return False
        
    def is_student(self):
        if any("Student" in s for s in self.MemberOf):
            return True
        else :
            return False


    def is_admin(self):
        if any(self.OUNetID in s for s in settings.ADMINS):
            return True
        else :
            return False
        
     

