import React, { useEffect, useState } from "react";
import Switch from "@material-ui/core/Switch";
import PropTypes from "prop-types";
import { makeStyles } from "@material-ui/core";
import Typography from "@material-ui/core/Typography";
import Grid from "@material-ui/core/Grid";

const useStyles = makeStyles({
  themeSwitch: {
    right: 0,
    width: "auto",
    display: "inline-block",
    position: "fixed"
  }
});

function Header({ theme, toggleTheme }) {
  const [checkedC, setCheckedC] = useState(true);
  const classes = useStyles();

  useEffect(() => {
    if (checkedC.length === 0) {
      setCheckedC(theme === "light");
    }
  }, [checkedC, theme]);

  const handleChange = event => {
    setCheckedC(event.target.checked);
    toggleTheme();
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
  toggleTheme: PropTypes.func.isRequired
};

export default Header;
