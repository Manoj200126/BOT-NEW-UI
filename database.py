import sqlite3
import hashlib
import datetime
import MySQLdb
from flask import session
from datetime import datetime
 
import numpy as np 
import numpy as np
import os 
import datetime

 
 
 

def db_connect():
    _conn = MySQLdb.connect(host="localhost", user="root",
                            passwd="root", db="vitamin")
    c = _conn.cursor()

    return c, _conn

# -------------------------------register-----------------------------------------------------------------
def user_reg(id,username, password, email, mobile, address,):
    try:
        c, conn = db_connect()
        print(id,username, password, email,
               mobile, address)
        j = c.execute("insert into register (id,username,password,email,mobile,address) values ('"+id+"','"+username +
                      "','"+password+"','"+email+"','"+mobile+"','"+address+"')")
        conn.commit()
        conn.close()
        print(j)
        return j
    except Exception as e:
        print(e)
        return(str(e))

# -------------------------------------Login --------------------------------------
def user_loginact(username, password):
    try:
        c, conn = db_connect()
        j = c.execute("select * from register where username='" +
                      username+"' and password='"+password+"'")
        data = c.fetchall()
        for a in data:
           session['uname'] = a[0]
       
        c.fetchall()
        conn.close()
        return j
    except Exception as e:
        return(str(e))


#---------------------------------------View Images---------------------------------------
def user_viewimages(username):
    c, conn = db_connect()
    c.execute("select * from upload where  username='"+username +"'")
    result = c.fetchall()
    conn.close()
    print("result")
    return result


if __name__ == "__main__":
    print(db_connect())
