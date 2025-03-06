import os
from flask import Flask, render_template, request, redirect, url_for, session, flash
import subprocess
import requests
from decouple import config
from utilsAPI import get_api_url

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for session management

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

API_URL = get_api_url()

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/home')
def home():
    if 'token' not in session:
        return redirect(url_for('login'))
    return render_template("index.html")

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/resources')
def resources():
    return render_template("resources.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if not username or not password:
            return render_template("login.html", error="Please enter both username and password.")

        try:
            token = get_token(username, password)
            if token:
                session['token'] = token  # Store token in session
                return redirect(url_for('home'))
        except Exception:
            return render_template("login.html", error="Login failed: incorrect username or password.")

    return render_template("login.html")

@app.route('/logout')
def logout():
    session.pop('token', None)  # Remove token from session
    return redirect(url_for('login'))

@app.route('/process-files', methods=['POST'])
def process_files():
    if 'token' not in session:
        return redirect(url_for('login'))

    session_url = request.form.get('session_url')
    trial_name = request.form.get('trial_name')
    angle_name = request.form.get('angle_name')

    if not session_url or session_url.strip() == '':
        return render_template("index.html", error="Please enter a valid session URL.")
    
    if not trial_name or trial_name.strip() == '':
        return render_template("index.html", error="Please enter a trial name.")
    
    if not angle_name or angle_name.strip() == '':
        return render_template("index.html", error="Please select an angle name.")
    
    try:
        # Download session data
        subprocess.run([
            'python', 'BatchDownload.py',
            session_url.strip(),
            session['token']  # Pass token to the script
        ], check=True)

        # Run OpenSim processing
        subprocess.run([
            'python', 'runOpensim.py',
            session_url.strip().split('/')[-1],  # Extract session ID from URL
            trial_name.strip()  # Pass trial name to runOpensim
        ], check=True)

        # Convert .mot to .csv
        subprocess.run([
            'python', 'motCoverter.py',
            session_url.strip().split('/')[-1],  # Extract session ID from URL
            trial_name.strip()  # Pass trial name to convertCSV
        ], check=True)

        # Plot the angle
        subprocess.run([
            'python', 'plotAngle.py',
            session_url.strip().split('/')[-1],  # Extract session ID from URL
            trial_name.strip(),  # Pass trial name to plotAngle
            angle_name.strip()  # Pass angle name to plotAngle
        ], check=True)

        return render_template("index.html", success="Files downloaded and processed successfully!")
    except subprocess.CalledProcessError as e:
        return render_template("index.html", error=f"There was an error processing the session URL: {str(e)}")

def get_token(username, password):
    try:
        data = {"username": username, "password": password}
        resp = requests.post(API_URL + 'login/', data=data)
        resp.raise_for_status()
        token = resp.json().get('token')

        if not token:
            raise Exception("No token received from the API.")
        
        return token
    except requests.exceptions.RequestException:
        raise Exception("Login failed: incorrect username or password.")

if __name__ == "__main__":
    app.run(debug=True)