from flask import Flask, request, redirect, render_template
import cgi
import os
import re

app = Flask(__name__)
app.config['DEBUG'] = True


def verify_email(email):
    # regex check to see that the email is valid
    # only admits certain TLDS. 
    valid_email = re.compile('\w.+@\w+.(net|edu|com|org){3,20}')

    if valid_email.match(email):
        return True
    else:
        return False        

def verify_password(pass1, pass2):
    # requirements: 8 length, 1 special, 1 uppercase, 1 digit
    valid_pass = re.compile('(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[#@$!%*?&])[A-Za-z\d@$#!%*?&]{8,20}')
    
    if pass1 == pass2: # double checking equality
        if valid_pass.match(pass1):
            return True
        else:
            return False
    else:
        return False

@app.route('/', methods=['POST','GET'])
def signup():
    user = ''
    pass1 = ''
    pass2 = ''
    email = ''

    email_error = ''
    password_error = ''
    
    if request.method == "POST":
        # assign variables from form input
        user = cgi.escape(request.form['user'])
        pass1 = cgi.escape(request.form['pass1'])
        pass2 = cgi.escape(request.form['pass2'])
        email = cgi.escape(request.form['email'])

        # do passwords match?
        if pass1 == pass2: # passwords match!
            # does the password meet our security requirements?
            if verify_password(pass1, pass2) == True: # password meets requirements
                if email: # if they input an email
                    if verify_email(email) == True: # is that email valid?
                        return render_template('welcome.html', user=user)
                    else: # yo email is bogus! do us a real one
                        email_error = 'Please enter a valid email. No funny TLDs. Between 3-20 characters.'
                        email = '' # wipes email field
                        return render_template('signup.html', email_error=email_error, email=email)
                else: # no email, no problem.
                    return render_template('welcome.html', user=user)
            else: # password didn't meet the security requirements; display those, start again
                password_error = """Password requirements: 8 length, 1 digit, 1 uppercase,
                                and one special character. Because I can."""
                pass1 = '' # wipes password fields
                pass2 = ''
                return render_template('signup.html', password_error=password_error, pass1=pass1, pass2=pass2)
        else: # fat fingers warning
            password_error = 'Passwords do not match. (Copy and paste, yo)'
            pass1 = ''
            pass2 = ''
            return render_template('signup.html', password_error=password_error, pass1=pass1, pass2=pass2)

    return render_template('signup.html',user=user, pass1=pass1, pass2=pass2,email=email)


if __name__ == "__main__":
    app.run()
