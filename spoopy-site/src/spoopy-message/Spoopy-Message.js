import React, {Component} from "react";
import "./Spoopy-Message.css";

class SpoopyMessage extends Component {
  render() {
    const {url, safety, reasons, error} = this.props.data;
    console.log(this.props.data)

    if (error) {
      return (
        <li>
          <p>{error}</p>
        </li>
      )
    } else {
      return (
        <li>
          <p>{url} {safety ? '\u2714' : '\u274c'}</p>
          <p>{reasons.join(", ")}</p>
        </li>
      )
    }
  }
}

export default SpoopyMessage;
