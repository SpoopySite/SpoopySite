import React, {Component} from "react";
import {withRouter} from "react-router-dom";
import SpoopyMessage from "../spoopy-message/Spoopy-Message";

class Spoopy extends Component {
  constructor(props) {
    super(props);

    this.safe = document.querySelector('#results h2');
    this.list = document.querySelector('#results ol');
    this.heading = document.getElementById('header');
    this.spinner = document.querySelector('.spinner');

    this.state = {spoopy_list: []};
  }

   static getWebSocket() {
    const l = window.location;
    const protocol = l.protocol.endsWith('s:') ? 'wss' : 'ws';
    return `${protocol}://${l.host}`;
  }

  async getData() {
    const suspect_url = decodeURIComponent(this.props.match.params.suspect_url);
    const ws = new WebSocket(`${Spoopy.getWebSocket()}/ws`);

    ws.onopen = function (event) {
      ws.send(suspect_url)
    };
    ws.onmessage = (event) => {
      let item;
      try {
        item = JSON.parse(event.data);
      } catch (err) {
        console.error(err.stack);
        this.safe.innerHTML = err.message;
        return;
      }
      if (item["end"]) {
        this.setState({finished: true});
      } else if (item["error"]) {
        this.state.spoopy_list.push(item);
        this.setState({finished: true});
        // Spoopy.addError(item, this.list, this.spinner);
      } else {
        this.state.spoopy_list.push(item);
        this.setState({finished: false});
        // Spoopy.addResult(item, this.list, this.spinner);
      }

      if (item.chain) {
        this.safe.textContent = item.safe ? 'Safe' : 'Unsafe';
        this.heading.textContent = item.chain[0].url;
        this.setState({finished: true});
      }
    }
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
    const {spoopy_list, finished} = this.state;

    return (
      <div className="wrapper">
        <h1 id="header">{decodeURIComponent(this.props.match.params.suspect_url)}</h1>
        <div id="results">
          <h2>{finished ? null : "Checking if Safe"}</h2>
          <ol>
            <>
              {spoopy_list.map(item => (
                <SpoopyMessage data={item}/>
              ))}
            </>
            {finished ? null :
              <div className="spinner">
                <div className="cube1"></div>
                <div className="cube2"></div>
              </div>}
          </ol>
        </div>
      </div>
    );
  }
}

export default withRouter(Spoopy);
