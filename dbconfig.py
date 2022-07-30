from math import trunc
from os import truncate
import sqlite3 
def run() :
    db = sqlite3.connect('database.db') 
    cursor = db.cursor() 
    # create a users table 
    query = ''' CREATE table users
        (name text not null,
        username text not null primary key,
        email text not null unique,
        password text not null)'''

    cursor.execute(query) 
    # create a user profile table
    query = '''create table userprofile(
        username text not null,
        profilepic text default "" ,
        bio text default "",
        foreign key(username)
        references users(username)
    )
    '''
    cursor.execute(query)
    # create a posts table
    query = '''create table posts(

        username text not null,
        postpic text default "" , 
        postbio text default "",
        foreign key(username)
        references users(username)
    )
    '''
    cursor.execute(query)

    # create a chat table
    query = '''create table userchats(
        currentuser text , 
        touser text , 
        messages text default ""
    )'''
    cursor.execute(query)
    db.close()

def truncateTable() : 
    db = sqlite3.connect('database.db') 
    cursor = db.cursor() 
    cursor.execute('delete from users') 
    db.commit() 
    db.close()

def showDatabase() : 
    db = sqlite3.connect('database.db') 
    cursor = db.cursor() 
    cursor.execute('select * from users') 
    print("Users table")
    for x in cursor.fetchall() : 
        print(x) 
    print("userProfile table") 
    cursor.execute("select * from userprofile") 
    for x in cursor.fetchall() : 
        print(x) 
    print("posts") 
    cursor.execute("select * from posts") 
    for x in cursor.fetchall() : 
        print(x) 
    cursor.execute("select * from userchats") 
    print("userChats")
    for x in cursor.fetchall() : 
        print(x)

run()