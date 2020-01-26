import React, { Component } from "react";
import { Link } from "react-router-dom";
import "./Footer.css";

class Footer extends Component {
  render() {
    return (
      <footer>
        <p>
          <Link to="/">Home</Link>
          <Link to="/docs">Docs</Link>
          <a href="https://github.com/Lagicrus/spoopy-python">GitHub</a>
        </p>
        <p className="inspiration">
          Inspired by <a href="https://github.com/spoopy-link/server">spoopy link</a>
        </p>
      </footer>
    );
  }
}

export default Footer;
