#!/usr/bin/env python
# coding: utf-8

# PREMIER SITE ESSAI

from flask import Flask, render_template, Markup, request, url_for
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
import cx_Oracle
import datetime
from sqlalchemy import create_engine
from gevent.pywsgi import WSGIServer
engine = create_engine('oracle://sbc2937a:yaya31@telline.univ-tlse3.fr:1521/etupre', max_identifier_length=128)

app=Flask(__name__)
mail=Mail(app)
s=URLSafeTimedSerializer('Secret key')

@app.route('/home/', methods = ['POST'])
def home(): 
    motdepasse = request.form['login_password']
    email = request.form['login_login']
    strSQL = "select mot_de_passe from cheikh_connexion where adresse_mail = '" + email + "' and compte_actif=1" 
    with engine.connect() as con:
        mdp = con.execute(strSQL)
        for row in mdp :
            for element in row : 
                if (element == motdepasse):
                    return render_template("pages/home.html", pseudo=email)
    return render_template("pages/menuConnexion.html", content = -1)

@app.route('/')#connexion
def connexion():
    return render_template('pages/menuConnexion.html')

@app.route('/inscription')
def inscription():
    return render_template("pages/menuInscription.html")

@app.route('/inscrit/', methods = ['GET', 'POST'])
def inscrit():
    motdepasse = request.form['login_password']
    email = request.form['login_login']
    prenom= request.form['login_prenom']
    nom= request.form['login_nom']
    date_naiss=request.form['login_date_naiss']

    #email confirmation
    token= s.dumps(email, salt='email-confirm')
 
    msg = Message('Email de confirmation', sender='noreply@gmail.com', recipients=[email])

    link=url_for('confirm_email', token=token, _external=True)

    msg.body= 'Votre lien de confirmation est {}'.format(link)

    print("-------------------messaaaaa--------------")
    mail.send(msg)
    print("----------------depaseeeeeeeeeeeeeeee----------")

    connection = engine.raw_connection()
    try:
        cursor = connection.cursor()
        retour = cursor.var(cx_Oracle.NUMBER)  # variable OUT
        num_confirmation = cursor.var(cx_Oracle.NUMBER)  # variable OUT
        cursor.callproc("cheikh_inscription", [email,motdepasse,prenom, nom, date_naiss, retour, num_confirmation])
        cursor.close()
        connection.commit()
    finally:
        connection.close()
    return render_template("pages/menuInscription.html", content = retour.values[0] )

@app.route('/confirm_email/<token>')
def confirm_email(token):
    try:
        email=s.loads(token, salt='email-confirm', max_age=20)
        print(email)
    except SignatureExpired:
        return '<script> alert("Lien de confirmation expirée")</script>'

if __name__=='__main__':
    app.run( port=3309, debug=True)
    #http_server = WSGIServer(('', 3309), app)















# In[ ]:




