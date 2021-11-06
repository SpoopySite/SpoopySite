import React from "react";
import { CircularProgress } from "@mui/material";
import { styled } from "@mui/system";

const StyledDiv = styled("div")({
  loading: {
    position: "absolute",
    left: "50%",
    top: "40%"
  }
})

export default function CenterLoading() {
  return (
    <StyledDiv>
      <CircularProgress/>
    </StyledDiv>
  );
}
