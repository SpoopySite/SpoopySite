import React from "react";
import "./Faq.css";

function Docs() {
  return (
    <div className="faq">
      <h2>FAQ</h2>
      <h3 id="Youtube">Youtube</h3>
      <p>In the traditional Youtube redirect URL which can be seen below.</p>
      <p>There is the `q` parameter which refers to the destination URL for the redirect.</p>
      <p>This must be automatically used, rather than then regular following the redirects as Youtube returns a 200
        status code when requested.</p>
      <p>So instead we must "guess" which it should go.</p>
      <code>https://www.youtube.com/redirect?v=VIDEO_CODE&redir_token=TOKEN&html_redirect=INT&event=EVENT&q=https%3A%2F%2Fgoogle.com</code>
      <h3 id="BitlyWarnings">Bitly Warnings</h3>
      <p>Bitly warns against some links, this could be any of the following reasons</p>
      <ul>
        <li>Bitly user reported a problem</li>
        <li>Black-listing service reported a problem</li>
        <li>Shortened multiple times</li>
        <li>Potentially malicious content</li>
      </ul>
    </div>
  );
}

export default Docs;
