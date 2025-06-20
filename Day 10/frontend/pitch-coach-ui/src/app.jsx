import React, { useState } from "react";
import axios from "axios";
import "./styles/app.css";

function App() {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleUpload = async () => {
    if (!file) return alert("Select a file first.");
    const formData = new FormData();
    formData.append("file", file);
    setLoading(true);
    try {
      const res = await axios.post("http://localhost:8000/upload", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setResult(res.data);
    } catch (e) {
      alert("Upload failed.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <h1>Pitch Deck Coach</h1>
      <input type="file" onChange={(e) => setFile(e.target.files[0])} />
      <button onClick={handleUpload} disabled={loading}>
        {loading ? "Analyzing..." : "Upload & Analyze"}
      </button>
      {result && (
        <div className="results">
          <h2>Results</h2>
          <pre>{JSON.stringify(result, null, 2)}</pre>
        </div>
      )}
    </div>
  );
}

export default App;
