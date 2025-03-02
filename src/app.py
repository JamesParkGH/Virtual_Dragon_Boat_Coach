import os
from flask import Flask, render_template, request, redirect, url_for, session, flash
import subprocess
import requests
import json
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

@app.route('/coach', methods=['GET', 'POST'])
def coach():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        credentials = load_credentials()

        if username in credentials and credentials[username] == password:
            session['coach'] = username
            return redirect(url_for('coach_dashboard'))
        else:
            return render_template('coach.html', error="Invalid username or password")

    return render_template('coach.html')

@app.route('/coach/dashboard')
def coach_dashboard():
    if 'coach' not in session:
        return redirect(url_for('coach_login'))

    base_dir = os.path.dirname(os.path.abspath(__file__))
    all_sessions_file = os.path.join(base_dir, "sessions.json")
    with open(all_sessions_file,'r+') as file:
        all_sessions = json.load(file)
    return render_template('coach_dash.html', coach=session['coach'])

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
    session.pop('coach', None)
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
            'python', 'convertCSV.py',
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

        save_sessions(session_url,trial_name)

        return render_template("index.html", success="Files downloaded and processed successfully!")
    except subprocess.CalledProcessError as e:
        return render_template("index.html", error=f"There was an error processing the session URL: {str(e)}")

@app.route('/feedbacks')
def feedbacks():
    if 'token' not in session:
        return redirect(url_for('login'))
    
    image_file = ""

    text_feedback = ""

    return render_template('feedback.html')

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

def load_credentials():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    credentials_file = os.path.join(base_dir, "credentials.txt")
    creds = {}
    if os.path.exists(credentials_file):
        with open(credentials_file, "r") as file:
            for line in file:
                username, password = line.strip().split(",")
                creds[username] = password
    return creds

def save_sessions(URL, trial_name):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    new_session = {URL: trial_name}
    all_sessions_file = os.path.join(base_dir, "sessions.json")
    with open(all_sessions_file,'r+') as file:
        existing_sessions = json.load(file)  
        existing_sessions.update(new_session)
        file.seek(0)
        json.dump(existing_sessions, file, indent=4)

    return
    
if __name__ == "__main__":
    app.run(debug=True)