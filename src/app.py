import os
from flask import Flask, render_template, request
import subprocess

app = Flask(__name__)

# Ensure the upload folder exists
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
@app.route('/home')
def home():
    return render_template("index.html")

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/resources')
def resources():
    return render_template("resources.html")

@app.route('/process-files', methods=['POST'])
def process_files():
    session_url = request.form.get('session_url')

    if not session_url or session_url.strip() == '':
        return render_template("index.html", error="Please enter a valid session URL.")
    
    # Save session URL to a file or pass it to the script
    try:
        # Call the batchDownload.py script with the session URL
        subprocess.run([
            'python', 'batchDownload.py',
            session_url.strip()
        ], check=True)

        return render_template("index.html", success="Files downloaded and processed successfully!")
    except subprocess.CalledProcessError as e:
        return render_template("index.html", error="There was an error processing the session URL.")

if __name__ == "__main__":
    app.run(debug=True)
