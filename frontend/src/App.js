import React, { Component } from "react";
import "./App.css";
import axios from "axios";

class App extends Component {
  state = {
    input: "",
    isLoading: true,
    code: "",
    buyDate: "",
    sellDate: "",
    profit: 0.0,
  };
  getCode = (e) => {
    this.setState({
      input: e.target.value,
    });
  };
  getAPI = async () => {
    const { input } = this.state;
    const response = await axios.get(
      "http://localhost:8000/api/?code=" + input
    );
    this.setState({
      code: input,
      buyDate: response.data["buy date"],
      sellDate: response.data["sell date"],
      profit: response.data["profit"],
      isLoading: false,
    });
  };
  render() {
    const { input, isLoading, code, buyDate, sellDate, profit } = this.state;
    const { getCode, getAPI } = this;
    return (
      <div className="App">
        <div className="App-header">
          <input
            type="text"
            placeholder="Code"
            value={input}
            onChange={getCode}
          />
          <button onClick={getAPI}> Search </button>
        </div>
        <section className="container">
          {isLoading ? (
            <h2> Enter Code! </h2>
          ) : (
            <div className="result">
              <h2> Code: {code} </h2>
              <h2> Buy date: {buyDate} </h2>
              <h2> Sell date: {sellDate} </h2>
              <h2> Profit: {profit.toFixed(5)}$ </h2>
            </div>
          )}
        </section>
      </div>
    );
  }
}

export default App;
