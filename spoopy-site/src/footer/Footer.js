import React, { Component } from "react";
import "./Footer.css";

class Footer extends Component {
  render() {
    return (
      <footer className="page-footer">
        <div className="footer-copyright">
          <div className="container center-align">
            <p>Inspired by <a href="https://github.com/spoopy-link/server">spoopy</a>. Source at <a
              href="https://github.com/Lagicrus/spoopy">Github</a></p>
          </div>
        </div>
      </footer>
    );
  }
}

export default Footer;
