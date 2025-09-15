from flask import Flask, render_template, request
import os
from pipeline import process_file_text

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
@app.route("/")
def index():
    return render_template("index.html")
@app.route("/analyze", methods=["POST"])
def analyze():
    selected_job = request.form.get("job_title")
    if "resume_file" not in request.files:
        return "No file part"
    file = request.files["resume_file"]
    if not file or file.filename == "":
        return "No file selected"
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)  # Save uploaded file
    results = process_file_text(filepath,selected_job)
    if not results:
        return "Could not extract resume text or no skills found." 
    if results:
        print(results)
    return render_template("results.html", results=results)
@app.route("/about")
def about():
    return render_template("about.html")

if __name__ == "__main__":
    app.run(debug=True)
