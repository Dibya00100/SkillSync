"""
Enhanced Matching Algorithm with NLP Integration
Provides advanced resume-job matching with semantic analysis
"""

import numpy as np
from typing import Dict, List, Tuple, Any
from nlp_processor import NLPProcessor
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import warnings
warnings.filterwarnings('ignore')

class EnhancedMatcher:
    def __init__(self):
        """Initialize the enhanced matcher with NLP processor"""
        self.nlp_processor = NLPProcessor()
        self.tfidf_vectorizer = TfidfVectorizer(
            max_features=1000,
            stop_words='english',
            ngram_range=(1, 2)
        )
    
    def calculate_comprehensive_match(self, resume_data: Dict, jd_data: Dict) -> Dict[str, Any]:
        """Calculate comprehensive match score using multiple factors"""
        
        # Extract text data
        resume_text = self._extract_text_from_data(resume_data)
        jd_text = self._extract_text_from_data(jd_data)
        
        if not resume_text or not jd_text:
            return self._empty_result()
        
        # Calculate different types of matches
        skill_match = self._calculate_skill_match(resume_data, jd_data)
        semantic_match = self._calculate_semantic_match(resume_text, jd_text)
        experience_match = self._calculate_experience_match(resume_data, jd_data)
        keyword_match = self._calculate_keyword_match(resume_text, jd_text)
        
        # Calculate weighted overall score
        weights = {
            'skill': 0.35,
            'semantic': 0.25,
            'experience': 0.25,
            'keyword': 0.15
        }
        
        overall_score = (
            skill_match['score'] * weights['skill'] +
            semantic_match['score'] * weights['semantic'] +
            experience_match['score'] * weights['experience'] +
            keyword_match['score'] * weights['keyword']
        )
        
        # Generate detailed analysis
        analysis = self._generate_detailed_analysis(resume_data, jd_data, resume_text, jd_text)
        
        # Generate optimization suggestions
        suggestions = self.nlp_processor.generate_ats_optimization_suggestions(resume_text, jd_text)
        
        return {
            'overall_score': round(overall_score, 1),
            'skill_match': skill_match,
            'semantic_match': semantic_match,
            'experience_match': experience_match,
            'keyword_match': keyword_match,
            'analysis': analysis,
            'suggestions': suggestions,
            'weights': weights
        }
    
    def _extract_text_from_data(self, data: Dict) -> str:
        """Extract text content from parsed data"""
        if not data:
            return ""
        
        text_parts = []
        
        # Add skills
        if 'skills' in data:
            if isinstance(data['skills'], list):
                text_parts.extend(data['skills'])
            elif isinstance(data['skills'], dict):
                for category, skills in data['skills'].items():
                    if isinstance(skills, list):
                        text_parts.extend(skills)
        
        # Add experience
        if 'experience' in data and isinstance(data['experience'], list):
            text_parts.extend(data['experience'])
        
        # Add projects
        if 'projects' in data and isinstance(data['projects'], list):
            text_parts.extend(data['projects'])
        
        # Add responsibilities and qualifications from JD
        if 'responsibilities' in data and isinstance(data['responsibilities'], list):
            text_parts.extend(data['responsibilities'])
        
        if 'qualifications' in data and isinstance(data['qualifications'], list):
            text_parts.extend(data['qualifications'])
        
        return ' '.join(str(part) for part in text_parts if part)
    
    def _calculate_skill_match(self, resume_data: Dict, jd_data: Dict) -> Dict[str, Any]:
        """Calculate skill-based matching score"""
        resume_skills = self._extract_skills_list(resume_data)
        jd_skills = self._extract_skills_list(jd_data)
        
        if not jd_skills:
            return {'score': 0, 'matched_skills': [], 'missing_skills': [], 'extra_skills': []}
        
        # Create lowercase mappings for comparison
        resume_lower = {skill.lower(): skill for skill in resume_skills}
        jd_lower = {skill.lower(): skill for skill in jd_skills}
        
        resume_set = set(resume_lower.keys())
        jd_set = set(jd_lower.keys())
        
        # Calculate matches
        matched = resume_set & jd_set
        missing = jd_set - resume_set
        extra = resume_set - jd_set
        
        # Calculate score
        score = len(matched) / len(jd_set) * 100 if jd_set else 0
        
        return {
            'score': round(score, 1),
            'matched_skills': [jd_lower[skill] for skill in sorted(matched)],
            'missing_skills': [jd_lower[skill] for skill in sorted(missing)],
            'extra_skills': [resume_lower[skill] for skill in sorted(extra)],
            'skill_coverage': round(len(matched) / len(jd_set) * 100, 1) if jd_set else 0
        }
    
    def _extract_skills_list(self, data: Dict) -> List[str]:
        """Extract skills as a flat list from data"""
        skills = []
        
        if 'skills' in data:
            if isinstance(data['skills'], list):
                skills.extend(data['skills'])
            elif isinstance(data['skills'], dict):
                for category, skill_list in data['skills'].items():
                    if isinstance(skill_list, list):
                        skills.extend(skill_list)
        
        return [str(skill).strip() for skill in skills if skill]
    
    def _calculate_semantic_match(self, resume_text: str, jd_text: str) -> Dict[str, Any]:
        """Calculate semantic similarity between resume and job description"""
        similarity = self.nlp_processor.calculate_semantic_similarity(resume_text, jd_text)
        
        # Convert similarity to percentage
        score = similarity * 100
        
        return {
            'score': round(score, 1),
            'similarity': round(similarity, 3),
            'interpretation': self._interpret_similarity(similarity)
        }
    
    def _interpret_similarity(self, similarity: float) -> str:
        """Interpret semantic similarity score"""
        if similarity >= 0.8:
            return "Excellent semantic match - highly relevant"
        elif similarity >= 0.6:
            return "Good semantic match - relevant"
        elif similarity >= 0.4:
            return "Moderate semantic match - somewhat relevant"
        elif similarity >= 0.2:
            return "Low semantic match - limited relevance"
        else:
            return "Very low semantic match - not very relevant"
    
    def _calculate_experience_match(self, resume_data: Dict, jd_data: Dict) -> Dict[str, Any]:
        """Calculate experience level matching"""
        resume_exp = self._extract_experience_info(resume_data)
        jd_exp = self._extract_experience_info(jd_data)
        
        if not jd_exp.get('years_experience'):
            return {'score': 50, 'resume_exp': resume_exp, 'jd_exp': jd_exp, 'match': 'unknown'}
        
        resume_years = resume_exp.get('years_experience', 0)
        jd_years = jd_exp.get('years_experience', 0)
        
        # Calculate experience match score
        if resume_years >= jd_years:
            score = 100
        elif resume_years >= jd_years * 0.8:
            score = 90
        elif resume_years >= jd_years * 0.6:
            score = 75
        elif resume_years >= jd_years * 0.4:
            score = 60
        else:
            score = 30
        
        return {
            'score': score,
            'resume_exp': resume_exp,
            'jd_exp': jd_exp,
            'match': 'meets_requirements' if resume_years >= jd_years else 'below_requirements'
        }
    
    def _extract_experience_info(self, data: Dict) -> Dict[str, Any]:
        """Extract experience information from data"""
        if not data:
            return {}
        
        # Try to extract from structured data first
        if 'experience_info' in data:
            return data['experience_info']
        
        # Extract from text if available
        text = self._extract_text_from_data(data)
        if text:
            return self.nlp_processor.extract_experience_info(text)
        
        return {}
    
    def _calculate_keyword_match(self, resume_text: str, jd_text: str) -> Dict[str, Any]:
        """Calculate keyword-based matching using TF-IDF"""
        if not resume_text or not jd_text:
            return {'score': 0, 'common_keywords': [], 'missing_keywords': []}
        
        try:
            # Extract keywords from both texts
            resume_keywords = [kw[0] for kw in self.nlp_processor.extract_keywords(resume_text, 20)]
            jd_keywords = [kw[0] for kw in self.nlp_processor.extract_keywords(jd_text, 20)]
            
            # Find common keywords
            resume_set = set(resume_keywords)
            jd_set = set(jd_keywords)
            
            common = resume_set & jd_set
            missing = jd_set - resume_set
            
            # Calculate score
            score = len(common) / len(jd_set) * 100 if jd_set else 0
            
            return {
                'score': round(score, 1),
                'common_keywords': list(common),
                'missing_keywords': list(missing),
                'keyword_coverage': round(len(common) / len(jd_set) * 100, 1) if jd_set else 0
            }
        except Exception as e:
            print(f"Error in keyword matching: {e}")
            return {'score': 0, 'common_keywords': [], 'missing_keywords': []}
    
    def _generate_detailed_analysis(self, resume_data: Dict, jd_data: Dict, resume_text: str, jd_text: str) -> Dict[str, Any]:
        """Generate detailed analysis of the match"""
        analysis = {
            'strengths': [],
            'weaknesses': [],
            'recommendations': [],
            'risk_factors': []
        }
        
        # Analyze skill match
        skill_match = self._calculate_skill_match(resume_data, jd_data)
        
        if skill_match['score'] >= 80:
            analysis['strengths'].append("Strong skill alignment with job requirements")
        elif skill_match['score'] >= 60:
            analysis['strengths'].append("Good skill alignment with most requirements")
        else:
            analysis['weaknesses'].append("Limited skill alignment with job requirements")
        
        # Analyze experience
        exp_match = self._calculate_experience_match(resume_data, jd_data)
        
        if exp_match['score'] >= 90:
            analysis['strengths'].append("Experience level meets or exceeds requirements")
        elif exp_match['score'] >= 70:
            analysis['strengths'].append("Experience level is adequate")
        else:
            analysis['weaknesses'].append("Experience level may be below requirements")
        
        # Analyze semantic match
        semantic_match = self._calculate_semantic_match(resume_text, jd_text)
        
        if semantic_match['score'] >= 70:
            analysis['strengths'].append("High semantic relevance to job description")
        elif semantic_match['score'] >= 50:
            analysis['strengths'].append("Moderate semantic relevance")
        else:
            analysis['weaknesses'].append("Low semantic relevance to job description")
        
        # Generate recommendations
        if skill_match['missing_skills']:
            analysis['recommendations'].append(f"Consider gaining experience with: {', '.join(skill_match['missing_skills'][:3])}")
        
        if exp_match['score'] < 70:
            analysis['recommendations'].append("Highlight relevant projects and achievements to compensate for experience gap")
        
        if semantic_match['score'] < 50:
            analysis['recommendations'].append("Tailor resume language to better match job description terminology")
        
        # Risk factors
        if skill_match['score'] < 40:
            analysis['risk_factors'].append("Significant skill gap may impact job performance")
        
        if exp_match['score'] < 50:
            analysis['risk_factors'].append("Experience gap may be a concern for employers")
        
        return analysis
    
    def _empty_result(self) -> Dict[str, Any]:
        """Return empty result structure"""
        return {
            'overall_score': 0,
            'skill_match': {'score': 0, 'matched_skills': [], 'missing_skills': [], 'extra_skills': []},
            'semantic_match': {'score': 0, 'similarity': 0, 'interpretation': 'No data available'},
            'experience_match': {'score': 0, 'resume_exp': {}, 'jd_exp': {}, 'match': 'unknown'},
            'keyword_match': {'score': 0, 'common_keywords': [], 'missing_keywords': []},
            'analysis': {'strengths': [], 'weaknesses': [], 'recommendations': [], 'risk_factors': []},
            'suggestions': {'missing_skills': [], 'skill_coverage': 0, 'recommendations': []},
            'weights': {'skill': 0.35, 'semantic': 0.25, 'experience': 0.25, 'keyword': 0.15}
        }
