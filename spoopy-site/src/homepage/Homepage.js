import React, { useState } from "react";
import { Redirect } from "react-router-dom";
import Container from "@material-ui/core/Container";
import Typography from "@material-ui/core/Typography";
import { makeStyles } from "@material-ui/styles";

const useStyles = makeStyles({
  wrapper: {
    position: "absolute",
    top: "50%",
    left: "50%",
    transform: "translate(-50%, -50%)"
  },
  size: {
    fontSize: "1.3rem"
  }
})

function Homepage() {
  const [switchPage, setSwitchPage] = useState(false);
  const [spoopyURL, setSpoopyURL] = useState("");
  const classes = useStyles();

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
      url = `http://${url}`
    }
    setSpoopyURL(url);
  };

  return (
    switchPage ?
      <Redirect push to={`/site/${encodeURIComponent(spoopyURL)}`}/> :
      <Container className={classes.wrapper}>
        <Typography variant="h3" component="h1" align="center">Spoopy Website Detector</Typography>
        <Typography variant="h5" component="h2" align="center">Checks how risky a website is by checking for IP Logging, Phishing, Malware and more.</Typography>
        <div align="center">
          <label className={classes.size} htmlFor="input">Check a link: </label>
          <input className={classes.size} id="input" type="text" value={spoopyURL} onKeyUp={goToSpoopy}
                 onChange={handleChange} autoFocus={true} />
          <button className={classes.size} id="go" onClick={goToSpoopy} onKeyUp={goToSpoopy}>Go</button>
        </div>
      </Container>
  );
}

export default Homepage;
