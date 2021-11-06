import React from "react";
import Container from "@mui/material/Container";
import { styled } from "@mui/system";

const StyledContainer = styled(Container)({
    container: {
    marginBottom: 71 // Height 58 + Padding 10 + Border Top 3
  }
})

export default function BottomPaddingContainer({ children }) {
  return (
    <StyledContainer>
      {children}
    </StyledContainer>
  );
}
