import React from "react";
import { Link as RouterLink } from "react-router-dom";
import { Link } from "@mui/material";
import { styled } from "@mui/system";

const StyledFooter = styled("footer")(({ theme }) => ({
  bottom: 0,
  position: "fixed",
  width: "100%",
  paddingTop: "0.5em",
  paddingBottom: "0.5em",
  borderTop: "3px solid lightslategray",
  fontSize: "20px",
  textAlign: "center",
  backgroundColor: theme.palette.background.default
}));

const StyledP = styled("p")({
  padding: 0,
  margin: 0,
  "& a": {
    display: "inline-block",
    padding: "2px"
  }
});

const StyledInspiration = styled(StyledP)({
  fontSize: "15px"
});

function Footer() {
  return (
    <StyledFooter>
      <StyledP>
        <Link component={RouterLink} to="/">Home</Link>
        <Link component={RouterLink} to="/docs">Docs</Link>
        <Link component={RouterLink} to="/faq">FAQ</Link>
        <Link href="https://github.com/Lagicrus/spoopy-python">GitHub</Link>
        <Link component={RouterLink} to="/about">About</Link>
      </StyledP>
      <StyledInspiration>
        Inspired by <Link href="https://github.com/spoopy-link/server">spoopy link</Link>
      </StyledInspiration>
    </StyledFooter>
  );
}

export default Footer;
