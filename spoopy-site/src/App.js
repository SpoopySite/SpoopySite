import React, { useMemo, useState } from "react";
import { BrowserRouter as Router, Route, Switch } from "react-router-dom";
import Homepage from "./homepage/Homepage";
import Spoopy from "./spoopy/Spoopy";
import Footer from "./footer/Footer";
import Docs from "./docs/Docs";
import Faq from "./faq/Faq";
import Header from "./header/Header";
import { createTheme, CssBaseline, ThemeProvider, useMediaQuery } from "@material-ui/core";
import { getKeyWrapper } from "./utils";
import { StyledEngineProvider } from "@material-ui/core/styles";

function App() {
  const [, handleReload] = useState(0);
  const cssPrefersDarkMode = useMediaQuery("(prefers-color-scheme: dark)", {
    noSsr: true
  });
  // eslint-disable-next-line no-unused-vars
  const [prefersDarkMode, resPDMLS] = getKeyWrapper("darkTheme", cssPrefersDarkMode);

  const theme = useMemo(
    () =>
      createTheme({
        palette: {
          mode: prefersDarkMode ? "dark" : "light"
        }
      }),
    [prefersDarkMode]
  );

  return (
    <Router>
      <StyledEngineProvider>
        <ThemeProvider theme={theme}>
          <CssBaseline/>
          <Header theme={theme.palette.mode} handleReload={handleReload}/>
          <Switch>
            <Route path={"/site/:suspect_url"} children={<Spoopy/>}/>
            <Route path="/docs" children={<Docs/>}/>
            <Route path="/faq" children={<Faq/>}/>
            <Route exact-path="/" children={<Homepage/>}/>
          </Switch>
          <Footer/>
        </ThemeProvider>
      </StyledEngineProvider>
    </Router>
  );
}


export default App;
