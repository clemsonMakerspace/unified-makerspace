import React, { useState } from 'react';
import { STATES } from '../App/App'

const UserForm = (props) => {
  const [userName, setUserName] = useState("");
  const [inputError, setInputError] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const handleChange = (event) => {
    // console.log(event);
    setUserName(event.target.value);
  }

  const handleSubmit = (event) => {
    // console.log(event);
    if (userName.trim() === "") {
      setInputError(errorMessage);
    } else {
      setInputError("");
      // TODO: API call, display sign-in message, redirect
      // API endpoint here
      fetch("https://p9r4g2xnw4.execute-api.us-east-1.amazonaws.com/prod/visit", {
        method:"post"
      }).then(response => {
        return response.json();
      }).then(data => {
        // success
        console.log("Success: ", data);
        props.handleSignInMessage(true);
      }).catch(error => {
        // error
        console.log("Error: ", error);
        props.handleSignInMessage(false);
      })
      setIsLoading(true);
    }
    event.preventDefault()
    setUserName("");
  }

  let render;
  let placeholder;
  let errorMessage;
  
  if (props.mode === STATES["CLEMSON"]) {
    render = <h3 className="text-light">Clemson User Login</h3>;
    placeholder = "Username";
    errorMessage = "Please enter your username.";
  } else if (props.mode === STATES["GUEST"]) {
    render = <h3 className="text-light">Guest User Login</h3>;
    placeholder = "Email Address"
    errorMessage = "Please enter an email address."
  }

  if (!isLoading) {
    return (
      <div>
        {render}
        <form onSubmit={handleSubmit} className="">
          <div className="form-group mb-3">
            <input type={(props.mode === STATES["CLEMSON"] ? "text" : "email")} 
            value={userName} 
            onChange={handleChange} 
            placeholder={placeholder}
            className="form-control"/>
            <span className="form-text text-danger d-block">{inputError}</span>
          </div>
          <div className="d-flex justify-content-start">
            <button type="submit" className="btn btn-secondary mr-5">Sign In</button>
            <button className="btn btn-link text-light" onClick={props.handleBack}>Cancel</button>
          </div>
        </form>
        
      </div>
    );
  } else {
    return (
      <h3 className="text-secondary">
          Loading...
      </h3>
    );
  }
};

export default UserForm;