import React from "react";
import ReactDOM from "react-dom";
import "./styles/style.scss";
import App from "./components/App/App";
import background_image from "./asset/background.webp";
import logo from "./asset/makerspace_logo.webp";
import { BrowserRouter as Router } from "react-router-dom";

document.body.className = "bg-dark";

ReactDOM.render(
  <React.StrictMode>
    <div
      className="pb-4"
      style={{
        backgroundImage: `url(${background_image})`,
        backgroundSize: "cover",
        minHeight: "100%",
      }}
    >
      <div className="w-full p-4">
        <img src={logo} style={{ maxWidth: "100%" }} />
      </div>
      <Router>
        <App />
      </Router>
    </div>
  </React.StrictMode>,
  document.getElementById("root")
);
