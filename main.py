from flask import Flask, request, redirect, render_template
import os
import jinja2

app = Flask(__name__)
app.config['DEBUG'] = True

#jinja
template_dir = os.path.join(os.path.dirname(__file__),'templates') 
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=True)


#index route loads a basic welcome page that links to user sign up
@app.route("/")
def index():
    template = jinja_env.get_template('index.html')
    return template.render()


#signup page
@app.route("/signup")
def display_signup_page():
    return render_template('signup.html', title="User Signup")


#welcome page
def display_welcome_page():
    return render_template('welcome.html', title="Welcome!")


#signup validation
@app.route("/signup", methods=['POST'])
def signup_validation():
    #error message variable initilization
    username_error =""
    password_error = ""
    verify_password_error = ""
    email_error = ""
    #sets variable equal to user data
    username = request.form['username']
    password = request.form['pass']
    verify_password = request.form['verifypass']
    email = request.form['email']

    
    #checks for empty input
    if username == "":
        username_error = "Required"
    if password == "":
        password_error = "Required"
    if verify_password == "":
        verify_password_error = "Required"

        
    #checks username + password + email for spaces
    if " " in username:
        username_error = "No Spaces Allowed"
    if " " in password:
        password_error = "No Spaces Allowed"
        verify_password_error = "No Spaces Allowed"
    if " " in email:
        email_error = "No Spaces Allowed"

        
    #all confirmation input are 3 and 20 characters long
    if (3 > len(username) or len(username) > 20) and username != "" :
        username_error = "Username must be between 3 to 20 characters long."

    if (3 > len(password) or len(password) > 20) and password != "" :
        password_error = "Password must be between 3 to 20 characters long." 
    
    if (3 > len(email) or len(email) > 20) and email != "":
        email_error = "Email must be between 3 to 20 characters long."

        
    #check that password and verifypassword match
    if password != verify_password:
        password_error = "Passwords do not match!"
        verify_password_error = "Passwords do not match!"

        
    #verify email has (@ .) must be between 3 and 20 characters
    if ("@" not in email or "." not in email) and (email != ""):
        email_error = "Invalid Email Given."

        
    #validation check > if all input is valid > render welcome page
    if not username_error and not password_error and not email_error:
        template = jinja_env.get_template('welcome.html')
        return template.render(username=username)

    
    template = jinja_env.get_template('signup.html')
    return template.render(email=email,username=username, username_error=username_error, password_error=password_error, verify_password_error=verify_password_error, email_error=email_error)


app.run()