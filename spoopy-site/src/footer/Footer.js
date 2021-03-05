import React from "react";
import { Link } from "react-router-dom";
import { makeStyles } from "@material-ui/core";
import clsx from "clsx";

const useStyles = makeStyles({
  footer: {
    bottom: 0,
    position: "fixed",
    width: "100%",
    paddingTop: "0.5em",
    paddingBottom: "0.5em",
    borderTop: "3px solid lightslategray",
    fontSize: "20px",
    textAlign: "center",
    backgroundColor: "white"
  },
  p: {
    padding: 0,
    margin: 0
  },
  a: {
    display: "inline-block",
    padding: "2px"
  },
  inspiration: {
    fontSize: "15px"
  }
});

function Footer() {
  const classes = useStyles();
  return (
    <footer className={classes.footer}>
      <p className={classes.p}>
        <Link className={classes.a} to="/">Home</Link>
        <Link className={classes.a} to="/docs">Docs</Link>
        <Link className={classes.a} to="/faq">FAQ</Link>
        <a href="https://github.com/Lagicrus/spoopy-python">GitHub</a>
      </p>
      <p className={clsx(classes.p, classes.inspiration)}>
        Inspired by <a href="https://github.com/spoopy-link/server">spoopy link</a>
      </p>
    </footer>
  );
}

export default Footer;
