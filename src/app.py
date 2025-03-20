import os
import re
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, session, flash
import subprocess
import requests
import ast
from decouple import config
from utilsAPI import get_api_url
from feedbackCompiler import compile_feedback
import smtplib

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required for session management

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'vdbc.db')

def init_db():
    """Initialize the database with minimal tables."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Create a simple table for shared data
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS shared_sessions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        session_url TEXT NOT NULL,
        trial_name TEXT NOT NULL,
        coach_feedback TEXT
    )
    ''')
    
    conn.commit()
    conn.close()

# Call this function when the app starts
init_db()

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
                session['username'] = username  # Store username in session
                return redirect(url_for('home'))
        except Exception:
            return render_template("login.html", error="Login failed: incorrect username or password.")

    return render_template("login.html")

@app.route('/coach-login', methods=['GET', 'POST'])
def coach_login():
    success = request.args.get('success')
    
    # Hardcoded coach credentials
    COACH_USERNAME = "coach"
    COACH_PASSWORD = "coach"
    
    if request.method == 'POST':
        vdbc_username = request.form.get('username')
        vdbc_password = request.form.get('password')

        if not vdbc_username or not vdbc_password:
            return render_template("coachLogin.html", error="Please enter both username and password.")

        if vdbc_username == COACH_USERNAME and vdbc_password == COACH_PASSWORD:
            session['token'] = "coach_token"  # Store a hardcoded token in session
            session['position'] = 'coach'  # Store user position in session
            return redirect(url_for('coach_dashboard'))
        else:
            return render_template("coachLogin.html", error="Login failed: This does not match coach credentials.")

    return render_template("coachLogin.html", success=success)

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
    username = session.get('username', 'Unknown')

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
        trc_file_path = os.path.join(data_folder, 'MarkerData', f'{trial_name}.csv')
        mot_file_path = os.path.join(data_folder, 'OpenSimData', 'Kinematics', f'{trial_name}.csv')

        # Run technique analysis and capture the output
        result = subprocess.run([
            'python', 'techniqueAnalyzer.py',
            trc_file_path,
            mot_file_path
        ], check=True, capture_output=True, text=True)

        # Store the analysis result in the session
        scores_str = result.stdout.strip()
        session['analysis_result'] = scores_str
        
        # Save the analysis results to a file for later access by coaches
        data_folder = os.path.join(os.getcwd(), 'Data', f'OpenCapData_{session["session_id"]}')
        analysis_folder = os.path.join(data_folder, 'Analysis')
        
        # Create the Analysis folder if it doesn't exist
        if not os.path.exists(analysis_folder):
            os.makedirs(analysis_folder)
            
        # Save the analysis results to a file
        with open(os.path.join(analysis_folder, f'{trial_name}_analysis.txt'), 'w') as file:
            file.write(scores_str)
        
        try:
            # Convert string representation of list to actual list
            scores = ast.literal_eval(scores_str)
            
            # Generate feedback based on scores
            feedback_data = compile_feedback(scores)
            session['feedback'] = feedback_data
        except Exception as e:
            flash(f"Warning: Could not generate feedback: {str(e)}")
        
        #save to database after analysis
        try:
            # Store in database
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()

            # Check if an entry already exists
            cursor.execute("""
                SELECT * FROM shared_sessions 
                WHERE username = ? AND session_url = ? AND trial_name = ?
            """, (username, session_url, trial_name))
            existing_entry = cursor.fetchone()
            
            if existing_entry:
                # Update the existing entry without touching the coach_feedback
                cursor.execute('''
                    UPDATE shared_sessions 
                    SET session_url = ?, trial_name = ?
                    WHERE username = ?
                ''', (session_url, trial_name, username))
            else:
                # Add a new entry
                cursor.execute('''
                    INSERT INTO shared_sessions (username, session_url, trial_name)
                    VALUES (?, ?, ?)
                ''', (username, session_url, trial_name))
            
            conn.commit()
            conn.close()
        except Exception as e:
            flash(f"Warning: Could not save session data: {str(e)}")

        return redirect(url_for('feedback'))
    except subprocess.CalledProcessError as e:
        return render_template("index.html", error=f"There was an error processing the session URL: {str(e)}")

@app.route('/coach-view-analysis', methods=['POST'])
def coach_view_analysis():
    if 'token' not in session or session.get('position') != 'coach':
        return redirect(url_for('coach_login'))
    
    # Get data from the form
    session_url = request.form.get('session_url')
    trial_name = request.form.get('trial_name')
    username = request.form.get('username')
    
    if not session_url or not trial_name:
        flash("Missing session URL or trial name")
        return redirect(url_for('coach_dashboard'))
    
    # Extract session ID from URL if it's a full URL
    session_id = session_url.split('/')[-1] if '/' in session_url else session_url
    
    try:
        # Connect to database to get any stored analysis results
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        # Query for this specific user and session
        cursor.execute('''
            SELECT * FROM shared_sessions 
            WHERE username = ? AND session_url = ? AND trial_name = ?
        ''', (username, session_url, trial_name))
        
        session_data = cursor.fetchone()
        conn.close()
        
        if not session_data:
            flash("Session data not found for this user")
            return redirect(url_for('coach_dashboard'))

        # Prepare details for coach feedback page
        analysis_details = {
            'username': username,
            'session_url': session_url,
            'trial_name': trial_name
        }
        
        # Set session variables that might be needed for the feedback template
        session['session_id'] = session_id
        session['trial_name'] = trial_name
        
        # Try to find previously generated analysis results
        try:
            # Look for analysis files based on session_id and trial_name
            data_folder = os.path.join(os.getcwd(), 'Data', f'OpenCapData_{session_id}')
            analysis_file = os.path.join(data_folder, 'Analysis', f'{trial_name}_analysis.txt')
            
            # If analysis file exists, read it
            if os.path.exists(analysis_file):
                with open(analysis_file, 'r') as file:
                    analysis_result = file.read()
                session['analysis_result'] = analysis_result
                
                # Generate feedback from the stored analysis
                try:
                    scores = ast.literal_eval(analysis_result)
                    feedback_data = compile_feedback(scores)
                    session['feedback'] = feedback_data
                except Exception as e:
                    flash(f"Could not generate feedback from stored analysis: {str(e)}")
            else:
                # If no saved analysis, inform the coach
                flash("No saved analysis found for this session. The paddler needs to re-run their analysis.")
                session['analysis_result'] = "No analysis data available"
                session['feedback'] = None
        except Exception as e:
            flash(f"Error retrieving analysis: {str(e)}")
            session['analysis_result'] = "Error retrieving analysis"
            session['feedback'] = None
        
        return render_template("coachFeedback.html", 
                              analysis_details=analysis_details,
                              analysis_result=session.get('analysis_result', ''), 
                              feedback=session.get('feedback'))
        
    except Exception as e:
        flash(f"Error loading session: {str(e)}")
        return redirect(url_for('coach_dashboard'))

        #  # Store in database
#     conn = sqlite3.connect(DB_PATH)
#     cursor = conn.cursor()

#     # Check if an entry already exists for the user
#     cursor.execute("SELECT * FROM shared_sessions WHERE username = ?", (username,))
#     existing_entry = cursor.fetchone()
    
#     if existing_entry:
#         # Update the existing entry
#         cursor.execute('''
#             UPDATE shared_sessions
#             SET session_url = ?, trial_name = ?, email = ?
#             WHERE username = ?
#         ''', (session_url, trial_name, email, username))
#     else:
#         # Add a new entry
#         cursor.execute('''
#             INSERT INTO shared_sessions (username, session_url, trial_name, email)
#             VALUES (?, ?, ?, ?)
#         ''', (username, session_url, trial_name, email))
    
#     conn.commit()
#     conn.close()

@app.route('/send-feedback', methods=['POST'])
def send_feedback():
    if 'token' not in session or session.get('position') != 'coach':
        return redirect(url_for('coach_login'))
    
    # Get form data
    username = request.form.get('recipient_username', '').strip()
    session_url = request.form.get('session_url', '').strip()
    trial_name = request.form.get('trial_name', '').strip()
    feedback = request.form.get('feedback', '').strip()
    
    if not username or not feedback or not session_url or not trial_name:
        flash("Missing required fields")
        return redirect(url_for('coach_dashboard'))
    
    success_message = None
    error_message = None
    
    try:
        # Connect to database
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Update the record with coach's feedback
        cursor.execute('''
            UPDATE shared_sessions
            SET coach_feedback = ?
            WHERE username = ? AND session_url = ? AND trial_name = ?
        ''', (feedback, username, session_url, trial_name))
        
        conn.commit()
        success_message = f"Feedback saved successfully for {username}"
        conn.close()
        
    except Exception as e:
        error_message = f"Error saving feedback: {str(e)}"
    
    # Retrieve analysis details for rendering the page
    try:
        # Get session ID from URL
        session_id = session_url.split('/')[-1] if '/' in session_url else session_url
        
        # Set session variables for the template
        session['session_id'] = session_id
        session['trial_name'] = trial_name
        
        # Get analysis result
        data_folder = os.path.join(os.getcwd(), 'Data', f'OpenCapData_{session_id}')
        analysis_file = os.path.join(data_folder, 'Analysis', f'{trial_name}_analysis.txt')
        
        if os.path.exists(analysis_file):
            with open(analysis_file, 'r') as file:
                analysis_result = file.read()
                session['analysis_result'] = analysis_result
                
                scores = ast.literal_eval(analysis_result)
                feedback_data = compile_feedback(scores)
                session['feedback'] = feedback_data
        else:
            session['analysis_result'] = "No analysis data available"
            session['feedback'] = None
            
    except Exception as e:
        flash(f"Error retrieving analysis: {str(e)}")
    
    # Create analysis details for the template
    analysis_details = {
        'username': username,
        'session_url': session_url,
        'trial_name': trial_name
    }
    
    return render_template("coachFeedback.html", 
                          analysis_details=analysis_details,
                          analysis_result=session.get('analysis_result', ''), 
                          feedback=session.get('feedback'),
                          existing_feedback=feedback,
                          success_message=success_message,
                          error_message=error_message)

@app.route('/coach-dashboard')
def coach_dashboard():
    if 'token' not in session or session.get('position') != 'coach':
        return redirect(url_for('coach_login'))
    
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # This enables column access by name
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT username, session_url, trial_name
        FROM shared_sessions
    ''')
    
    shared_sessions = cursor.fetchall()
    conn.close()
    
    # Group sessions by username
    grouped_sessions = {}
    for session_data in shared_sessions:
        username = session_data['username']
        if username not in grouped_sessions:
            grouped_sessions[username] = []
        
        grouped_sessions[username].append({
            'session_url': session_data['session_url'],
            'trial_name': session_data['trial_name']
        })
    
    return render_template("coachDashboard.html", grouped_sessions=grouped_sessions)

@app.route('/clear-database', methods=['POST'])
def clear_database():
    if 'token' not in session or session.get('position') != 'coach':
        return redirect(url_for('coach_login'))
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Clear all entries from the shared_sessions table
    cursor.execute('DELETE FROM shared_sessions')
    
    conn.commit()
    conn.close()
    
    flash("Database cleared successfully.")
    return redirect(url_for('coach_dashboard'))

@app.route('/feedback')
def feedback():
    if 'token' not in session:
        return redirect(url_for('login'))
    
    # Read the analysis result from the session
    analysis_result = session.get('analysis_result', '')

    # Get the feedback from the session
    feedback_data = session.get('feedback', None)
    
    # Get current user and session info
    username = session.get('username', '')
    session_id = session.get('session_id', '')
    trial_name = session.get('trial_name', '')
    session_url = session.get('session_url')
    
    # Get the feedback from the session
    feedback_data = session.get('feedback', None)

    opencap_url = f"https://app.opencap.ai/session/{session_id}"

    # Check for coach feedback
    coach_feedback = None
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT coach_feedback FROM shared_sessions 
            WHERE username = ? AND session_url = ? AND trial_name = ?
        """, (username, session_url, trial_name))
        
        result = cursor.fetchone()
        if result and result['coach_feedback']:
            coach_feedback = result['coach_feedback']
            
        conn.close()
    except Exception as e:
        flash(f"Error retrieving coach feedback: {str(e)}")

    return render_template("feedback.html", 
                          analysis_result=analysis_result, 
                          feedback=feedback_data,
                          opencap_url=opencap_url,
                          coach_feedback=coach_feedback)
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
        
        # Add the graph to the session
        session['graph_filename'] = f"{session['trial_name']}_{angle_name.strip()}.png"
        
    except subprocess.CalledProcessError as e:
        return render_template("feedback.html", 
                              error=f"There was an error generating the graph: {str(e)}",
                              feedback=session.get('feedback', None),
                              analysis_result=session.get('analysis_result', ''))

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

def verify_vdbc_credentials(username, password):
    users = session.get('users', {})
    user = users.get(username)
    
    if user and user.get('vdbc_password') == password:
        return user
    
    return None

if __name__ == "__main__":
    app.run(debug=True)