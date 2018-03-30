from flask import Flask, request, redirect, render_template
import cgi
import os
import re

app = Flask(__name__)
app.config['DEBUG'] = True

def verify_email(email):
    '''Checks for valid email via regex; returns a bool.
    Only admits common TLD emails.'''

    valid_email = re.compile('\w.+@\w+.(net|edu|com|org)')

    if valid_email.match(email):
        return True
    else:
        return False        

def verify_password(pass1, pass2):
    '''Checks for password symmetry and min. requirements via regex; returns a bool.
    Requirements: 8-20 length, 1 special, 1 uppercase, 1 digit'''

    valid_pass = re.compile('(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[#@$!%*?&])[A-Za-z\d@$#!%*?&]{8,20}')

    if pass1 == pass2 and valid_pass.match(pass1):
        return True
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
    password_match_error = ''

    if request.method == 'POST': # user submits data
        # assign escaped variables from form input
        user = cgi.escape(request.form['user'])
        pass1 = cgi.escape(request.form['pass1'])
        pass2 = cgi.escape(request.form['pass2'])
        email = cgi.escape(request.form['email'])

        if not pass1 == pass2:
            # passwords don't match; set error message
            password_match_error = 'Passwords do not match. (Copy and paste, yo)'

        if not verify_password(pass1, pass2):
            # password doesn't meet requirements; set error message
            password_error = """Password requirements: 8-20 length, 1 digit, 1 uppercase, and one special character."""

        if email:  # If user enters an email
            # Check for length; if too long, create specific error output.
            if len(email) < 3 or len(email) > 20:
                email_error = 'Emails must be between 3-20 characters. '

            if not verify_email(email):
                # Invalid TLD/formating; will combine with length error if present.
                email_error = email_error + 'Invalid formating and/or TLD. Only .com/.edu/.org/.net addresses accepted.'

            if email_error:
                # wipes email if an error has been created in this block, which
                # must happen after both error checks have occured
                email = ''

        # Wipe PW fields and let user try again
        if email_error or password_error or password_match_error:
            pass1 = ''
            pass2 = ''
            return render_template('signup.html', title='Signup',user=user, email=email, pass1=pass1, pass2=pass2, email_error=email_error, password_error=password_error, password_match_error=password_match_error) # var=var=var=error=error=...

        # happy path; user wins, passes go, collects $200 (but not from me)
        # allows for rendering regardless of there being an email entered or not
        return render_template('welcome.html', title='Welcome, ' + user + '!', user=user)                    

    # Draws an empty form from empty strings above
    return render_template('signup.html', title='Signup', user=user, pass1=pass1, pass2=pass2,email=email)

if __name__ == "__main__":
    app.run()
