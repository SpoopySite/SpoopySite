import React, { useCallback, useEffect, useState } from "react";
import PropTypes from "prop-types";
import Stack from "@mui/material/Stack";
import Typography from "@mui/material/Typography";
import Switch from "@mui/material/Switch";
import Toolbar from "@mui/material/Toolbar";
import AppBar from "@mui/material/AppBar";
import Box from "@mui/material/Box";

function changeItem(event, value, key, reloadWrapper) {
  if (value == null) {
    return;
  }
  localStorage.setItem(key, value);
  reloadWrapper(Math.round(Math.random() * 100));
}

function Header({ theme, handleReload }) {
  const [checkedC, setCheckedC] = useState(true);
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
      <Box sx={{ flexGrow: 1 }}>
        <AppBar position="static" color="transparent">
          <Toolbar sx={{justifyContent: "flex-end"}}>
            <Stack direction="row" spacing={1} alignItems="center">
              <Typography>Dark Mode</Typography>
              <Switch
                checked={checkedC}
                onChange={handleChange}
                color="default"
              />
              <Typography>Light Mode</Typography>
            </Stack>
          </Toolbar>
        </AppBar>
      </Box>
    </header>
  );
}

Header.propTypes = {
  theme: PropTypes.string.isRequired,
  handleReload: PropTypes.func.isRequired
};

export default Header;
