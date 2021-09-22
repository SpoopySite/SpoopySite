import React, { Component } from "react";
import { withRouter } from "react-router-dom";
import SpoopyMessage from "../spoopy-message/Spoopy-Message";
import Spinner from "../spinner/Spinner";
import Container from "@mui/material/Container";
import Typography from "@mui/material/Typography";
import List from "@mui/material/List";

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
        <Container>
          <Typography
            variant="h3"
            component="h1"
            align="center"
            id="header"
            style={{wordBreak: "break-word"}}
          >
            {decodeURIComponent(this.props.match.params.suspect_url)}
          </Typography>
          <Container>
            <Typography variant="h5" component="h2">{finished ? null : "Checking if Safe"}</Typography>
            <List>
              {spoopy_list.map(item => (
                <SpoopyMessage data={item} key={item.url}/>
              ))}
              {finished ? null :
                <Spinner/>}
            </List>
          </Container>
        </Container>
    );
  }
}

export default withRouter(Spoopy);
