import React, { useState } from 'react';
import axios from 'axios';
import './styles.css';

function App() {
  const [selectedFiles, setSelectedFiles] = useState([]);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleFileChange = (e) => {
    // Convert FileList to array and set to state
    setSelectedFiles(Array.from(e.target.files));
  };

  const handleSubmit = async (e) => {
    setLoading(true);
    e.preventDefault();
    // Ensure exactly 4 files are selected
    if (selectedFiles.length !== 4) {
      alert('Please upload exactly 4 videos.');
      return;
    }

    const formData = new FormData();
    // Append all selected files to FormData
    selectedFiles.forEach(file => formData.append('videos', file));

    try {
      const response = await axios.post('http://localhost:5000/upload', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      setResult(response.data);
      console.log(response);
      setLoading(false);
    } catch (error) {
      console.error('Error uploading files:', error);
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <center><h1>Adaptive Traffic Signal Control System</h1>
      <hr/>
      <div className='main-container'>
        <div className='center'>
          <section id="upload" className="upload">
            <h2>   Attach Videos for Processing</h2>
            <p>Select 4 videos showing different roads at an intersection.</p>
            <form onSubmit={handleSubmit}>
              <input 
                type="file" 
                multiple 
                accept="video/*" 
                onChange={handleFileChange} 
              />
              <br/>
              <button type="submit">Get Timings</button>
            </form>
          </section>
          <section id="result" className="result">
          {!loading && !result && (
            <p className='placeholder'>Optimized Timings will appear here</p>
          )}
          {loading && <p className='loader'>Processing videos, it may take a few minutes...</p>}
          {result && !result.error && (
            <>
              <h2>Results</h2>
              <p>GA Optimized Green Light Timings:</p>
              <ul>
                <li>North: <span id="north-time">{result.north}</span> seconds</li>
                <li>South: <span id="south-time">{result.south}</span> seconds</li>
                <li>West: <span id="west-time">{result.west}</span> seconds</li>
                <li>East: <span id="east-time">{result.east}</span> seconds</li>
              </ul>
            </>
          )}
        </section>
        {result && result.error && (
          <div>
            <h2>Error:</h2>
            <p>{result.error}</p>
          </div>
        )}
        </div>
      </div>
      </center>
    </div>
  );
}

export default App;

