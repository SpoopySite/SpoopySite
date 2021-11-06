import React, { useState } from "react";
import { Redirect } from "react-router-dom";
import Container from "@mui/material/Container";
import Typography from "@mui/material/Typography";
import { styled } from "@mui/system";

const StyledContainer = styled(Container)({
  position: "absolute",
  top: "50%",
  left: "50%",
  transform: "translate(-50%, -50%)"
});

const StyledDiv = styled("div")({
  paddingTop: 3,
  "& button": {
    marginLeft: 5,
  },
  "& button, label, input": {
    fontSize: "1.3rem"
  }
});
function Homepage() {
  const [switchPage, setSwitchPage] = useState(false);
  const [spoopyURL, setSpoopyURL] = useState("");

  const goToSpoopy = (event) => {
    const keyCode = event.keyCode || event.which;
    if (event.type === "click" || keyCode === 13) {
      setSwitchPage(true);
    }
  };

  /**
   * @param {React.ChangeEvent<HTMLInputElement>} event
   */
  const handleChange = (event) => {
    let url = event.target.value.trim();
    if (!url.startsWith("http") && !url.startsWith("https") && url.length > 0) {
      url = `http://${url}`;
    }
    setSpoopyURL(url);
  };

  return (
    switchPage ?
      <Redirect push to={`/site/${encodeURIComponent(spoopyURL)}`}/> :
      <StyledContainer>
        <Typography variant="h3" component="h1" align="center">Spoopy Website Detector</Typography>
        <Typography variant="h5" component="h2" align="center">Checks how risky a website is by checking for IP Logging,
          Phishing, Malware and more.</Typography>
        <StyledDiv align="center">
          <label htmlFor="input">Check a link: </label>
          <input id="input" type="text" value={spoopyURL} onKeyUp={goToSpoopy}
                 onChange={handleChange} autoFocus={true}/>
          <button id="go" onClick={goToSpoopy} onKeyUp={goToSpoopy}>Go</button>
        </StyledDiv>
      </StyledContainer>
  );
}

export default Homepage;
