import React, { Component } from "react";
import { Redirect } from "react-router-dom";
import "./Homepage.css";

class Homepage extends Component {
  constructor(props) {
    super(props);

    this.state = {
      switchPage: false,
      spoopy_url: null
    };

    this.goToSpoopy = this.goToSpoopy.bind(this);
    this.handleChange = this.handleChange.bind(this);
  }

  goToSpoopy(event) {
    const keyCode = event.keyCode || event.which;
    if (event.type === "click" || keyCode === 13) {
      this.setState({ switchPage: true });
      // window.location.pathname += "site/" + encodeURIComponent(document.getElementById("input").value);
    }
  }

  handleChange(event) {
    this.setState({ spoopy_url: event.target.value });
  }

  render() {
    if (this.state.switchPage) {
      return (
        <Redirect push to={"/site/" + encodeURIComponent(this.state.spoopy_url)}/>
      );
    } else {
      return (
        <div className="wrapper">
          <h1>Spoopy Website Detector</h1>
          <h3>Checks how risky a website is by checking for IP Logging, Phishing, Malware and more.</h3>
          <div>
            <label htmlFor="input">Check a link:</label>
            <input id="input" type="text" value={this.state.spoopy_url} onKeyUp={this.goToSpoopy}
                   onChange={this.handleChange}/>
            <button id="go" onClick={this.goToSpoopy} onKeyUp={this.goToSpoopy}>Go</button>
          </div>
        </div>
      );
    }
  }
}

export default Homepage;
