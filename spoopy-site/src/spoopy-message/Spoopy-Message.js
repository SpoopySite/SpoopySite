import React from "react";
import { Link } from "react-router-dom";
import PropTypes from "prop-types";
import { makeStyles } from "@material-ui/core";
import ListItem from "@material-ui/core/ListItem";
import ListItemText from "@material-ui/core/ListItemText";

const useStyles = makeStyles({
  results: {
    fontSize: "1.5em",
    overflowWrap: "break-word"
  },
  errorResults: {
    fontSize: "1.5em",
    overflowWrap: "break-word",
    color: "red"
  }
});

function SpoopyMessage({ data }) {
  const { url, safety, reasons, error, youtube, bitly_warning } = data;
  const classes = useStyles();

  if (error) {
    return (
      <ListItem className={classes.errorResults}>
        <ListItemText primary={error}/>
      </ListItem>
    );
  } else if (youtube) {
    return (
      <ListItem className={classes.results}>
        <ListItemText
          primary={`${url} \u2714`}
          secondary={<>This link was a guess. You can read more <Link to="/faq#Youtube\">here</Link></>}
        />
      </ListItem>
    );
  } else if (bitly_warning) {
    return (
      <ListItem className={classes.results}>
        <ListItemText
          primary={`${url} \u274c`}
          secondary={<>Bitly does not recommend visiting the next link.
            You can read more <Link to="/faq#BitlyWarnings">here</Link></>}
        />
      </ListItem>
    );
  } else {
    return (
      <ListItem className={classes.results}>
        <ListItemText
          primary={`${url} ${safety ? "\u2714" : "\u274c"}`}
          secondary={reasons.join(", ")}
        />
      </ListItem>
    );
  }
}

SpoopyMessage.propTypes = {
  data: PropTypes.object.isRequired
};

export default SpoopyMessage;
