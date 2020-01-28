import React, { Component } from "react";
import Switch from "@material-ui/core/Switch";
import "./Header.css";

class Header extends Component {
  constructor(props) {
    super(props);

    this.state = {
      checkedC: (this.props.theme === "light")
    };
    this.toggleTheme = this.props.toggleTheme;
  }

  render() {
    const handleChange = name => event => {
      this.setState({ ...this.state, [name]: event.target.checked });
      this.toggleTheme();
    };

    return (
      <header>
        <div className="theme-switch">
          <span>Dark Mode</span>
          <Switch
            checked={this.state.checkedC}
            onChange={handleChange("checkedC")}
            color="default"
          />
          <span>Light Mode</span>
        </div>
      </header>
    );
  }
}

export default Header;
