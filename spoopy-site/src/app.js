import React from "react";
import { BrowserRouter as Router, Route, Switch } from "react-router-dom";
import Homepage from "./homepage/Homepage";
import Spoopy from "./spoopy/Spoopy";

function App() {
  return (
    <main>
      <Router>
        <Switch>
          <Route path={"/site/:suspect_url"} children={<Spoopy/>}/>
          <Route exact-path="/" children={<Homepage/>}/>
        </Switch>
      </Router>
    </main>
  );
}

export default App;
