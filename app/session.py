##This class will manage user sessions
from flask import session

class Session():
    ##Create session upon successful login
    def createSession(name):
        session['user'] = name
    #Get session will return current active session
    #If no session found, returns None
    def getSession():
        if 'user' in session:
            return session['user']

        return 'None'
    
    #Function to check if user is logged in
    #Returns boolean value True and false otherwise
    def isLoggedIn():
        if 'user' in session:
            return True

        return False

    ##Drops current active session such that its no longer active...logging out
    def dropSession():
        session.pop('user', None)
        return True