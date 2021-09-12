import React from "react";
import Container from "@mui/material/Container";
import { makeStyles } from "@mui/styles";

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
