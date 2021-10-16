import React from "react";
import { Link } from "react-router-dom";
import ListItemText from "@mui/material/ListItemText";
import PropTypes from "prop-types";

export function Youtube({ url }) {
  return (
    <ListItemText
      primary={`${url} \u2714`}
      secondary={<>This link was a guess. You can read more <Link to="/faq#Youtube\">here</Link></>}
    />
  );
}

Youtube.propTypes = {
  url: PropTypes.string.isRequired
};

export function Bitly({ url }) {
  return (
    <ListItemText
      primary={`${url} \u274c`}
      secondary={<>Bitly does not recommend visiting the next link.
        You can read more <Link to="/faq#BitlyWarnings">here</Link></>}
    />
  );
}

Bitly.propTypes = {
  url: PropTypes.string.isRequired
};

export function Adfly({ url, safety }) {
  return (
    <ListItemText
      primary={`${url} ${safety ? "\u2714" : "\u274c"}`}
      secondary="Known Adfly Domain"
    />
  );
}

Adfly.propTypes = {
  url: PropTypes.string.isRequired,
  safety: PropTypes.bool.isRequired
}
