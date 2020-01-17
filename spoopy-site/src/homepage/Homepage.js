import React from 'react';
import "./Homepage.css";

function Homepage() {
  function goToSpoopy(event) {
    const keyCode = event.keyCode || event.which;
    if (keyCode !== 13) return;
    window.location.pathname = "spoopy/" + encodeURIComponent(document.getElementById('input').value);
  }

  return (
    <div className="wrapper">
      <h1>Spoopy Website Detector</h1>
      <h3>Checks how risky a website is by checking for IP Logging, Phishing, Malware and more.</h3>
      <div>
        <label htmlFor="input">Check a link:</label>
        <input id="input" type="text" onKeyUp={goToSpoopy}/>
        <button id="go">Go</button>
      </div>
    </div>
  );
}

export default Homepage;
