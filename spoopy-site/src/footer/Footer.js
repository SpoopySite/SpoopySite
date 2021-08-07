import React from "react";
import { Link as RouterLink } from "react-router-dom";
import { Link } from "@material-ui/core";
import clsx from "clsx";
import Typography from "@material-ui/core/Typography";
import { makeStyles } from "@material-ui/styles";

const useStyles = makeStyles({
  footer: {
    bottom: 0,
    position: "fixed",
    width: "100%",
    paddingTop: "0.5em",
    paddingBottom: "0.5em",
    borderTop: "3px solid lightslategray",
    fontSize: "20px",
    textAlign: "center"
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
        <Link component={RouterLink} className={classes.a} to="/">Home</Link>
        <Link component={RouterLink} className={classes.a} to="/docs">Docs</Link>
        <Link component={RouterLink} className={classes.a} to="/faq">FAQ</Link>
        <Link href="https://github.com/Lagicrus/spoopy-python">GitHub</Link>
      </p>
      <Typography className={clsx(classes.p, classes.inspiration)}>
        Inspired by <Link href="https://github.com/spoopy-link/server">spoopy link</Link>
      </Typography>
    </footer>
  );
}

export default Footer;
