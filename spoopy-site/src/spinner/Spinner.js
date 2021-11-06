import React from "react";
import "./Spinner.css";
import { styled } from "@mui/system";

const StyledSpinner = styled("div")({
  margin: "100px auto",
  width: "40px",
  height: "40px",
  position: "relative"
});

const StyledCube = styled("div")({
  animation: "sk-cubemove 1.8s infinite ease-in-out",
  backgroundColor: "grey",
  width: "15px",
  height: "15px",
  position: "absolute",
  top: 0,
  left: 0,
});

const StyledDelayedCube = styled(StyledCube)({
  animationDelay: "-.9s"
});

function Spinner() {
  return (
    <StyledSpinner>
      <StyledCube/>
      <StyledDelayedCube/>
    </StyledSpinner>
  );
}

export default Spinner;
