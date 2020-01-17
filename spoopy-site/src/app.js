import React from "react";
import { BrowserRouter as Router, Route, Switch } from "react-router-dom";
// import "./App.css";
// import Archive from "./Archive";
import Homepage from "./homepage/Homepage"

function App() {
  return (
    <main>
      <Router>
        <Switch>
          <Route exact-path="/" children={<Homepage/>} />
        </Switch>
      </Router>
    </main>
  );
}

export default App;
