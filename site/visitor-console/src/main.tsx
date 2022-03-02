import React from "react";
import ReactDOM from "react-dom";
import { BrowserRouter as Router } from "react-router-dom";

import "./styles/global.scss";
import App from "./pages/App";
import background_image from "./assets/background.webp";
import logo from "./assets/makerspace_logo.webp";

document.body.className = "bg-dark";

ReactDOM.render(
  <React.StrictMode>
    <div
      className="pb-5"
      style={{
        backgroundImage: `url(${background_image})`,
        backgroundSize: "cover",
        minHeight: "100%",
      }}
    >
      <div className="w-full pt-4 ps-4 pb-5">
        <img
          src={logo}
          style={{ maxWidth: "100%" }}
          alt="Clemson Makerspace Logo"
        />
      </div>
      <Router>
        <App />
      </Router>
    </div>
  </React.StrictMode>,
  document.getElementById("root")
);
