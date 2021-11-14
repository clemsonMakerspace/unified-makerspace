import React, { useState } from 'react';
import { State, Props } from '../App/App'


const UserForm = (props: Props) => {
  const [userName, setUserName] = useState("");
  const [inputError, setInputError] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  const handleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setUserName(event.currentTarget.value);
  }

  const handleSubmit = (event: React.FormEvent<HTMLFormElement>) => {
    if (userName.trim() === "") {
      setInputError(errorMessage);
    } else {
      setInputError("");
      const param = {username: userName};
      fetch("https://api.cumaker.space/visit", {
        method:"post",
        body:JSON.stringify(param)
      }).then(response => {
        if (response.ok) {
          if (props.handleSignInMessage) props.handleSignInMessage(true);
        } else {
          if (props.handleSignInMessage) props.handleSignInMessage(false);
        }
      }).catch(error => {if (props.handleSignInMessage) props.handleSignInMessage(false)});
      setIsLoading(true);
    }
    event.preventDefault()
    setUserName("");
  }

  let title;
  let placeholder;
  let errorMessage: string;
  
  if (props.mode === State.CLEMSON) {
    title = <h3 className="text-light">Clemson User Login</h3>;
    placeholder = "Username";
    errorMessage = "Please enter your username.";
  } else if (props.mode === State.GUEST) {
    title = <h3 className="text-light">Guest User Login</h3>;
    placeholder = "Email Address"
    errorMessage = "Please enter an email address."
  }

  if (!isLoading) {
    return (
      <div>
        {title}
        <form onSubmit={handleSubmit} className="">
          <div className="form-group mb-3">
            <input type={(props.mode === State.CLEMSON ? "text" : "email")} 
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