from flask import Flask, url_for, session, render_template, redirect  # Import necessary Flask modules
from authlib.integrations.flask_client import OAuth  # Import OAuth module
import json  # Import JSON module for data serialization
import requests  # Import requests module for making HTTP requests
import webbrowser

app = Flask(__name__)  # Create Flask application instance

# Configuration settings
appConf = {
    "OAUTH2_CLIENT_ID": "696489702018-6ufophl5cone35ehp28umug20sn8mp0k.apps.googleusercontent.com",
    # Google OAuth client ID
    "OAUTH2_CLIENT_SECRET": "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",  # Google OAuth client secret
    "OAUTH2_META_URL": "https://accounts.google.com/.well-known/openid-configuration",  # Google OAuth metadata URL
    "FLASK_SECRET": "d67a0009-26b2-4e9d-93e9-7ed3d5db35f2",  # Secret key for Flask session
    "FLASK_PORT": 5000  # Flask application port
}

# Setting the secret key for the session
app.secret_key = appConf.get("FLASK_SECRET")

# Creating OAuth instance
oauth = OAuth(app)

# Registering OAuth provider (Google)
oauth.register("myApp",
               client_id=appConf.get("OAUTH2_CLIENT_ID"),
               client_secret=appConf.get("OAUTH2_CLIENT_SECRET"),
               server_metadata_url=appConf.get("OAUTH2_META_URL"),
               client_kwargs={
                   "scope": "openid profile email https://www.googleapis.com/auth/user.birthday.read https://www.googleapis.com/auth/user.gender.read",
               }
               )


# Home route
@app.route("/")  # Define route for the home page
def home():
    """Render home template with user session data."""
    return render_template("home_page.html", session=session.get("user"),
                           pretty=json.dumps(session.get("user"),
                                             indent=4))  # Render home_page.html template with user session data


# Google login route
@app.route("/google-login")  # Define route for Google login
def googleLogin():
    """Redirect to the Google OAuth authorization endpoint."""
    return oauth.myApp.authorize_redirect(
        redirect_uri=url_for("googleCallback", _external=True))  # Redirect to Google OAuth authorization endpoint


# Callback route after successful Google login
@app.route("/sign-google")  # Define route for Google OAuth callback
def googleCallback():
    """Callback route after successful Google OAuth login."""
    # Authorizing access token from Google
    token = oauth.myApp.authorize_access_token()

    # Requesting user data from Google People API
    personDataUrl = "https://people.googleapis.com/v1/people/me?personFields=genders,birthdays"
    personData = requests.get(
        personDataUrl,
        headers={
            "Authorization": f"Bearer {token['access_token']}"
        }
    ).json()

    # Adding user data to session
    token["personData"] = personData
    session["user"] = token

    # Redirecting back to home page
    return redirect(url_for("home"))


# Logout route
@app.route("/logout")  # Define route for logout
def logout():
    """Logout route: Clear user session data."""
    session.pop("user", None)  # Clear user session data

    # Redirecting back to home page
    return redirect(url_for("home"))


if __name__ == "__main__":
    # Open the application in Chrome
    webbrowser.open("http://127.0.0.1:5000", new=2)  # Adjust the URL as needed
    app.run(debug=True)