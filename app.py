
from crypt import methods
from flask import Flask, flash, jsonify, redirect, render_template , request, url_for ,session
import sqlite3
import static.python.functions as utilities
from werkzeug.utils import secure_filename
import os 
from flask_socketio import SocketIO , send , emit


app = Flask(__name__) 
socketio = SocketIO(app) 
app.secret_key = 'secret'
UPLOAD_FOLDER = 'static/images/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
def allowed_file(filename):
     return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
def checkUserLoggedIn() : 
    if 'user' in session : 
        return True 
    return False 
# Home page 
@app.route('/home')
@app.route('/') 
def homePage() : 
    if 'user' in session : 
        return redirect(url_for('profile'))
    return render_template('home.html')

# login

@app.route('/',methods=['POST']) 
def login() : 
    db = sqlite3.connect('database.db')
    form = request.form
    loggedIn , msg = utilities.logInUser(form,db) 
    db.close()
    if not loggedIn : 
        return render_template('home.html',msg=msg)
    session['user'] = form['username'].lower() 
    return redirect(url_for('profile'))

# register user 

@app.route('/register') 
def registerPage() : 
    return render_template('register.html')

@app.route('/register',methods=['POST']) 
def register() : 
    db = sqlite3.connect('database.db') 
    isRegistered , msg = utilities.registerNewUser(request.form,db) 
    db.close()
    if not isRegistered : 
        return render_template('register.html',msg=msg) 
    else : 
        return render_template('home.html',msg=msg)

# user profile 

@app.route('/profile') 
def profile() : 
    if 'user' in session : 
        user = session['user'].lower()
        db = sqlite3.connect('database.db')
        userprofile = utilities.getUserProfileDetails(user , db)
        userprofileposts = utilities.getUserProfilePosts(user,db)
        db.close()
        return render_template('profile.html',user=user,userprofile=userprofile,userprofileposts=userprofileposts,canedit=1)
    else : 
        return redirect(url_for('homePage'))

# sho other user profile 
@app.route('/profile/others/<string:username>') 
def profileUser(username) : 
    db = sqlite3.connect('database.db') 
    userprofile = utilities.getUserProfileDetails(username , db) 
    userprofileposts = utilities.getUserProfilePosts(username,db)
    db.close() 
    return render_template('profile.html',user=username , userprofile=userprofile , userprofileposts=userprofileposts ,canedit=0)


# user profile edit
# home user edit profile
@app.route('/editprofile',methods=['GET'])
def editProfile() : 
    return render_template('editprofile.html')

# user profile edit
#  update bio 
@app.route('/editprofile/addbio',methods=['post'])  
def addProfileBio() : 
    db = sqlite3.connect('database.db')
    bio = request.form['profilebio']
    currentUser = session['user'] 
    utilities.updateProfileBio(currentUser,bio,db)
    db.close()
    return redirect(url_for('profile'))

#user profile edit 
# update profilepic
@app.route('/editprofile/addprofilepic',methods=['POST']) 
def updateProfilePic() : 
    db = sqlite3.connect('database.db')
    username = session['user']
    file = request.files['file'] 
    fileName = secure_filename(file.filename)
    # check for allowed file names 
    if not allowed_file(fileName) : 
        return redirect(url_for('editProfile'))
    extentsion = os.path.splitext(fileName)[1] 
    # storing the file name as unique
    utilities.deleteProfilePic(username,db)
    fileName = os.path.join(UPLOAD_FOLDER,f'{username}profilepic{extentsion}')
    file.save(fileName)
    # saving the filename to database 

    utilities.updateProfilePic(fileName ,username, db)
    db.close()
    return redirect('/profile')

#user profile edit 
# add posts
@app.route('/ediprofile/addposts',methods=['POST'])
def addProfilePosts() : 
    username = session['user']
    file = request.files['file']
    bio = request.form['bio'] 
    fileName = secure_filename(file.filename)
    # check for allowed file names 
    if not allowed_file(fileName) : 
        return redirect(url_for('editProfile'))
    extentsion = os.path.splitext(fileName)[1] 
    
    db = sqlite3.connect('database.db')
    fileName = utilities.addProfilePosts(username,extentsion,bio,db)
    file.save(fileName)
    db.close()
    return redirect('/profile')
    
# chat app
@app.route('/profile/chat')
def chatApp() : 
    if checkUserLoggedIn() : 
        userName = session['user']
        db = sqlite3.connect('database.db')
        chatHistory = utilities.getChatHistory(userName , db)
        userprofile = utilities.getUserProfileDetails(userName , db)
        db.close()
        print(chatHistory)
        return render_template('chat.html',userprofile=userprofile,chathistory=chatHistory)
    return "NOT LOGGED IN"


# active chat users list 
activeChatUsers = {} 


#all socket io functionalities
#connection
@socketio.on('message',namespace='/chat') 
def handle_message(msg) : 
    userName = session['user']
    if userName not in activeChatUsers : 
        activeChatUsers[userName] = request.sid
    print(userName + msg)

# recieving msg from client and sending to another client
@socketio.on('client-sended-message',namespace='/chat')
def recievedMessage(payLoad) : 
    toUsername = payLoad['tousername'] 
    message = payLoad['message']
    fromUsername = session['user'] 
    db = sqlite3.connect('database.db')
    # to reload the client page for a new text message
    message = fromUsername + ' : ' + message
    # checking if it is the first message and updating the database
    toReload = utilities.updateChatTable(fromUsername,toUsername,message,db)
    print("to reload in main app function ",toReload)
    utilities.updateChatTable(toUsername,fromUsername,message,db)
    if toUsername in activeChatUsers :
        toUserNameSessionId = activeChatUsers[toUsername]
        emit('recieved-message',{'fromusername' : fromUsername , 'message' : message , 'toreload' : toReload},room=toUserNameSessionId)
    
#if user disconnected
@socketio.on('disconnect' ,namespace='/chat') 
def handle_message() : 
    userName = session['user'] 
    if userName in activeChatUsers : 
        del activeChatUsers[userName]
    print(userName + " disconnected")


# search others
@app.route('/profile/search') 
def searchOthers() : 
    return render_template('search.html') 

# search others 
@app.route('/profile/search/<string:searchtext>' ,methods=['GET'])
def searchWithName(searchtext) : 
    db = sqlite3.connect('database.db') 
    profiles = utilities.getProfileBasedOnSearch(searchtext,db)
    db.close()
    return jsonify(profiles)

# requesting to chat to a new user 
@app.route('/profile/search/adduser/<string:tousername>')
def addProfileSearchUser(tousername) : 
    fromUserName = session['user'] 
    toUsername = tousername
    message = ''
    db = sqlite3.connect('database.db')
    utilities.updateChatTable(fromUserName,toUsername,message,db)
    utilities.updateChatTable(toUsername,fromUserName,message,db)
    return redirect('/profile/chat')
    db.close()
#user profile logout


@app.route('/logout',methods=['POST'])
def logout() : 
    session.pop('user') 
    return redirect(url_for('homePage'))

if __name__ == '__main__' : 
    socketio.run(app,debug = True,host='0.0.0.0') 

# also delete from session when removing a user


# at last sort the chats based on timestamps