import React from 'react';
import "./Homepage.css";

function Homepage() {
  return (
    <div className="wrapper">
    <h1>Spoopy Website Detector</h1>
    <h3>Checks how risky a website is by checking for IP Logging, Phishing, Malware and more.</h3>
    <div>
      <label htmlFor="input">Check a link:</label>
      <input id="input" type="text"/>
      <button id="go">Go</button>
    </div>
  </div>
  );
}

export default Homepage;
