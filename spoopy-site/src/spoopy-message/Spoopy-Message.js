import React from "react";
import { Link } from "react-router-dom";
import PropTypes from "prop-types";
import { makeStyles } from "@material-ui/core";

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
      <li className={classes.errorResults}>
        <p>{error}</p>
      </li>
    );
  } else if (youtube) {
    return (
      <li className={classes.results}>
        <p>{url} {"\u2714"}</p>
        <p>This link was a guess. You can read more <Link to="/faq#Youtube">here</Link></p>
      </li>
    );
  } else if (bitly_warning) {
    return (
      <li className={classes.results}>
        <p>{url} {"\u274c"}</p>
        <p>Bitly does not recommend visiting the next link.
          You can read more <Link to="/faq#BitlyWarnings">here</Link></p>
      </li>
    );
  } else {
    return (
      <li className={classes.results}>
        <p>{url} {safety ? "\u2714" : "\u274c"}</p>
        <p>{reasons.join(", ")}</p>
      </li>
    );
  }
}

SpoopyMessage.propTypes = {
  data: PropTypes.object.isRequired
};

export default SpoopyMessage;
