from flask import Flask, request, redirect, render_template
import cgi
import os
import re

app = Flask(__name__)
app.config['DEBUG'] = True


def verify_email(email):
    '''Checks for valid email via regex; returns a bool'''
    # regex check to see that the email is valid
    # only admits certain TLDS. 
    valid_email = re.compile('(\w.+@\w+.(net|edu|com|org)')

    if valid_email.match(email):
        return True
    else:
        return False        

def verify_password(pass1, pass2):
    '''Checks for password symmetry and min. requirements via regex; returns a bool.'''
    # requirements: 8-20 length, 1 special, 1 uppercase, 1 digit
    valid_pass = re.compile('(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[#@$!%*?&])[A-Za-z\d@$#!%*?&]{8,20}')
    
    # double checking equality and regex match
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

    if request.method == 'POST': # User submits data
        # assign variables from form input
        user = cgi.escape(request.form['user'])
        pass1 = cgi.escape(request.form['pass1'])
        pass2 = cgi.escape(request.form['pass2'])
        email = cgi.escape(request.form['email'])

        if not pass1 == pass2:
            # passwords don't match; set error message and wipe variable
            password_match_error = 'Passwords do not match. (Copy and paste, yo)'
#            pass1 = ''
#            pass2 = ''

        if email: # Build an email error message
            if len(email) < 3 or len(email) > 20:
                email_error = 'Emails must be between 3-20 characters.'

            if not verify_email(email):
                # invalid email, set error message and wipe variable
                email_error = email_error + 'Invalid TLD.'
                email = ''

        if not verify_password(pass1, pass2):
            # password doesn't meet requirements; set error and wipe variables
            password_error = """Password requirements: 8-20 length, 1 digit, 1 uppercase,
                                and one special character."""
#            pass1 = ''
#            pass2 = ''

        # There's an error, so repopulate fields and let user start over
        if email_error or password_error or password_match_error:
            pass1 = ''
            pass2 = ''
            return render_template('signup.html', user=user, email=email, pass1=pass1, pass2=pass2, email_error=email_error, password_error=password_error, password_match_error=password_match_error) # var=var=var=error=error=...

        # happy path; user wins, passes go, collects $200 (but not from me)
        # allows for rendering regardless of there being an email entered or not
        return render_template('welcome.html', user=user)                    

    # Draws an empty form from empty strings above
    return render_template('signup.html',user=user, pass1=pass1, pass2=pass2,email=email)


if __name__ == "__main__":
    app.run()

# Original handling logic. Decided to refactor this using "guard clauses" after reading a blog
# Changes also made it easy to display all possible error messages simeltaneously as
# the messages are now set outside of a nested if with a return
''' 
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
                        return render_template('signup.html', user=user, email_error=email_error, email=email)
                else: # no email, no problem.
                    return render_template('welcome.html', user=user)
            else: # password didn't meet the security requirements; display those, start again
                password_error = """Password requirements: 8-20 length, 1 digit, 1 uppercase, and one special character."""
                pass1 = '' # wipes password fields
                pass2 = ''
                return render_template('signup.html', user=user, email=email, password_error=password_error, pass1=pass1, pass2=pass2)
        else: # fat fingers warning
            password_error = 'Passwords do not match. (Copy and paste, yo)'
            pass1 = ''
            pass2 = ''
            return render_template('signup.html', user=user, email=email, password_error=password_error, pass1=pass1, pass2=pass2)
'''
