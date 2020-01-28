import React, { Component } from "react";
import "./Faq.css";

class Docs extends Component {
  render() {
    return (
      <div className="faq">
        <h2>FAQ</h2>
        <h3 id="Youtube">Youtube</h3>
        <p>In the traditional Youtube redirect URL which can be seen below.</p>
        <p>There is the `q` parameter which refers to the destination URL for the redirect.</p>
        <p>This must be automatically used, rather than then regular following the redirects as Youtube returns a 200 status code when requested.</p>
        <p>So instead we must "guess" which it should go.</p>
        <code>https://www.youtube.com/redirect?v=VIDEO_CODE&redir_token=TOKEN&html_redirect=INT&event=EVENT&q=https%3A%2F%2Fgoogle.com</code>
      </div>
    );
  }
}

export default Docs;
