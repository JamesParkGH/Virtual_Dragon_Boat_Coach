from flask import Flask, render_template, request

app = Flask(__name__)

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

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return render_template("index.html", error="No file selected")
    
    file = request.files['file']
    if file.filename == '':
        return render_template("index.html", error="No file selected")

    # Process the file (this is where you'd integrate analysis)
    filename = file.filename
    return render_template("index.html", success=f"File '{filename}' uploaded successfully!")

if __name__ == "__main__":
    app.run(debug=True)
