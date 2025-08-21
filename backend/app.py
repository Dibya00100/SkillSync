from flask import  Flask, request, jsonify
from werkzeug.http import parse_date

from parser import parse_resume

app = Flask(__name__)

@app.route("/parse_resume", methods=["POST"])
def upload_resume():
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files["file"]
    filename = file.filename

    #save temp file
    filepath = f"temp_{filename}"
    file.save(filepath)

    #Parse resume
    parse_data = parse_resume(filepath)
    return jsonify(parse_data)

if __name__ == "__main__":
    app.run(debug=True, port=5000)