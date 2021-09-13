import React, { useCallback, useEffect, useState } from "react";
import PropTypes from "prop-types";
import { makeStyles } from "@mui/styles";
import Stack from "@mui/material/Stack";
import Typography from "@mui/material/Typography";
import Switch from "@mui/material/Switch";

const useStyles = makeStyles({
  themeSwitch: {
    right: 0,
    width: "auto",
    display: "inline-block",
    position: "fixed"
  }
});

function changeItem(event, value, key, reloadWrapper) {
  if (value == null) {
    return;
  }
  localStorage.setItem(key, value);
  reloadWrapper(Math.round(Math.random() * 100));
}

function Header({ theme, handleReload }) {
  const [checkedC, setCheckedC] = useState(true);
  const classes = useStyles();
  const handleReloadWrapper = useCallback(
    (randomInt) => handleReload(randomInt),
    [handleReload]
  );

  useEffect(() => {
    if (theme === "dark") {
      setCheckedC(false);
    }
  }, [checkedC, theme]);

  const handleChange = (event, value) => {
    setCheckedC(event.target.checked);
    const num = value === false ? 1 : 2;
    changeItem(event, num, "darkTheme", handleReloadWrapper);
  };

  return (
    <header>
      <div className={classes.themeSwitch}>
        <Stack direction="row" spacing={1} alignItems="center">
          <Typography>Dark Mode</Typography>
          <Switch
            checked={checkedC}
            onChange={handleChange}
            color="default"
          />
          <Typography>Light Mode</Typography>
        </Stack>
      </div>
    </header>
  );
}

Header.propTypes = {
  theme: PropTypes.string.isRequired,
  handleReload: PropTypes.func.isRequired
};

export default Header;
