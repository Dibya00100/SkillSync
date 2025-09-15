"""
Advanced NLP Processing Module for SkillSync
Provides comprehensive text analysis, skill extraction, and semantic matching
"""

import re
import nltk
import numpy as np
import pandas as pd
from typing import List, Dict, Tuple, Any
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from textblob import TextBlob
from collections import Counter
import warnings
warnings.filterwarnings('ignore')

# Download required NLTK data
try:
    nltk.download('punkt', quiet=True)
    nltk.download('stopwords', quiet=True)
    nltk.download('averaged_perceptron_tagger', quiet=True)
    nltk.download('wordnet', quiet=True)
except:
    pass

class NLPProcessor:
    def __init__(self):
        """Initialize NLP models and processors"""
        self.nlp = None
        self.sentence_model = None
        self.skill_keywords = self._load_skill_keywords()
        self.stop_words = set(nltk.corpus.stopwords.words('english'))
        self.tfidf_vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')
        
        # Initialize models (lazy loading)
        self._initialize_models()
    
    def _initialize_models(self):
        """Initialize NLP models"""
        print("NLP models initialized (using simplified version)")
        # For now, we'll use TF-IDF based similarity instead of sentence transformers
        self.nlp = None
        self.sentence_model = None
    
    def _load_skill_keywords(self) -> Dict[str, List[str]]:
        """Load comprehensive skill keywords database"""
        return {
            'programming_languages': [
                'python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'c', 'go', 'rust', 'kotlin',
                'swift', 'php', 'ruby', 'scala', 'r', 'matlab', 'perl', 'haskell', 'clojure', 'erlang',
                'dart', 'lua', 'assembly', 'bash', 'powershell', 'sql', 'html', 'css', 'scss', 'sass'
            ],
            'frameworks_libraries': [
                'react', 'angular', 'vue', 'node.js', 'express', 'django', 'flask', 'fastapi', 'spring',
                'laravel', 'symfony', 'rails', 'asp.net', 'jquery', 'bootstrap', 'tailwind', 'material-ui',
                'tensorflow', 'pytorch', 'keras', 'scikit-learn', 'pandas', 'numpy', 'matplotlib', 'seaborn',
                'd3.js', 'three.js', 'webpack', 'babel', 'gulp', 'grunt', 'jest', 'cypress', 'selenium'
            ],
            'databases': [
                'mysql', 'postgresql', 'mongodb', 'redis', 'elasticsearch', 'cassandra', 'dynamodb',
                'sqlite', 'oracle', 'sql server', 'mariadb', 'neo4j', 'influxdb', 'couchdb', 'firebase'
            ],
            'cloud_platforms': [
                'aws', 'azure', 'gcp', 'google cloud', 'amazon web services', 'microsoft azure',
                'heroku', 'digitalocean', 'linode', 'vultr', 'cloudflare', 'vercel', 'netlify'
            ],
            'devops_tools': [
                'docker', 'kubernetes', 'jenkins', 'gitlab ci', 'github actions', 'travis ci',
                'circleci', 'terraform', 'ansible', 'chef', 'puppet', 'vagrant', 'prometheus',
                'grafana', 'elk stack', 'splunk', 'new relic', 'datadog'
            ],
            'data_science': [
                'machine learning', 'deep learning', 'artificial intelligence', 'ai', 'ml', 'dl',
                'data analysis', 'data visualization', 'statistics', 'probability', 'regression',
                'classification', 'clustering', 'neural networks', 'nlp', 'computer vision',
                'recommendation systems', 'time series', 'feature engineering', 'model deployment'
            ],
            'soft_skills': [
                'leadership', 'communication', 'teamwork', 'problem solving', 'critical thinking',
                'project management', 'agile', 'scrum', 'kanban', 'time management', 'mentoring',
                'collaboration', 'adaptability', 'creativity', 'analytical thinking', 'attention to detail'
            ]
        }
    
    def preprocess_text(self, text: str) -> str:
        """Clean and preprocess text"""
        if not text:
            return ""
        
        # Remove extra whitespace and normalize
        text = re.sub(r'\s+', ' ', text.strip())
        
        # Remove special characters but keep alphanumeric and basic punctuation
        text = re.sub(r'[^\w\s\.\,\!\?\;\:\-\(\)]', ' ', text)
        
        # Remove extra spaces
        text = re.sub(r'\s+', ' ', text)
        
        return text.strip()
    
    def extract_entities(self, text: str) -> Dict[str, List[str]]:
        """Extract named entities using spaCy"""
        if not self.nlp or not text:
            return {}
        
        doc = self.nlp(text)
        entities = {
            'PERSON': [],
            'ORG': [],
            'GPE': [],  # Geopolitical entities (countries, cities)
            'DATE': [],
            'MONEY': [],
            'PERCENT': [],
            'EMAIL': [],
            'PHONE': []
        }
        
        for ent in doc.ents:
            if ent.label_ in entities:
                entities[ent.label_].append(ent.text.strip())
        
        # Extract email and phone using regex
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        phone_pattern = r'\b(?:\+?1[-.\s]?)?\(?([0-9]{3})\)?[-.\s]?([0-9]{3})[-.\s]?([0-9]{4})\b'
        
        entities['EMAIL'] = re.findall(email_pattern, text)
        entities['PHONE'] = re.findall(phone_pattern, text)
        
        return {k: list(set(v)) for k, v in entities.items() if v}
    
    def extract_skills_advanced(self, text: str) -> Dict[str, List[str]]:
        """Advanced skill extraction using multiple methods"""
        if not text:
            return {}
        
        text_lower = text.lower()
        extracted_skills = {
            'programming_languages': [],
            'frameworks_libraries': [],
            'databases': [],
            'cloud_platforms': [],
            'devops_tools': [],
            'data_science': [],
            'soft_skills': []
        }
        
        # Method 1: Keyword matching
        for category, skills in self.skill_keywords.items():
            for skill in skills:
                if skill.lower() in text_lower:
                    extracted_skills[category].append(skill.title())
        
        # Method 2: spaCy NER for technical terms
        if self.nlp:
            doc = self.nlp(text)
            for token in doc:
                if token.pos_ in ['NOUN', 'PROPN'] and not token.is_stop:
                    token_text = token.text.lower()
                    # Check if it's a technical term
                    for category, skills in self.skill_keywords.items():
                        if any(skill in token_text for skill in skills):
                            if token.text.title() not in extracted_skills[category]:
                                extracted_skills[category].append(token.text.title())
        
        # Method 3: Pattern-based extraction
        patterns = {
            'programming_languages': r'\b(python|java|javascript|typescript|c\+\+|c#|go|rust|kotlin|swift|php|ruby|scala|r|matlab|perl|haskell|clojure|erlang|dart|lua|assembly|bash|powershell|sql|html|css|scss|sass)\b',
            'databases': r'\b(mysql|postgresql|mongodb|redis|elasticsearch|cassandra|dynamodb|sqlite|oracle|sql server|mariadb|neo4j|influxdb|couchdb|firebase)\b',
            'cloud_platforms': r'\b(aws|azure|gcp|google cloud|amazon web services|microsoft azure|heroku|digitalocean|linode|vultr|cloudflare|vercel|netlify)\b'
        }
        
        for category, pattern in patterns.items():
            matches = re.findall(pattern, text_lower, re.IGNORECASE)
            for match in matches:
                if match.title() not in extracted_skills[category]:
                    extracted_skills[category].append(match.title())
        
        # Remove duplicates and empty categories
        return {k: list(set(v)) for k, v in extracted_skills.items() if v}
    
    def calculate_semantic_similarity(self, text1: str, text2: str) -> float:
        """Calculate semantic similarity between two texts using TF-IDF"""
        if not text1 or not text2:
            return 0.0
        
        try:
            # Use TF-IDF for similarity calculation
            tfidf_matrix = self.tfidf_vectorizer.fit_transform([text1, text2])
            similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
            
            return float(similarity)
        except Exception as e:
            print(f"Error calculating semantic similarity: {e}")
            return 0.0
    
    def extract_keywords(self, text: str, top_k: int = 10) -> List[Tuple[str, float]]:
        """Extract top keywords using TF-IDF approach"""
        if not text:
            return []
        
        # Simple keyword extraction using frequency
        words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
        words = [word for word in words if word not in self.stop_words]
        
        word_freq = Counter(words)
        total_words = len(words)
        
        # Calculate TF scores
        keywords = [(word, freq/total_words) for word, freq in word_freq.most_common(top_k)]
        
        return keywords
    
    def analyze_sentiment(self, text: str) -> Dict[str, Any]:
        """Analyze sentiment of text"""
        if not text:
            return {'polarity': 0.0, 'subjectivity': 0.0, 'sentiment': 'neutral'}
        
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity
        subjectivity = blob.sentiment.subjectivity
        
        # Determine sentiment label
        if polarity > 0.1:
            sentiment = 'positive'
        elif polarity < -0.1:
            sentiment = 'negative'
        else:
            sentiment = 'neutral'
        
        return {
            'polarity': round(polarity, 3),
            'subjectivity': round(subjectivity, 3),
            'sentiment': sentiment
        }
    
    def extract_experience_info(self, text: str) -> Dict[str, Any]:
        """Extract experience-related information"""
        if not text:
            return {}
        
        # Extract years of experience
        years_pattern = r'(\d+)\+?\s*(?:years?|yrs?)\s*(?:of\s*)?(?:experience|exp)'
        years_match = re.search(years_pattern, text.lower())
        years_experience = int(years_match.group(1)) if years_match else None
        
        # Extract job titles
        title_patterns = [
            r'(?:senior|sr\.?|lead|principal|staff|architect)\s+([a-z\s]+(?:engineer|developer|analyst|manager|director|specialist))',
            r'([a-z\s]+(?:engineer|developer|analyst|manager|director|specialist|scientist|consultant))',
            r'(?:junior|jr\.?|entry|associate)\s+([a-z\s]+(?:engineer|developer|analyst))'
        ]
        
        job_titles = []
        for pattern in title_patterns:
            matches = re.findall(pattern, text.lower())
            job_titles.extend([match.title() for match in matches])
        
        return {
            'years_experience': years_experience,
            'job_titles': list(set(job_titles)),
            'seniority_level': self._determine_seniority_level(text, years_experience)
        }
    
    def _determine_seniority_level(self, text: str, years: int = None) -> str:
        """Determine seniority level based on text and years"""
        text_lower = text.lower()
        
        if any(word in text_lower for word in ['senior', 'sr.', 'lead', 'principal', 'staff', 'architect']):
            return 'senior'
        elif any(word in text_lower for word in ['junior', 'jr.', 'entry', 'associate']):
            return 'junior'
        elif years:
            if years >= 5:
                return 'senior'
            elif years >= 2:
                return 'mid'
            else:
                return 'junior'
        else:
            return 'mid'
    
    def generate_ats_optimization_suggestions(self, resume_text: str, jd_text: str) -> Dict[str, Any]:
        """Generate ATS optimization suggestions"""
        if not resume_text or not jd_text:
            return {}
        
        # Extract skills from both documents
        resume_skills = self.extract_skills_advanced(resume_text)
        jd_skills = self.extract_skills_advanced(jd_text)
        
        # Flatten skill lists for comparison
        resume_skills_flat = []
        jd_skills_flat = []
        
        for category, skills in resume_skills.items():
            resume_skills_flat.extend(skills)
        
        for category, skills in jd_skills.items():
            jd_skills_flat.extend(skills)
        
        # Find missing skills
        resume_skills_lower = [skill.lower() for skill in resume_skills_flat]
        missing_skills = [skill for skill in jd_skills_flat if skill.lower() not in resume_skills_lower]
        
        # Generate suggestions
        suggestions = {
            'missing_skills': missing_skills[:10],  # Top 10 missing skills
            'skill_coverage': len(set(resume_skills_lower) & set([s.lower() for s in jd_skills_flat])) / len(jd_skills_flat) if jd_skills_flat else 0,
            'recommendations': self._generate_recommendations(missing_skills, resume_skills, jd_skills)
        }
        
        return suggestions
    
    def _generate_recommendations(self, missing_skills: List[str], resume_skills: Dict, jd_skills: Dict) -> List[str]:
        """Generate specific recommendations"""
        recommendations = []
        
        if missing_skills:
            recommendations.append(f"Consider adding these missing skills: {', '.join(missing_skills[:5])}")
        
        # Check for skill categories
        if 'programming_languages' in jd_skills and not resume_skills.get('programming_languages'):
            recommendations.append("Add programming languages section to highlight technical skills")
        
        if 'cloud_platforms' in jd_skills and not resume_skills.get('cloud_platforms'):
            recommendations.append("Include cloud platform experience (AWS, Azure, GCP)")
        
        if 'databases' in jd_skills and not resume_skills.get('databases'):
            recommendations.append("Add database technologies you've worked with")
        
        return recommendations
    
    def process_resume_advanced(self, text: str) -> Dict[str, Any]:
        """Advanced resume processing with comprehensive analysis"""
        if not text:
            return {}
        
        # Clean text
        cleaned_text = self.preprocess_text(text)
        
        # Extract all information
        entities = self.extract_entities(cleaned_text)
        skills = self.extract_skills_advanced(cleaned_text)
        keywords = self.extract_keywords(cleaned_text, 15)
        experience_info = self.extract_experience_info(cleaned_text)
        sentiment = self.analyze_sentiment(cleaned_text)
        
        return {
            'entities': entities,
            'skills': skills,
            'keywords': keywords,
            'experience_info': experience_info,
            'sentiment': sentiment,
            'text_length': len(cleaned_text),
            'word_count': len(cleaned_text.split())
        }
    
    def process_job_description_advanced(self, text: str) -> Dict[str, Any]:
        """Advanced job description processing"""
        if not text:
            return {}
        
        # Clean text
        cleaned_text = self.preprocess_text(text)
        
        # Extract all information
        entities = self.extract_entities(cleaned_text)
        skills = self.extract_skills_advanced(cleaned_text)
        keywords = self.extract_keywords(cleaned_text, 20)
        experience_info = self.extract_experience_info(cleaned_text)
        sentiment = self.analyze_sentiment(cleaned_text)
        
        # Extract sections
        sections = self._extract_jd_sections(cleaned_text)
        
        return {
            'entities': entities,
            'skills': skills,
            'keywords': keywords,
            'experience_info': experience_info,
            'sentiment': sentiment,
            'sections': sections,
            'text_length': len(cleaned_text),
            'word_count': len(cleaned_text.split())
        }
    
    def _extract_jd_sections(self, text: str) -> Dict[str, List[str]]:
        """Extract structured sections from job description"""
        sections = {
            'responsibilities': [],
            'requirements': [],
            'qualifications': [],
            'benefits': [],
            'company_info': []
        }
        
        lines = text.split('\n')
        current_section = None
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Detect section headers
            if any(keyword in line.lower() for keyword in ['responsibilities', 'duties', 'what you will do']):
                current_section = 'responsibilities'
            elif any(keyword in line.lower() for keyword in ['requirements', 'must have', 'required']):
                current_section = 'requirements'
            elif any(keyword in line.lower() for keyword in ['qualifications', 'preferred', 'nice to have']):
                current_section = 'qualifications'
            elif any(keyword in line.lower() for keyword in ['benefits', 'perks', 'compensation']):
                current_section = 'benefits'
            elif any(keyword in line.lower() for keyword in ['about us', 'company', 'our mission']):
                current_section = 'company_info'
            elif current_section and line:
                sections[current_section].append(line)
        
        return {k: v for k, v in sections.items() if v}
