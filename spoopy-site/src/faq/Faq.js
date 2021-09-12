import React from "react";
import Container from "@mui/material/Container";
import Typography from "@mui/material/Typography";
import List from "@mui/material/List";
import ListItemText from "@mui/material/ListItemText";
import ListItem from "@mui/material/ListItem"

function Docs() {
  return (
    <Container>
      <Typography variant="h4" component="h1">FAQ</Typography>
      <Typography variant="h5" component="h2" id="Youtube">Youtube</Typography>
      <Typography>In the traditional Youtube redirect URL which can be seen below.</Typography>
      <Typography>There is the `q` parameter which refers to the destination URL for the redirect.</Typography>
      <Typography>This must be automatically used, rather than then regular following the redirects as Youtube returns a
        200
        status code when requested.</Typography>
      <Typography>So instead we must "guess" which it should go.</Typography>
      <code>https://www.youtube.com/redirect?v=VIDEO_CODE&redir_token=TOKEN&html_redirect=INT&event=EVENT&q=https%3A%2F%2Fgoogle.com</code>
      <Typography variant="h5" component="h2" id="BitlyWarnings">Bitly Warnings</Typography>
      <Typography>Bitly warns against some links, this could be any of the following reasons</Typography>
      <List>
        <ListItem><ListItemText primary="Bitly user reported a problem"/></ListItem>
        <ListItem><ListItemText primary="Black-listing service reported a problem"/></ListItem>
        <ListItem><ListItemText primary="Shortened multiple times"/></ListItem>
        <ListItem><ListItemText primary="Potentially malicious content"/></ListItem>
      </List>
    </Container>
  );
}

export default Docs;
