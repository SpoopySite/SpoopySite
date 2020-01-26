import React from "react";
import { BrowserRouter as Router, Route, Switch } from "react-router-dom";
import Homepage from "./homepage/Homepage";
import Spoopy from "./spoopy/Spoopy";
import Footer from "./footer/Footer";
import Docs from "./docs/Docs";

function App() {
  return (
    <main>
      <Router>
        <Switch>
          <Route path={"/site/:suspect_url"} children={<Spoopy/>}/>
          <Route path="/docs" children={<Docs/>}/>
          <Route exact-path="/" children={<Homepage/>}/>
        </Switch>
        <Footer/>
      </Router>
    </main>
  );
}

export default App;
