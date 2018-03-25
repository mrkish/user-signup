from flask import Flask, request, redirect, render_template
import cgi
import os

app = Flask(__name__)
app.config['DEBUG'] = True


def verify_email(email):
    # regex check to see that the email is valid
    return True

def verify_password(pass1, pass2):

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