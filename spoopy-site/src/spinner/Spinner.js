import React from "react";
import "./Spinner.css";
import clsx from "clsx";
import { makeStyles } from "@mui/styles";

const useStyles = makeStyles({
  spinner: {
    margin: "100px auto",
    width: "40px",
    height: "40px,",
    position: "relative"
  },
  cube: {
    backgroundColor: "grey",
    width: "15px",
    height: "15px",
    position: "absolute",
    top: 0,
    left: 0,
    animation: "sk-cubemove 1.8s infinite ease-in-out"
  },
  delayedCube: {
    animationDelay: "-.9s"
  }
});

function Spinner() {
  const classes = useStyles();
  return (
    <div className={classes.spinner}>
      <div className={classes.cube}/>
      <div className={clsx(classes.cube, classes.delayedCube)}/>
    </div>
  );
}

export default Spinner;
