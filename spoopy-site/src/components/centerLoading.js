import React from "react";
import { CircularProgress } from "@material-ui/core";
import { makeStyles } from "@material-ui/styles";

const useStyles = makeStyles({
  loading: {
    position: "absolute",
    left: "50%",
    top: "40%"
  }
});

export default function CenterLoading() {
  const classes = useStyles();
  return (
    <div className={classes.loading}>
      <CircularProgress/>
    </div>
  );
}
