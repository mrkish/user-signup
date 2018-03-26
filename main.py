from flask import Flask, request, redirect, render_template
import cgi
import os
import re

app = Flask(__name__)
app.config['DEBUG'] = True


def verify_email(email):
    # regex check to see that the email is valid
    valid_email = re.compile('\w.+@\w+.(net|edu|com|org)')
    if valid_email.match(email):
        return True
    else:
        return False        

def verify_password(pass1, pass2):
    valid_pass = re.compile('(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[#@$!%*?&])[A-Za-z\d@$#!%*?&]{8,}')

    if pass1 == pass2:
        if valid_pass.match(pass1):
            return True
        else:
            password_error = """Please enter a password of 8 characters or longer with 
                              at least one upper and lowercase character, one special 
                              character, and one digit."""
            return False

    return True 
    

@app.route('/', methods=['POST','GET'])
def signup():

    email_error = ''
    password_error = ''
    
    if request.method == "POST":
        user = cgi.escape(request.form['user_name'])
        email = request.form['email']
        pass1 = request.form['password1']
        pass2 = request.form['passowrd2']

        if (verify_email(email) == True and
            verify_password(pass1, pass2) == True):
            
            return render_template('signup.html')

    return render_template('signup.html')



if __name__ == "__main__":
    app.run()