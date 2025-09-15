from flask import Flask, request, jsonify
from parser import parse_resume
from parser_jd import parse_jd
from mather import calculate_match
from enhanced_mather import EnhancedMatcher
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# Initialize enhanced matcher
enhanced_matcher = EnhancedMatcher()

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

@app.route('/match', methods=['POST'])
def match_resume_jd():
    data = request.get_json()
    if not data or 'resume' not in data or 'jd' not in data:
        return jsonify({"error": "Both resume and jd is required"}), 400
    result = calculate_match(data["resume"], data["jd"])
    return jsonify(result)

@app.route('/enhanced_match', methods=['POST'])
def enhanced_match_resume_jd():
    """Enhanced matching with NLP analysis"""
    data = request.get_json()
    if not data or 'resume' not in data or 'jd' not in data:
        return jsonify({"error": "Both resume and jd is required"}), 400
    
    try:
        result = enhanced_matcher.calculate_comprehensive_match(data["resume"], data["jd"])
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": f"Enhanced matching failed: {str(e)}"}), 500

@app.route('/analyze_text', methods=['POST'])
def analyze_text():
    """Analyze text with NLP"""
    data = request.get_json()
    if not data or 'text' not in data:
        return jsonify({"error": "Text is required"}), 400
    
    try:
        text = data['text']
        analysis_type = data.get('type', 'general')  # general, resume, jd
        
        if analysis_type == 'resume':
            result = enhanced_matcher.nlp_processor.process_resume_advanced(text)
        elif analysis_type == 'jd':
            result = enhanced_matcher.nlp_processor.process_job_description_advanced(text)
        else:
            # General analysis
            result = {
                'entities': enhanced_matcher.nlp_processor.extract_entities(text),
                'skills': enhanced_matcher.nlp_processor.extract_skills_advanced(text),
                'keywords': enhanced_matcher.nlp_processor.extract_keywords(text, 15),
                'sentiment': enhanced_matcher.nlp_processor.analyze_sentiment(text),
                'experience_info': enhanced_matcher.nlp_processor.extract_experience_info(text)
            }
        
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": f"Text analysis failed: {str(e)}"}), 500

@app.route('/optimize_resume', methods=['POST'])
def optimize_resume():
    """Generate ATS optimization suggestions"""
    data = request.get_json()
    if not data or 'resume' not in data or 'jd' not in data:
        return jsonify({"error": "Both resume and jd are required"}), 400
    
    try:
        resume_text = enhanced_matcher._extract_text_from_data(data['resume'])
        jd_text = enhanced_matcher._extract_text_from_data(data['jd'])
        
        suggestions = enhanced_matcher.nlp_processor.generate_ats_optimization_suggestions(resume_text, jd_text)
        return jsonify(suggestions)
    except Exception as e:
        return jsonify({"error": f"Optimization failed: {str(e)}"}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "nlp_processor": "available" if enhanced_matcher.nlp_processor.nlp else "unavailable",
        "sentence_model": "available" if enhanced_matcher.nlp_processor.sentence_model else "unavailable"
    })

if __name__ == "__main__":
    app.run(debug=True, port=5001)