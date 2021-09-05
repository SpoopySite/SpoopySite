import React from "react";
import Container from "@material-ui/core/Container";
import { makeStyles } from "@material-ui/styles";

const useStyles = makeStyles({
  container: {
    marginBottom: 71 // Height 58 + Padding 10 + Border Top 3
  }
});

export default function BottomPaddingContainer({ children }) {
  const classes = useStyles();
  return (
    <Container className={classes.container}>
      {children}
    </Container>
  );
}
