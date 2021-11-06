import React, { useState } from "react";
import { Redirect } from "react-router-dom";
import Container from "@mui/material/Container";
import Typography from "@mui/material/Typography";
import { styled } from "@mui/system";
import TextField from "@mui/material/TextField";
import InputAdornment from "@mui/material/InputAdornment";
import Button from "@mui/material/Button";

const StyledContainer = styled(Container)({
  position: "absolute",
  top: "50%",
  left: "50%",
  transform: "translate(-50%, -50%)"
});

const StyledDiv = styled("div")({
  paddingTop: "1em"
});

function Homepage() {
  const [switchPage, setSwitchPage] = useState(false);
  const [spoopyURL, setSpoopyURL] = useState("");

  const goToSpoopy = (event) => {
    const keyCode = event.keyCode || event.which;
    if (event.type === "click" || keyCode === 13) {
      if (!(spoopyURL.startsWith("http://") || (spoopyURL.startsWith("https://")))) {
        setSpoopyURL(`http://${spoopyURL}`);
      }
      setSwitchPage(true);
    }
  };

  /**
   * @param {React.ChangeEvent<HTMLInputElement>} event
   */
  const handleChange = (event) => {
    let url = event.target.value.trim();
    setSpoopyURL(url);
  };

  const StartAdornment = () => {
    if (spoopyURL.startsWith("http://") || (spoopyURL.startsWith("https://"))) {
      return null;
    }
    return (
      <InputAdornment position={"start"}>http://</InputAdornment>
    );
  };

  const EndAdornment = () => {
    return (
      <Button
        id="go"
        onClick={goToSpoopy}
        onKeyUp={goToSpoopy}
        variant="outlined"
      >
        Go
      </Button>
    );
  };

  return (
    switchPage ?
      <Redirect push to={`/site/${encodeURIComponent(spoopyURL)}`}/> :
      <StyledContainer>
        <Typography variant="h3" component="h1" align="center">Spoopy Website Detector</Typography>
        <Typography variant="h5" component="h2" align="center">Checks how risky a website is by checking for IP Logging,
          Phishing, Malware and more.</Typography>
        <StyledDiv align="center">
          <TextField
            id="input"
            type="text"
            value={spoopyURL}
            onKeyUp={goToSpoopy}
            onChange={handleChange}
            autoFocus
            variant="outlined"
            label="Check a link"
            InputProps={{
              startAdornment: <StartAdornment/>,
              endAdornment: <EndAdornment/>
            }}
            fullWidth
          />
        </StyledDiv>
      </StyledContainer>
  );
}

export default Homepage;
