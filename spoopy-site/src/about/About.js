import React from "react";
import Typography from "@mui/material/Typography";
import Link from "@mui/material/Link";
import ListItem from "@mui/material/ListItem";
import ListItemText from "@mui/material/ListItemText";
import List from "@mui/material/List";
import { makeStyles } from "@mui/styles";
import BottomPaddingContainer from "../components/BottomPaddingContainer";

const useStyles = makeStyles({
  list: {
    "& a": {
      paddingTop: 0,
      paddingBottom: 0,
      maxWidth: "fit-content"
    },
    marginTop: "0 !important",
    marginBottom: "0 !important"
  },
  ghost: {
    margin: "0 auto",
    width: "min-content"
  }
});

const spoopyGhost =
  `     ████
   ████████
  █▓▓████▓▓█
 █▒▓▓▒██▒▓▓▒█
 █▒▒▒▒██▒▒▒▒█
 █▒▒▒▒██▒▒▒▒█
███▒▒████▒▒███
██████████████
██████████████
██ ███  ███ ██
█   ██  ██   █  - SuperFromNotDiscord`

function About() {
  const classes = useStyles();

  return (
    <BottomPaddingContainer>
      <pre className={classes.ghost}>{spoopyGhost}</pre>
      <Typography variant="h4" component="h1" gutterBottom>About</Typography>
      <Typography variant="h5" component="h2" gutterBottom>Inspiration</Typography>
      <Typography variant="body1">
        This was inspired by <Link href="https://github.com/devsnek">devsnek</Link>'s original
        project, <Link href="https://github.com/spoopy-link/server">Spoopy-Link</Link>
      </Typography>
      <Typography variant="body1" paragraph>
        This was created as the original wasn't being updated and it wasn't online much if at all over a 2 year period
        when myself and others wanted to use and check questionable links that were being sent.
        Thus, I decided to recreate it myself so we could use it again.
      </Typography>
      <Typography paragraph>
        I ended up doing it in Python due to this being my strength and at the time, lack of understanding in JS
        especially in Node.JS. This also proved to be a good starting project for my adventures into React.
      </Typography>
      <Typography variant="h5" component="h2" gutterBottom>Code</Typography>
      <Typography variant="body1">
        The code behind this project is allow open source and is hosted on <Link
        href="https://github.com/Lagicrus/spoopy-python">GitHub</Link>.
      </Typography>
      <Typography variant="body1" paragraph>Bug reports and pull requests are fully welcome</Typography>
      <Typography variant="body1">The project has somewhat grown since the original version after "converting"
        it.</Typography>
      <Typography variant="body1">It has since grown to check with sources such as <Link
        href="https://cloudflare.com">Cloudflare</Link> and
        their malware DNS service, a automated phishing provider, and even services to deal with common link sites such
        as AdFly and BitLy.</Typography>
      <Typography variant="body1">With more coming as needs demand</Typography>
      <Typography variant="h5" component="h2" gutterBottom>Who are you?</Typography>
      <Typography variant="body1" paragraph>
        I am <Link href="https://github.com/Lagicrus">Lagicrus</Link> on GitHub, and can be found on <Link
        href="https://discord.com">Discord</Link> as
        Oceanlord#0001
      </Typography>
      <Typography variant="h5" component="h2" gutterBottom>Tech Stack</Typography>
      <Typography variant="h6" component="h3" gutterBottom>Front-End</Typography>
      <Typography variant="body1">
        The list below shows what is used to help power this site's frontend and make it understandable and easy to use
      </Typography>
      <List className={classes.list}>
        <ListItem component={Link} href="https://reactjs.org"><ListItemText primary="ReactJS"/></ListItem>
        <ListItem component={Link} href="https://reactrouter.com/"><ListItemText primary="ReactRouter"/></ListItem>
        <ListItem component={Link} href="https://material-ui.com/"><ListItemText primary="Material-UI"/></ListItem>
      </List>
      <Typography variant="h6" component="h3" gutterBottom>Back-End</Typography>
      <Typography variant="body1">
        The list below shows what is used to help power the backend of the site and serve the API
      </Typography>
      <List className={classes.list}>
        <ListItem component={Link} href="https://sanicframework.org/"><ListItemText primary="Sanic"/></ListItem>
        <ListItem component={Link} href="https://www.docker.com/"><ListItemText primary="Docker"/></ListItem>
        <ListItem component={Link} href="https://docs.aiohttp.org/en/stable/"><ListItemText
          primary="AIOHTTP"/></ListItem>
        <ListItem component={Link} href="https://github.com/MagicStack/asyncpg"><ListItemText
          primary="asyncpg"/></ListItem>
      </List>
    </BottomPaddingContainer>
  );
}

export default About;
