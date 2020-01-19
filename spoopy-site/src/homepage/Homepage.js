import React, { Component } from "react";
import { Redirect } from "react-router-dom";
import "./Homepage.css";

class Homepage extends Component {
  constructor(props) {
    super(props);

    this.state = {
      switchPage: false
    };
  }

  goToSpoopy(event) {
    const keyCode = event.keyCode || event.which;
    if (event.type === "click" || keyCode === 13) {
      console.log(true);
      console.log(this);
      this.setState({switchState: true})
      // window.location.pathname += "site/" + encodeURIComponent(document.getElementById("input").value);
    }
  }

  render() {
    if (this.state.switchPage) {
    return (
      <Redirect to="/site/test"/>
    );
  } else {
    return (
      <div className="wrapper">
        <h1>Spoopy Website Detector</h1>
        <h3>Checks how risky a website is by checking for IP Logging, Phishing, Malware and more.</h3>
        <div>
          <label htmlFor="input">Check a link:</label>
          <input id="input" type="text" onKeyUp={this.goToSpoopy}/>
          <button id="go" onClick={this.goToSpoopy} onKeyUp={this.goToSpoopy}>Go</button>
        </div>
      </div>
    );
  }
  }
}

export default Homepage;
