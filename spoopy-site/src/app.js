import React, { Component } from "react";
import { BrowserRouter as Router, Route, Switch } from "react-router-dom";
import Homepage from "./homepage/Homepage";
import Spoopy from "./spoopy/Spoopy";
import Footer from "./footer/Footer";
import Docs from "./docs/Docs";
import Faq from "./faq/Faq";
import Header from "./header/Header";
import "./app.css";

class App extends Component {
  constructor(props) {
    super(props);

    if (localStorage.getItem("theme") === null) {
      localStorage.setItem("theme", "light");
    }

    this.state = {
      theme: localStorage.getItem("theme")
    };
    this.toggleTheme = this.toggleTheme.bind(this);
  }

  setTheme(theme) {
    document.documentElement.setAttribute("data-theme", theme);
    localStorage.setItem("theme", theme);
    document.documentElement.classList.add("theme-transition");
    window.setTimeout(() => {
      document.documentElement.classList.remove("theme-transition");
    }, 1000);
  }

  toggleTheme() {
    const theme = this.state.theme === "dark" ? "light" : "dark";
    console.log(this.state.theme);
    this.setState({ theme });
    this.setTheme(theme);
  }

  componentDidMount() {
    this.setTheme(localStorage.getItem("theme"));
  }

  render() {
    return (
      <main>
        <Router>
          <Header toggleTheme={this.toggleTheme} theme={this.state.theme}/>
          <Switch>
            <Route path={"/site/:suspect_url"} children={<Spoopy/>}/>
            <Route path="/docs" children={<Docs/>}/>
            <Route path="/faq" children={<Faq/>}/>
            <Route exact-path="/" children={<Homepage/>}/>
          </Switch>
          <Footer/>
        </Router>
      </main>
    );
  }
}


export default App;
