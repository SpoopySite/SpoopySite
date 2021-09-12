import React from "react";
import "./Docs.css";
import Container from "@mui/material/Container";
import Typography from "@mui/material/Typography";

const example_json = {
  "processed": {
    "urls": {
      "https://google.co.uk": {
        "safety": -1,
        "hsts": "NO_HSTS",
        "blacklist": false,
        "phishtank": false,
        "safe": true
      },
      "https://www.google.co.uk/": {
        "safety": -1,
        "hsts": "NO_HSTS",
        "blacklist": false,
        "phishtank": false,
        "safe": true
      }
    }
  }
};

function Docs() {
  return (
    <Container>
      <Typography variant="h4" component="h1">API</Typography>
      <Typography>Send a <b>GET</b> request to <b>/api/check_website</b></Typography>
      <Typography>The URL you are checking either needs to be sent in the JSON body
        under the <b>website</b> key.</Typography>
      <Typography>Or, it needs to be as a query parameter under the value <b>website</b></Typography>
      <Typography variant="h5" component="h2">Response</Typography>
      <Typography>The response will be a JSON based object which will contain the processed URLs
        under the "processed" "urls" keys.</Typography>
      <Typography>Each URL will then have the safety, hsts status, blacklisted, phishtank status
        and the overall status listed within.</Typography>
      <Typography variant="h5" component="h2">Example Response</Typography>
      <div id="example_json"><p>{JSON.stringify(example_json, null, 2)}</p></div>
    </Container>
  );
}

export default Docs;
