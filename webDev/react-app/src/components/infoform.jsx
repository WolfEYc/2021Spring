import React, { Component } from 'react'
import './info.css';

class NameForm extends Component {
    constructor(props) {
      super(props);
      this.state = {clientid: '', ip: '',port: ''};
      this.handleClientChange = this.handleClientChange.bind(this);
      this.handleIPChange = this.handleIPChange.bind(this);
      this.handlePortChange = this.handlePortChange.bind(this);
      this.handleSubmit = this.handleSubmit.bind(this);
    }
  
    handleClientChange(event) {    this.setState({clientid: event.target.value});  }
    handleIPChange(event) {    this.setState({ip: event.target.value});  }
    handlePortChange(event) {    this.setState({port: event.target.value});  }

    handleSubmit(event) {
      console.log(this.state)
      alert('state: ' + this.state);
      event.preventDefault();
    }
  
    render() {
      return (
        <form onSubmit={this.handleSubmit}>
          
           <label>
            ClientID:
            <input type="text" value={this.state.clientid} onChange={this.handleClientChange} />
           </label>
           <label>
            Server IP:
            <input type="text" value={this.state.ip} onChange={this.handleIPChange} />
           </label>
           <label>
            Port:
            <input type="text" value={this.state.port} onChange={this.handlePortChange} />
           </label>
          
          <input type="submit" value="Connect" />
          <input type="submit" value="Disconnect" />
        </form>
      );
    }
  }

  export default NameForm;
