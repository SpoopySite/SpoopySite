import React from "react";
import { BrowserRouter as Router, Route, Switch } from "react-router-dom";
// import "./App.css";
import Homepage from "./homepage/Homepage"
import Spoopy from "./spoopy/Spoopy"

function App() {
  return (
    <main>
      <Router>
        <Switch>
          <Route path={"/spoopy/:suspect_url"} children={<Spoopy/>}/>
          <Route exact-path="/" children={<Homepage/>} />
        </Switch>
      </Router>
    </main>
  );
}

export default App;
