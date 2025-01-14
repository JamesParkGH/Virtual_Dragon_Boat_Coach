import os
from flask import Flask, render_template, request
import subprocess

app = Flask(__name__)

# Ensure the upload folder exists
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Allowed file extensions
ALLOWED_EXTENSIONS = {'osim', 'trc', 'mot'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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
    model = request.files.get('model')
    marker_data = request.files.get('marker_data')
    motion = request.files.get('motion')

    if not model or model.filename == '':
        return render_template("index.html", error="Please upload a model file (.osim).")
    if not marker_data or marker_data.filename == '':
        return render_template("index.html", error="Please upload a marker data file (.trc).")
    if not motion or motion.filename == '':
        return render_template("index.html", error="Please upload a motion file (.mot).")
    
    # Save the uploaded files
    model_path = os.path.join(app.config['UPLOAD_FOLDER'], model.filename)
    marker_data_path = os.path.join(app.config['UPLOAD_FOLDER'], marker_data.filename)
    motion_path = os.path.join(app.config['UPLOAD_FOLDER'], motion.filename)
    
    model.save(model_path)
    marker_data.save(marker_data_path)
    motion.save(motion_path)

    # Run the OpenSim processing script with the uploaded files
    try:
        # Call the script via subprocess
        subprocess.run([
            'python', 'runOpensim.py',
            model_path,
            marker_data_path,
            motion_path
        ], check=True)

        return render_template("index.html", success="Files uploaded and processed successfully!")
    except subprocess.CalledProcessError as e:
        return render_template("index.html", error="There was an error processing the files.")

if __name__ == "__main__":
    app.run(debug=True)
