import React, { Component } from "react";
import "./Spoopy-Message.css";
import { Link } from "react-router-dom";

class SpoopyMessage extends Component {
  render() {
    const { url, safety, reasons, error, youtube, bitly_warning } = this.props.data;

    if (error) {
      return (
        <li className="error-results">
          <p>{error}</p>
        </li>
      );
    } else if (youtube) {
      return (
        <li className="results">
          <p>{url} {"\u2714"}</p>
          <p>This link was a guess. You can read more <Link to="/faq#Youtube">here</Link></p>
        </li>
      );
    } else if (bitly_warning) {
      return (
        <li className="results">
          <p>{url} {"\u274c"}</p>
          <p>Bitly does not recommend visiting the next link.
            You can read more <Link to="/faq#BitlyWarnings">here</Link></p>
        </li>
      )
    } else {
      return (
        <li className="results">
          <p>{url} {safety ? "\u2714" : "\u274c"}</p>
          <p>{reasons.join(", ")}</p>
        </li>
      );
    }
  }
}

export default SpoopyMessage;
