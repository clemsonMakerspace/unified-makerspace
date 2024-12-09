import React from "react";
import ReactDOM from "react-dom";
import { Link, BrowserRouter as Router } from "react-router-dom";
import "./styles/global.scss";
import App from "./pages/App";
import background_image from "./assets/background.png";
import logo from "./assets/makerspace_logo.webp";

document.body.className = "bg-dark";

ReactDOM.render(
  <React.StrictMode>
    <div
      className="pb-5"
      style={{
        backgroundImage: `url(${background_image})`,
        backgroundAttachment: "fixed",
        backgroundSize: "cover",
        backgroundPosition: "center",
        minHeight: "100vh",
        width: "100%",
      }}
    >
      <div className="d-flex w-full justify-content-between pt-4 px-4 pb-5">
        <a href="/">
          <img
            src={logo}
            style={{ maxWidth: "100%" }}
            alt="Clemson Makerspace Logo"
          />
        </a>
      </div>
      <App />
    </div>
  </React.StrictMode>,
  document.getElementById("root")
);
