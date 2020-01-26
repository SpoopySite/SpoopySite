import React, { Component } from "react";
import "./Docs.css";

class Docs extends Component {
  render() {
    const example_json = {
      "processed": {
        "urls": {
          "https://google.co.uk": {
            "safety": -1,
            "hsts": "NO_HSTS",
            "blacklist": false,
            "phishtank": false,
            "safe": true
          },
          "https://www.google.co.uk/": {
            "safety": -1,
            "hsts": "NO_HSTS",
            "blacklist": false,
            "phishtank": false,
            "safe": true
          }
        }
      }
    };
    return (
      <div className="docs">
        <h2>API</h2>
        <p>Send a <b>GET</b> request to <b>/check_website</b></p>
        <p>The URL you are checking either needs to be sent in the JSON body
          under the <b>website</b> key.</p>
        <p>Or, it needs to be as a query parameter under the value <b>website</b></p>
        <h2>Response</h2>
        <p>The response will be a JSON based object which will contain the processed URLs
          under the "processed" "urls" keys.</p>
        <p>Each URL will then have the safety, hsts status, blacklisted, phishtank status
          and the overall status listed within.</p>
        <h3>Example Response</h3>
        <div id="example_json"><p>{JSON.stringify(example_json, null, 2)}</p></div>
      </div>
    );
  }
}

export default Docs;
