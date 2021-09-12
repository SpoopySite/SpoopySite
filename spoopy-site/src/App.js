import React, { lazy, Suspense, useMemo, useState } from "react";
import { BrowserRouter as Router, Route, Switch } from "react-router-dom";
import Spoopy from "./spoopy/Spoopy";
import Footer from "./footer/Footer";
import Header from "./header/Header";
import { adaptV4Theme, createTheme, CssBaseline, ThemeProvider, useMediaQuery } from "@mui/material";
import { getKeyWrapper } from "./utils";
import CenterLoading from "./components/centerLoading";
import {StyledEngineProvider} from "@mui/material/styles"

function lazyLoadRetry(fn, retriesLeft = 5, interval = 1000) {
  return new Promise((resolve, reject) => {
    fn()
      .then(resolve)
      .catch(() => {
        setTimeout(() => {
          if (retriesLeft === 1) {
            window.location.reload();
          }

          lazyLoadRetry(fn, retriesLeft - 1, interval).then(resolve, reject);
        }, interval);
      });
  });
}

const Homepage = lazy(() => lazyLoadRetry(() => import(/* webpackChunkName: "hP" */ "./homepage/Homepage")));
const About = lazy(() => lazyLoadRetry(() => import(/* webpackChunkName: "aP" */ "./about/About")));
const Faq = lazy(() => lazyLoadRetry(() => import(/* webpackChunkName: "fP" */ "./faq/Faq")));
const Docs = lazy(() => lazyLoadRetry(() => import(/* webpackChunkName: "dP" */ "./docs/Docs")));

function App() {
  const [, handleReload] = useState(0);
  const cssPrefersDarkMode = useMediaQuery("(prefers-color-scheme: dark)", {
    noSsr: true
  });
  // eslint-disable-next-line no-unused-vars
  const [prefersDarkMode, resPDMLS] = getKeyWrapper("darkTheme", cssPrefersDarkMode);

  const theme = useMemo(
    () =>
      createTheme(adaptV4Theme({
        palette: {
          mode: prefersDarkMode ? "dark" : "light"
        }
      })),
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
            <Route path="/docs">
              <Suspense fallback={<CenterLoading/>}>
                <Docs/>
              </Suspense>
            </Route>
            <Route path="/faq">
              <Suspense fallback={<CenterLoading/>}>
                <Faq/>
              </Suspense>
            </Route>
            <Route path="/about">
              <Suspense fallback={<CenterLoading/>}>
                <About/>
              </Suspense>
            </Route>
            <Route exact-path="/">
              <Suspense fallback={<CenterLoading/>}>
                <Homepage/>
              </Suspense>
            </Route>
          </Switch>
          <Footer/>
        </ThemeProvider>
      </StyledEngineProvider>
    </Router>
  );
}


export default App;
