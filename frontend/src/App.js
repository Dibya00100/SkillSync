import React, { useState } from "react";
import axios from "axios";
import logo from "./assets/skillsync_logo.png";
import "./App.css";
import { FaFileUpload } from "react-icons/fa";
import { MdDescription } from "react-icons/md";

function App() {
  const [darkMode, setDarkMode] = useState(false);
  const [resumeData, setResumeData] = useState(null);
  const [jdData, setJdData] = useState(null);
  const [matchResult, setMatchResult] = useState(null);

  const handleUpload = async (event, endpoint, setter) => {
    const file = event.target.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await axios.post(`http://127.0.0.1:5000/${endpoint}`, formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setter(res.data);
    } catch (err) {
      console.error("Upload failed:", err);
    }
  };

  const handleMatch = async () => {
    try {
      const res = await axios.post("http://127.0.0.1:5000/match", {
        resume: resumeData,
        jd: jdData,
      });
      setMatchResult(res.data);
    } catch (err) {
      console.error("Match failed:", err);
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
          <button onClick={handleMatch}>Match Resume with JD</button>
          {matchResult && (
            <div className="result">
              <h3>Match Result</h3>

              {/* Score Progress Bar */}
              <div className="score-bar">
                <div
                  className="score-fill"
                  style={{ width: `${matchResult.match_score}%` }}
                >
                  {matchResult.match_score}%
                </div>
              </div>

              {/* Skills */}
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
      </div>
    </div>
  );
}

export default App;