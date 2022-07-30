
import os 
import sqlite3
from tabnanny import check 

UPLOAD_FOLDER = 'static/images/'
def registerNewUser(form,db) :
    cursor = db.cursor() 
    # inserting values for user table
    values = (form['name'],form['username'].lower(),form['email'],form['password'])
    query = 'insert into users values(?,?,?,?)'
    try : 
        cursor.execute(query,values) 
    except Exception as e  : 
        return (False , e)
    # inserting values for userprofile table
    cursor.execute('insert into userprofile (username) values(?)',(form['username'].lower(),))
    db.commit() 
    return (True , 'You are Registered .. now sign In')


def logInUser(form,db) : 
    cursor = db.cursor() 
    query = 'select password from users where username=(?)'
    cursor.execute(query,(form['username'].lower(),))
    result = cursor.fetchone() 
    if result and len(result) == 1 and form['password'] == result[0] : 
           return (True , 'logged In')
    return (False , 'Username and password Don\'t match')


def getUserProfileDetails(username,db) : 
    cursor = db.cursor() 
    query = 'select * from userprofile where username=(?)' 
    cursor.execute(query,(username,)) 
    return list(cursor.fetchone())

# update bio 

def updateProfileBio(username,bio,db) : 
    cursor = db.cursor() 
    query = '''update userprofile 
        set bio=(?) where username=(?)
    '''
    cursor.execute(query,(bio,username))
    db.commit()

# update profile picture 

def updateProfilePic(fileName ,username, db) : 
    cursor = db.cursor() 
    query = '''update userprofile
        set profilepic=(?) where username=(?)
    '''
    cursor.execute(query,(fileName,username))
    db.commit()

# delete profile picture 

def deleteProfilePic(username,db) : 
    cursor = db.cursor() 
    query = 'select profilepic from userprofile where username=(?)'
    cursor.execute(query,(username,))
    addressOfProfilePic = cursor.fetchone()[0] 
    if addressOfProfilePic == '' : 
        return 
    os.remove(addressOfProfilePic)
    query = '''update userprofile
        set profilepic="" where username=(?)
    '''
    cursor.execute(query,(username,))

# get userprofile all posts they have done
def getUserProfilePosts(username, db) : 
    cursor = db.cursor() 
    query = 'select postbio,postpic from posts where username=(?)'
    cursor.execute(query,(username,))
    allPosts = cursor.fetchall() 
    return allPosts

def addProfilePosts(username,extension, bio , db) : 
    cursor = db.cursor() 
    # cursor.execute('insert into posts(username,postbio) values(?,?)',(username,bio))
    cursor.execute('select username from posts where username=(?)',(username,))
    postId = len(cursor.fetchall()) + 1
    fileName = os.path.join(UPLOAD_FOLDER,username + str(postId) + extension)
    query = 'insert into posts(username,postpic,postbio) values(?,?,?)'
    cursor.execute(query,(username,fileName,bio))
    db.commit()
    return fileName

# get chathistory 

def getChatHistory(username , db) : 
    cursor = db.cursor() 
    cursor.execute('select * from userchats where currentuser=(?)',(username,))
    chatHistory = cursor.fetchall() 
    
    # testing 
    newChatHistory = []
    for chats in chatHistory :
        newChats = list(chats) 

        cursor.execute('select profilepic from userprofile where username=(?)' , (newChats[1],))
        newChats.append(cursor.fetchone()[0])
        newChatHistory.append(newChats)
    # testing
    return newChatHistory

# updating chat table 
def updateChatTable(fromUserName , toUserName , message,db) :   
    cursor = db.cursor()
   
    def checkIfAlreadyTexted() : 
        print("checking if already texted\n\n\n")
        query = 'select messages from userchats where currentuser=(?) and touser=(?)'
        cursor.execute(query,(fromUserName,toUserName))
        res = cursor.fetchall() 
        if len(res) == 0: 
            toReload = True 
            return (False , toReload)
        elif len(res) == 1 and res[0][0] == '' :
            toReload = True 
            return (True , toReload) 
        return (True , False)
    
    # getting the old value of messages 
    (alreadyTexted , toReload) = checkIfAlreadyTexted()
    if alreadyTexted :
        query= 'select messages from userchats where currentuser=(?) and touser=(?)'
        cursor.execute(query,(fromUserName,toUserName))
        print("message sented :" , message ,'\n\n\n\n')
        message = cursor.fetchone()[0] + '\n' +message
        # updating the table 
        query = '''update userchats
            set messages=(?) where currentuser=(?) and touser=(?)
        '''
        cursor.execute(query , (message,fromUserName , toUserName))
    # registering a new chat 
    else : 
        query = 'insert into userchats values(?,?,?)'
        cursor.execute(query,(fromUserName,toUserName , message))
    db.commit()
    print("final to reload" , toReload)
    return toReload


def getProfileBasedOnSearch(searchtext,db) : 
    cursor =db.cursor() 
    query = f"select username,profilepic from userprofile where username LIKE '{searchtext}%'"
    cursor.execute(query)
    res = cursor.fetchall() 
    newRes = [] 
    for profiles in res : 
        newProfile = list(profiles) 
        newRes.append(newProfile)
    return newRes