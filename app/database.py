##This class is meant to mimic a normal database
##It is therefore NOT a real database object class
class User(object):
    def __init__(self, email, username, password):
        self.__email = email
        self.__username = username
        self.__password = password
    
    def printEmail(self):
        return self.__email
    
    def printUsername(self):
        return self.__username

    def printPassword(self):
        return self.__password