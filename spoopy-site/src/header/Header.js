import React, { useCallback, useEffect, useState } from "react";
import Switch from "@material-ui/core/Switch";
import PropTypes from "prop-types";
import Typography from "@material-ui/core/Typography";
import Grid from "@material-ui/core/Grid";
import { makeStyles } from "@material-ui/styles";

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
      setCheckedC(false)
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
        <Grid component="label" container alignItems="center" spacing={1}>
          <Grid item>
            <Typography>
              Dark Mode
            </Typography>
          </Grid>
          <Grid item>
            <Switch
              checked={checkedC}
              onChange={handleChange}
              color="default"
            />
          </Grid>
          <Grid item>
            <Typography>
              Light Mode
            </Typography>
          </Grid>
        </Grid>
      </div>
    </header>
  );
}

Header.propTypes = {
  theme: PropTypes.string.isRequired,
  handleReload: PropTypes.func.isRequired
};

export default Header;
