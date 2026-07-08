from flask import Flask, render_template, request
import os
import uuid
from werkzeug.utils import secure_filename
from pipeline import process_file_text

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

ALLOWED_EXTENSIONS = {"pdf", "png", "jpg", "jpeg"}
app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024  # 5MB limit


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():
    selected_job = request.form.get("job_title")

    if "resume_file" not in request.files:
        return "No file part", 400

    file = request.files["resume_file"]
    if not file or file.filename == "":
        return "No file selected", 400

    if not allowed_file(file.filename):
        return "Unsupported file type. Please upload a PDF, PNG, or JPG.", 400

    # secure + unique filename to prevent path traversal and collisions
    filename = secure_filename(file.filename)
    unique_name = f"{uuid.uuid4().hex}_{filename}"
    filepath = os.path.join(UPLOAD_FOLDER, unique_name)
    file.save(filepath)

    try:
        results = process_file_text(filepath, selected_job)
    except Exception as e:
        print(f"Error processing {filepath}: {e}")
        return "Something went wrong processing your resume. Please try a different file.", 500
    finally:
        # delete the uploaded file right after processing — don't retain user documents
        if os.path.exists(filepath):
            os.remove(filepath)

    if not results:
        return "Could not extract resume text or no skills found."

    return render_template("results.html", results=results)


@app.route("/about")
def about():
    return render_template("about.html")


if __name__ == "__main__":
    app.run(debug=False)