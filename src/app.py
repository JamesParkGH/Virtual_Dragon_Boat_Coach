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

@app.route('/start-analyze', methods=['POST'])
def start_analyze():
    if 'token' not in session:
        return redirect(url_for('login'))

    session_url = request.form.get('session_url')
    trial_name = request.form.get('trial_name')

    if not session_url or session_url.strip() == '':
        return render_template("index.html", error="Please enter a valid session URL.")
    
    if not trial_name or trial_name.strip() == '':
        return render_template("index.html", error="Please enter a trial name.")
    
    try:
        # Download session data
        subprocess.run([
            'python', 'batchDownload.py',
            session_url.strip(),
            session['token']  # Pass token to the script
        ], check=True)

        # Store session_id and trial_name in session
        session['session_id'] = session_url.strip().split('/')[-1]  # Assuming session_id is part of the URL
        session['trial_name'] = trial_name.strip()

        subprocess.run([
            'python', 'motConverter.py',
            session_url.strip().split('/')[-1],  # Extract session ID from URL
            trial_name.strip()  # Pass trial name to convertCSV
        ], check=True)

        subprocess.run([
            'python', 'trcConverter.py',
            session_url.strip().split('/')[-1],  # Extract session ID from URL
            trial_name.strip()  # Pass trial name to trcConverter
        ], check=True)

        # Define file paths for techniqueAnalyzer
        data_folder = os.path.join(os.getcwd(), 'Data', f'OpenCapData_{session["session_id"]}')
        mot_file_path = os.path.join(data_folder, 'OpenSimData', 'Kinematics', f'{trial_name}.csv')
        trc_file_path = os.path.join(data_folder, 'MarkerData', f'{trial_name}.csv')

        # Run technique analysis and capture the output
        result = subprocess.run([
            'python', 'techniqueAnalyzer.py',
            trc_file_path,
            mot_file_path
        ], check=True, capture_output=True, text=True)

        # Store the analysis result in the session
        session['analysis_result'] = result.stdout.strip()

        return redirect(url_for('feedback'))
    except subprocess.CalledProcessError as e:
        return render_template("index.html", error=f"There was an error processing the session URL: {str(e)}")

@app.route('/feedback')
def feedback():
    if 'token' not in session:
        return redirect(url_for('login'))

    # Read the analysis result from the session
    analysis_result = session.get('analysis_result', '')

    return render_template("feedback.html", analysis_result=analysis_result)

@app.route('/generate-graph', methods=['POST'])
def generate_graph():
    if 'token' not in session:
        return redirect(url_for('login'))

    angle_name = request.form.get('angle_name')

    if not angle_name or angle_name.strip() == '':
        return render_template("feedback.html", error="Please select an angle name.")
    
    try:
        # Plot the angle
        subprocess.run([
            'python', 'plotAngle.py',
            session['session_id'],  # Use session ID stored in session
            session['trial_name'],  # Use trial name stored in session
            angle_name.strip()  # Pass angle name to plotAngle
        ], check=True)
    except subprocess.CalledProcessError as e:
        return render_template("feedback.html", error=f"There was an error generating the graph: {str(e)}")

    return redirect(url_for('feedback'))

@app.route('/run-opensim', methods=['POST'])
def run_opensim():
    if 'token' not in session:
        return redirect(url_for('login'))

    try:
        # Run OpenSim processing
        subprocess.run([
            'python', 'runOpensim.py',
            session['session_id'],  # Use session ID stored in session
            session['trial_name']  # Use trial name stored in session
        ], check=True)
    except subprocess.CalledProcessError as e:
        flash(f"There was an error running OpenSim: {str(e)}")

    return redirect(url_for('feedback'))

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