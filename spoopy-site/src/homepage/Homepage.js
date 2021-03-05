import React, { useState } from "react";
import { Redirect } from "react-router-dom";
import "./Homepage.css";

function Homepage() {
  const [switchPage, setSwitchPage] = useState(false);
  const [spoopyURL, setSpoopyURL] = useState("");

  const goToSpoopy = (event) => {
    const keyCode = event.keyCode || event.which;
    if (event.type === "click" || keyCode === 13) {
      setSwitchPage(true);
    }
  };

  const handleChange = (event) => {
    setSpoopyURL(event.target.value);
  };

  return (
    switchPage ?
      <Redirect push to={`/site/${encodeURIComponent(spoopyURL)}`}/> :
      <div className="wrapper">
        <h1>Spoopy Website Detector</h1>
        <h3>Checks how risky a website is by checking for IP Logging, Phishing, Malware and more.</h3>
        <div>
          <label htmlFor="input">Check a link: </label>
          <input id="input" type="text" value={spoopyURL} onKeyUp={goToSpoopy}
                 onChange={handleChange}/>
          <button id="go" onClick={goToSpoopy} onKeyUp={goToSpoopy}>Go</button>
        </div>
      </div>
  );
}

export default Homepage;
