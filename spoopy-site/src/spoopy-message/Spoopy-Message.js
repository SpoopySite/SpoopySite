import React, { lazy } from "react";
import PropTypes from "prop-types";
import ListItem from "@mui/material/ListItem";
import ListItemAvatar from "@mui/material/ListItemAvatar";
import Avatar from "@mui/material/Avatar";
import { ListItemText } from "@mui/material";
import { Adfly } from "./warningMessages";
import { styled } from "@mui/system";

const { Youtube, Bitly } = lazy(() => import(/* webpackChunkName: "wM" */ "./warningMessages"));

const StyledResults = styled(ListItem)({
  fontSize: "1.5em",
  overflowWrap: "break-word"
});

const StyledErrorText = styled(ListItemText)({
  color: "red"
});

function SpoopyMessageResults({ error, youtube, url, bitly_warning, adfly, safety, reasons }) {
  if (error) {
    return (
      <StyledErrorText primary={error}/>
    );
  } else if (youtube) {
    return (
      <Youtube url={url}/>
    );
  } else if (bitly_warning) {
    return (
      <Bitly url={url}/>
    );
  } else if (adfly) {
    return (
      <Adfly url={url} safety={safety}/>
    );
  } else {
    return (
      <ListItemText
        primary={`${url} ${safety ? "\u2714" : "\u274c"}`}
        secondary={reasons.join(", ")}
      />
    );
  }
}

SpoopyMessageResults.propTypes = {
  error: PropTypes.bool,
  youtube: PropTypes.bool.isRequired,
  url: PropTypes.string.isRequired,
  bitly_warning: PropTypes.bool.isRequired,
  adfly: PropTypes.bool.isRequired,
  safety: PropTypes.bool.isRequired,
  reasons: PropTypes.arrayOf(PropTypes.string).isRequired
};

function SpoopyMessage({ data }) {
  const { url, safety, reasons, error, youtube, bitly_warning, adfly } = data;

  return (
    <StyledResults alignItems="flex-start">
      <ListItemAvatar>
        <Avatar sx={{ width: 32, height: 32 }} src={`https://www.google.com/s2/favicons?domain=${url}&sz=32`}/>
      </ListItemAvatar>
      <SpoopyMessageResults
        safety={safety}
        url={url}
        adfly={adfly}
        bitly_warning={bitly_warning}
        error={error}
        reasons={reasons}
        youtube={youtube}
      />
    </StyledResults>
  );
}

SpoopyMessage.propTypes = {
  data: PropTypes.object.isRequired
};

export default SpoopyMessage;
