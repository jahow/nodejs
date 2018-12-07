import React, { Component } from 'react';
import logo from './logo.svg';
import './App.css';
import Map from './Map.js';
class App extends Component {
  render() {
    return (
      <div className="App">
        <header className="map-header">
          <img src={logo} className="App-logo" alt="logo" />
        </header>
        <Map>
        </Map>
      </div>
    );
  }
}

export default App;
