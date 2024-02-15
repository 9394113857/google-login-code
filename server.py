from flask import Flask, url_for, session, render_template, redirect
from authlib.integrations.flask_client import OAuth
import json
import requests

app = Flask(__name__)

# Configuration settings
appConf = {
    "OAUTH2_CLIENT_ID": "152013327427-d9e1jo2els3buk8l8t59ic1v8rv2icnv.apps.googleusercontent.com",
    "OAUTH2_CLIENT_SECRET": "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",
    "OAUTH2_META_URL": "https://accounts.google.com/.well-known/openid-configuration",
    "FLASK_SECRET": "c17846ff-178c-42e5-a316-483b7d05ba00",
    "FLASK_PORT": 5000
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
@app.route("/")
def home():
    """Render home template with user session data."""
    return render_template("home.html", session=session.get("user"),
                           pretty=json.dumps(session.get("user"), indent=4))

# Google login route
@app.route("/google-login")
def googleLogin():
    """Redirect to the Google OAuth authorization endpoint."""
    return oauth.myApp.authorize_redirect(redirect_uri=url_for("googleCallback", _external=True))

# Callback route after successful Google login
@app.route("/sign-google")
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
@app.route("/logout")
def logout():
    """Logout route: Clear user session data."""
    session.pop("user", None)
    
    # Redirecting back to home page
    return redirect(url_for("home"))

# Running the Flask application
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
