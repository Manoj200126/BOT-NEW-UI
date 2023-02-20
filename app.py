import os
import MySQLdb
from flask import Flask, session, url_for, redirect, render_template, request, abort, flash
from database import db_connect
from database import db_connect,user_reg,user_loginact,user_viewimages
from database import db_connect 
import re
from sklearn.preprocessing import LabelEncoder
import joblib
import numpy as np
from werkzeug.utils import secure_filename

 

app = Flask(__name__)
app.secret_key = os.urandom(24)
PEOPLE_FOLDER = os.path.join('static', 'images')
app.config['UPLOAD_FOLDER'] = PEOPLE_FOLDER

@app.route("/")
def FUN_root():
    return render_template("index.html")

@app.route("/index.html")
def logout():
    return render_template("index.html")

# @app.route("/upload.html")
# def upload():
#     return render_template("upload.html")

@app.route("/register.html")
def reg():
    return render_template("register.html")

@app.route("/login.html")
def login():
    return render_template("login.html")

# @app.route("/upload.html")
# def up():
#     username = session['username']
#     data = view_vit(username)
#     return render_template("upload.html" , data = data)

@app.route("/viewdata.html")
def up1():
    return render_template("viewdata.html")

# -------------------------------------------register-------------------------------------------------------
@app.route("/regact", methods = ['GET','POST'])
def registeract():
   if request.method == 'POST':    
      id="0"
      status = user_reg(id,request.form['username'],request.form['password'],request.form['email'],request.form['mobile'],request.form['address'])
      if status == 1:
       return render_template("login.html",m1="sucess")
      else:
       return render_template("register.html",m1="failed")


@app.route("/botact", methods = ['GET','POST'])
def Vitaminact1():
   if request.method == 'POST': 
      username=session['username']
      a=request.form['ids']
      b=request.form['url']
      c=request.form['followers_count']
      d=request.form['friends_count']
      e=request.form['listed_count']
      f=request.form['favourites_count']
      g=request.form['verified']
      h=request.form['statuses_count']
      i=request.form['default_profile']
      j=request.form['default_profile_image']
      check = np.array([a,b, c, d, e, f, g,h, i,j]).reshape(1, -1)
      print(check[0])
      Labelx=LabelEncoder()
      check[:,1]=Labelx.fit_transform(check[:,1])
      check[:,6]=Labelx.fit_transform(check[:,6])
      check[:,8]=Labelx.fit_transform(check[:,8])
      check[:,9]=Labelx.fit_transform(check[:,9])    
      nb_spam_model = open("Bot_model.pkl", 'rb')
      clf = joblib.load(nb_spam_model)       
      B_pred = clf.predict(check[[0]])
      if B_pred == 1:
        print("FRAUD USER DETECTED IN SOCIAL NETWORK")
        outputsting="FRAUD USER DETECTED IN SOCIAL NETWORK"
        full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'FRAUD.jpg')
      else:
        outputsting="GENUINE USER DETECTED IN SOCIAL NETWORK"
        full_filename = os.path.join(app.config['UPLOAD_FOLDER'], 'GENUSER.jpg')

      print(outputsting)   

     
      return render_template("upload.html",m1="sucess",first=outputsting,user_image = full_filename)
    
#--------------------------------------------Login-----------------------------------------------------
@app.route("/loginact", methods=['GET', 'POST'])
def useract():
    if request.method == 'POST':
        status = user_loginact(request.form['username'], request.form['password'])
        print(status)
        if status == 1:
            session['username'] = request.form['username']                             
            return render_template("userhome.html", m1="sucess")
        else:
            return render_template("login.html", m1="Login Failed")

@app.route("/viewimage.html")
def viewimages():
    data = user_viewimages(session['username'])
	 
    print(data)
    return render_template("viewimage.html",user = data)


if __name__ == "__main__":
    app.run(debug=True, host='127.0.0.1', port=5000,use_reloader = False)
