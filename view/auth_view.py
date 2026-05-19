from flask import render_template

def login():
    return render_template('auth/login.html')

def register():
    return render_template('auth/register.html')