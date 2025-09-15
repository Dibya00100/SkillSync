
# SkillSync 🚀

**AI-Powered Resume & Job Matcher with Advanced NLP**

SkillSync is a comprehensive platform that uses cutting-edge Natural Language Processing to help job seekers optimize their resumes and match them with job descriptions. Upload your resume and job posting to get detailed analysis, semantic matching, and ATS optimization suggestions.

## ✨ Features

### 🧠 AI-Enhanced Matching
- **Semantic Analysis**: Uses sentence transformers for deep text understanding
- **Multi-factor Scoring**: Combines skill, semantic, experience, and keyword matching
- **Detailed Breakdown**: See exactly how your resume matches job requirements
- **Smart Recommendations**: Get actionable advice for improvement

### 📊 Advanced Analytics
- **Named Entity Recognition**: Extracts names, organizations, locations, dates
- **Skill Categorization**: Automatically categorizes skills (programming, frameworks, databases, etc.)
- **Experience Analysis**: Determines seniority level and years of experience
- **Sentiment Analysis**: Analyzes job description tone and culture

### 🎯 ATS Optimization
- **Missing Skills Detection**: Identifies skills you should add
- **Keyword Optimization**: Suggests relevant keywords to include
- **Coverage Analysis**: Shows how well your resume covers job requirements
- **Actionable Suggestions**: Specific recommendations for improvement

### 📱 Modern UI
- **Tabbed Interface**: Switch between Basic, AI Enhanced, and ATS Optimization
- **Dark Mode**: Beautiful dark theme support
- **Responsive Design**: Works on desktop and mobile
- **Real-time Analysis**: Instant results with loading indicators

## 🛠 Tech Stack

### Backend
- **Flask**: Web framework
- **spaCy**: Advanced NLP processing
- **Transformers**: Hugging Face models for semantic analysis
- **Sentence Transformers**: Text similarity and embeddings
- **scikit-learn**: Machine learning utilities
- **NLTK**: Natural language toolkit
- **TextBlob**: Sentiment analysis

### Frontend
- **React**: Modern UI framework
- **Axios**: HTTP client
- **React Icons**: Beautiful icons
- **CSS3**: Advanced styling with gradients and animations

### File Processing
- **pdfplumber**: PDF text extraction
- **python-docx**: Word document processing
- **PyMuPDF**: Alternative PDF processing

## 🚀 Quick Start

### 1. Setup Environment
```bash
# Clone the repository
git clone <repository-url>
cd SkillSync

# Install Python dependencies
pip install -r requirements.txt

# Run NLP setup (downloads models)
python setup_nlp.py
```

### 2. Start Backend
```bash
cd backend
python app.py
```
Backend runs on `http://localhost:5000`

### 3. Start Frontend
```bash
cd frontend
npm install
npm start
```
Frontend runs on `http://localhost:3000`

## 📋 API Endpoints

### Core Endpoints
- `POST /parse_resume` - Parse resume file (PDF/DOCX)
- `POST /parse_jd` - Parse job description (file or text)
- `POST /match` - Basic skill matching
- `POST /enhanced_match` - AI-enhanced comprehensive matching
- `POST /optimize_resume` - Generate ATS optimization suggestions
- `POST /analyze_text` - General text analysis
- `GET /health` - Health check

### Example Usage
```python
# Enhanced matching
import requests

response = requests.post('http://localhost:5000/enhanced_match', json={
    'resume': resume_data,
    'jd': job_description_data
})

result = response.json()
print(f"Overall Score: {result['overall_score']}%")
print(f"Semantic Match: {result['semantic_match']['score']}%")
```

## 🧪 NLP Features Explained

### 1. Semantic Matching
Uses sentence transformers to understand the meaning behind text, not just keywords. This helps match resumes even when different terminology is used.

### 2. Skill Extraction
Advanced skill recognition that goes beyond simple keyword matching:
- Categorizes skills by type (programming, frameworks, databases, etc.)
- Uses NLP patterns to identify technical terms
- Handles variations and synonyms

### 3. Experience Analysis
Automatically extracts:
- Years of experience from text
- Job titles and seniority levels
- Career progression patterns

### 4. ATS Optimization
Generates specific suggestions for:
- Missing skills to add
- Keywords to include
- Resume structure improvements
- ATS-friendly formatting tips

## 📊 Sample Output

### Enhanced Match Result
```json
{
  "overall_score": 78.5,
  "skill_match": {
    "score": 85.0,
    "matched_skills": ["Python", "Machine Learning", "SQL"],
    "missing_skills": ["Docker", "Kubernetes"],
    "extra_skills": ["JavaScript", "React"]
  },
  "semantic_match": {
    "score": 72.3,
    "similarity": 0.723,
    "interpretation": "Good semantic match - relevant"
  },
  "experience_match": {
    "score": 90.0,
    "match": "meets_requirements"
  },
  "analysis": {
    "strengths": ["Strong skill alignment", "Experience level adequate"],
    "weaknesses": ["Missing DevOps skills"],
    "recommendations": ["Consider gaining Docker experience"]
  }
}
```

## 🔧 Configuration

### NLP Models
The system uses these pre-trained models:
- **spaCy**: `en_core_web_sm` for NER and text processing
- **Sentence Transformers**: `all-MiniLM-L6-v2` for semantic similarity

### Customization
You can modify skill keywords in `backend/nlp_processor.py`:
```python
self.skill_keywords = {
    'programming_languages': ['python', 'java', 'javascript', ...],
    'frameworks_libraries': ['react', 'django', 'spring', ...],
    # Add your own categories
}
```

## 🐛 Troubleshooting

### Common Issues

1. **spaCy model not found**
   ```bash
   python -m spacy download en_core_web_sm
   ```

2. **Sentence transformer slow first run**
   - Models are downloaded on first use
   - Subsequent runs will be faster

3. **Memory issues with large files**
   - Process resumes in chunks
   - Consider using smaller models for production

### Performance Tips
- Use SSD storage for faster model loading
- Consider GPU acceleration for sentence transformers
- Implement caching for repeated analyses

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add your improvements
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- spaCy team for excellent NLP library
- Hugging Face for transformer models
- React team for the frontend framework
- All contributors and testers

---

**Made with ❤️ for job seekers everywhere**