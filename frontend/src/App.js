import React, { useState } from "react";
import axios from "axios";
import logo from "./assets/skillsync_logo.png";
import "./App.css";
import { FaFileUpload, FaBrain, FaChartLine, FaLightbulb } from "react-icons/fa";
import { MdDescription, MdAnalytics, MdSettings } from "react-icons/md";

function App() {
  const [darkMode, setDarkMode] = useState(false);
  const [resumeData, setResumeData] = useState(null);
  const [jdData, setJdData] = useState(null);
  const [matchResult, setMatchResult] = useState(null);
  const [enhancedMatchResult, setEnhancedMatchResult] = useState(null);
  const [optimizationSuggestions, setOptimizationSuggestions] = useState(null);
  const [loading, setLoading] = useState(false);
  const [activeTab, setActiveTab] = useState('basic');

  const handleUpload = async (event, endpoint, setter) => {
    const file = event.target.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await axios.post(`http://127.0.0.1:5001/${endpoint}`, formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setter(res.data);
    } catch (err) {
      console.error("Upload failed:", err);
    }
  };

  const handleMatch = async () => {
    setLoading(true);
    try {
      const res = await axios.post("http://127.0.0.1:5001/match", {
        resume: resumeData,
        jd: jdData,
      });
      setMatchResult(res.data);
    } catch (err) {
      console.error("Match failed:", err);
    } finally {
      setLoading(false);
    }
  };

  const handleEnhancedMatch = async () => {
    setLoading(true);
    try {
      const res = await axios.post("http://127.0.0.1:5001/enhanced_match", {
        resume: resumeData,
        jd: jdData,
      });
      setEnhancedMatchResult(res.data);
    } catch (err) {
      console.error("Enhanced match failed:", err);
    } finally {
      setLoading(false);
    }
  };

  const handleOptimization = async () => {
    setLoading(true);
    try {
      const res = await axios.post("http://127.0.0.1:5001/optimize_resume", {
        resume: resumeData,
        jd: jdData,
      });
      setOptimizationSuggestions(res.data);
    } catch (err) {
      console.error("Optimization failed:", err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <header className="header">
        <img src={logo} alt="SkillSync" className="logo" />
        <h1>SkillSync</h1>
        <button className="dark-toggle" onClick={() => setDarkMode(!darkMode)}>
          {darkMode ? "☀️ Light" : "🌙 Dark"}
        </button>
      </header>

      <div className={darkMode ? "app dark" : "app"}>
        {/* Upload Resume */}
        <div className="container upload-box">
          <h2><FaFileUpload style={{ marginRight: "8px" }}/> Upload Resume</h2>
          <label className="file-label">
            <input
              type="file"
              onChange={(e) => handleUpload(e, "parse_resume", setResumeData)}
            />
            <span>📄 Choose or Drag & Drop Resume</span>
          </label>
          {resumeData && <pre>{JSON.stringify(resumeData, null, 2)}</pre>}
        </div>

        {/* Upload JD */}
        <div className="container upload-box">
          <h2><MdDescription style={{ marginRight: "8px" }}/> Upload Job Description</h2>
          <label className="file-label">
            <input
              type="file"
              onChange={(e) => handleUpload(e, "parse_jd", setJdData)}
            />
            <span>📋 Choose or Drag & Drop JD</span>
          </label>
          {jdData && <pre>{JSON.stringify(jdData, null, 2)}</pre>}
        </div>

        {/* Match Section */}
        <div className="container">
          <div className="tab-buttons">
            <button 
              className={activeTab === 'basic' ? 'active' : ''} 
              onClick={() => setActiveTab('basic')}
            >
              <FaChartLine /> Basic Match
            </button>
            <button 
              className={activeTab === 'enhanced' ? 'active' : ''} 
              onClick={() => setActiveTab('enhanced')}
            >
              <FaBrain /> AI Enhanced
            </button>
            <button 
              className={activeTab === 'optimize' ? 'active' : ''} 
              onClick={() => setActiveTab('optimize')}
            >
              <MdSettings /> ATS Optimize
            </button>
          </div>

          {activeTab === 'basic' && (
            <div>
              <button onClick={handleMatch} disabled={loading}>
                {loading ? 'Analyzing...' : 'Match Resume with JD'}
              </button>
              {matchResult && (
                <div className="result">
                  <h3>Basic Match Result</h3>
                  <div className="score-bar">
                    <div
                      className="score-fill"
                      style={{ width: `${matchResult.match_score}%` }}
                    >
                      {matchResult.match_score}%
                    </div>
                  </div>
                  <p>
                    <b>Matched Skills:</b>{" "}
                    {matchResult.matched_skills.map((s, i) => (
                      <span key={i} className="tag matched">{s}</span>
                    ))}
                  </p>
                  <p>
                    <b>Missing Skills:</b>{" "}
                    {matchResult.missing_skills.map((s, i) => (
                      <span key={i} className="tag missing">{s}</span>
                    ))}
                  </p>
                </div>
              )}
            </div>
          )}

          {activeTab === 'enhanced' && (
            <div>
              <button onClick={handleEnhancedMatch} disabled={loading}>
                {loading ? 'AI Analyzing...' : 'AI Enhanced Match'}
              </button>
              {enhancedMatchResult && (
                <div className="result enhanced-result">
                  <h3><FaBrain /> AI Enhanced Analysis</h3>
                  
                  {/* Overall Score */}
                  <div className="overall-score">
                    <h4>Overall Match Score: {enhancedMatchResult.overall_score}%</h4>
                    <div className="score-bar large">
                      <div
                        className="score-fill"
                        style={{ width: `${enhancedMatchResult.overall_score}%` }}
                      >
                        {enhancedMatchResult.overall_score}%
                      </div>
                    </div>
                  </div>

                  {/* Detailed Breakdown */}
                  <div className="breakdown">
                    <div className="breakdown-item">
                      <h5>Skill Match: {enhancedMatchResult.skill_match.score}%</h5>
                      <div className="mini-bar">
                        <div style={{ width: `${enhancedMatchResult.skill_match.score}%` }}></div>
                      </div>
                    </div>
                    <div className="breakdown-item">
                      <h5>Semantic Match: {enhancedMatchResult.semantic_match.score}%</h5>
                      <div className="mini-bar">
                        <div style={{ width: `${enhancedMatchResult.semantic_match.score}%` }}></div>
                      </div>
                      <small>{enhancedMatchResult.semantic_match.interpretation}</small>
                    </div>
                    <div className="breakdown-item">
                      <h5>Experience Match: {enhancedMatchResult.experience_match.score}%</h5>
                      <div className="mini-bar">
                        <div style={{ width: `${enhancedMatchResult.experience_match.score}%` }}></div>
                      </div>
                    </div>
                    <div className="breakdown-item">
                      <h5>Keyword Match: {enhancedMatchResult.keyword_match.score}%</h5>
                      <div className="mini-bar">
                        <div style={{ width: `${enhancedMatchResult.keyword_match.score}%` }}></div>
                      </div>
                    </div>
                  </div>

                  {/* Skills Analysis */}
                  <div className="skills-analysis">
                    <h5>Skills Analysis</h5>
                    <div className="skills-grid">
                      <div className="skill-category">
                        <h6>✅ Matched Skills</h6>
                        {enhancedMatchResult.skill_match.matched_skills.map((s, i) => (
                          <span key={i} className="tag matched">{s}</span>
                        ))}
                      </div>
                      <div className="skill-category">
                        <h6>❌ Missing Skills</h6>
                        {enhancedMatchResult.skill_match.missing_skills.map((s, i) => (
                          <span key={i} className="tag missing">{s}</span>
                        ))}
                      </div>
                      <div className="skill-category">
                        <h6>➕ Extra Skills</h6>
                        {enhancedMatchResult.skill_match.extra_skills.map((s, i) => (
                          <span key={i} className="tag extra">{s}</span>
                        ))}
                      </div>
                    </div>
                  </div>

                  {/* Analysis */}
                  <div className="analysis">
                    <h5>📊 Detailed Analysis</h5>
                    <div className="analysis-grid">
                      <div className="analysis-section">
                        <h6>Strengths</h6>
                        <ul>
                          {enhancedMatchResult.analysis.strengths.map((strength, i) => (
                            <li key={i}>{strength}</li>
                          ))}
                        </ul>
                      </div>
                      <div className="analysis-section">
                        <h6>Areas for Improvement</h6>
                        <ul>
                          {enhancedMatchResult.analysis.weaknesses.map((weakness, i) => (
                            <li key={i}>{weakness}</li>
                          ))}
                        </ul>
                      </div>
                      <div className="analysis-section">
                        <h6>Recommendations</h6>
                        <ul>
                          {enhancedMatchResult.analysis.recommendations.map((rec, i) => (
                            <li key={i}>{rec}</li>
                          ))}
                        </ul>
                      </div>
                    </div>
                  </div>
                </div>
              )}
            </div>
          )}

          {activeTab === 'optimize' && (
            <div>
              <button onClick={handleOptimization} disabled={loading}>
                {loading ? 'Generating Suggestions...' : 'Generate ATS Optimization'}
              </button>
              {optimizationSuggestions && (
                <div className="result optimization-result">
                  <h3><MdSettings /> ATS Optimization Suggestions</h3>
                  
                  <div className="optimization-metrics">
                    <div className="metric">
                      <h5>Skill Coverage</h5>
                      <div className="metric-value">{optimizationSuggestions.skill_coverage}%</div>
                    </div>
                  </div>

                  <div className="suggestions">
                    <h5>🎯 Missing Skills to Add</h5>
                    <div className="suggestion-list">
                      {optimizationSuggestions.missing_skills.map((skill, i) => (
                        <div key={i} className="suggestion-item">
                          <span className="suggestion-icon">💡</span>
                          <span>Consider adding: <strong>{skill}</strong></span>
                        </div>
                      ))}
                    </div>
                  </div>

                  <div className="recommendations">
                    <h5>📝 Recommendations</h5>
                    <ul>
                      {optimizationSuggestions.recommendations.map((rec, i) => (
                        <li key={i}>{rec}</li>
                      ))}
                    </ul>
                  </div>
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default App;