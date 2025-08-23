from flask import  Flask, request, jsonify
from parser import parse_resume
from parser_jd import parse_jd
from mather import calculate_match
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

@app.route("/parse_jd", methods=["POST"])
def upload_jd():
    if "file" in request.files:  # handle file upload
        file = request.files["file"]
        text = file.read().decode("utf-8")
    else:  # handle JSON input
        data = request.get_json()
        if not data or "jd_text" not in data:
            return jsonify({"error": "No JD text provided"}), 400
        text = data["jd_text"]

    parsed_data = parse_jd(text)
    return jsonify(parsed_data)

@app.route('/match_skill', methods=['POST'])
def match_resume_jd():
    data = request.get_json()
    if not data or 'resume' not in data or 'jd' not in data:
        return jsonify({"error": "Both resume and jd is required"}), 400
    result = calculate_match(data["resume"], data["jd"])
    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True, port=5000)