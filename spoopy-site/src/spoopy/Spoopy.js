import React, { Component } from "react";
import { withRouter } from "react-router-dom";
import SpoopyMessage from "../spoopy-message/Spoopy-Message";
import Spinner from "../spinner/Spinner";
import "./Spoopy.css";

class Spoopy extends Component {
  constructor(props) {
    super(props);

    this.state = { spoopy_list: [] };
  }

  static getWebSocket() {
    const l = window.location;
    let host;
    host = process.env.NODE_ENV === "development" ? "localhost:8282" : l.host;
    const protocol = l.protocol.endsWith("s:") ? "wss" : "ws";
    return `${protocol}://${host}`;
  }

  async getData() {
    const suspect_url = decodeURIComponent(this.props.match.params.suspect_url);
    const ws = new WebSocket(`${Spoopy.getWebSocket()}/ws`);

    ws.onopen = function(event) {
      ws.send(suspect_url);
    };
    ws.onmessage = (event) => {
      let item;
      try {
        item = JSON.parse(event.data);
      } catch (err) {
        console.error(err.stack);
        this.setState({ err });
        return;
      }
      if (item["end"]) {
        this.setState({ finished: true });
      } else if (item["error"]) {
        this.state.spoopy_list.push(item);
        this.setState({ finished: true });
      } else {
        this.state.spoopy_list.push(item);
        this.setState({ finished: false });
      }
    };
  }

  async componentDidMount() {
    try {
      const data = await this.getData();
      this.setState({ data });
    } catch (error) {
      this.setState({ error });
    }
  }

  render() {
    const { spoopy_list, finished, error } = this.state;

    return (
      error ? <div className="status error">{error.message}</div> :
        <div className="spoopy-wrapper">
          <h1 id="header">{decodeURIComponent(this.props.match.params.suspect_url)}</h1>
          <div id="results">
            <h2>{finished ? null : "Checking if Safe"}</h2>
            <ol>
              <>
                {spoopy_list.map(item => (
                  <SpoopyMessage data={item} key={item.url}/>
                ))}
              </>
              {finished ? null :
                <Spinner/>}
            </ol>
          </div>
        </div>
    );
  }
}

export default withRouter(Spoopy);
