import React, { Component } from "react";
import "./Footer.css";

class Footer extends Component {
  render() {
    return (
      <footer className="page-footer">
        <div className="footer-copyright">
          <div className="container">
            <p>Inspired by <a href="https://github.com/spoopy-link/server">spoopy</a>. Source at <a
              href="https://github.com/Lagicrus/spoopy-python">Github</a></p>
            <p className="subFooter">Docs can be found <a href="/docs">here</a>. Homepage
            located <a href="/">here</a></p>
          </div>
        </div>
      </footer>
    );
  }
}

export default Footer;
