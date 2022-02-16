import React, { Dispatch, ReactElement, SetStateAction, useState } from "react";
import { State, Props } from "../App/App";

const UserForm = (props: Props) => {
  const [userName, setUserName]: [string, Dispatch<SetStateAction<string>>] =
    useState<string>("");
  const [inputError, setInputError]: [
    string,
    Dispatch<SetStateAction<string>>
  ] = useState<string>("");
  const [isLoading, setIsLoading]: [
    boolean,
    Dispatch<SetStateAction<boolean>>
  ] = useState<boolean>(false);

  const handleChange = (event: React.ChangeEvent<HTMLInputElement>): void => {
    setUserName(event.currentTarget.value);
  };

  const handleSubmit = (event: React.FormEvent<HTMLFormElement>): void => {
    if (userName.trim() === "") {
      setInputError(errorMessage);
    } else {
      setInputError("");
      const param = { username: userName };
      fetch("https://api.cumaker.space/visit", {
        method: "post",
        body: JSON.stringify(param),
      }).then((response) => {
        if (response.ok) {
          if (props.handleSignInMessage) props.handleSignInMessage(true);
        } else {
          if (props.handleSignInMessage) props.handleSignInMessage(false);
        }
      });
      setIsLoading(true);
    }
    event.preventDefault();
    setUserName("");
  };

  let title: ReactElement = (
    <h3 className="text-light">
      {props.mode === State.CLEMSON
        ? "Clemson User Login"
        : props.mode === State.GUEST
        ? "Guest User Login"
        : ""}
    </h3>
  );
  let placeholder: string = "";
  let errorMessage: string = "";

  if (props.mode === State.CLEMSON) {
    placeholder = "Username";
    errorMessage = "Please enter your username.";
  } else if (props.mode === State.GUEST) {
    placeholder = "Email Address";
    errorMessage = "Please enter an email address.";
  }

  if (!isLoading) {
    return (
      <div>
        {title}
        <form onSubmit={handleSubmit} className="">
          <div className="form-group mb-3">
            <input
              type={props.mode === State.CLEMSON ? "text" : "email"}
              value={userName}
              onChange={handleChange}
              placeholder={placeholder}
              className="form-control"
            />
            <span className="form-text text-danger d-block">{inputError}</span>
          </div>
          <div className="d-flex justify-content-start">
            <button type="submit" className="btn btn-secondary mr-5">
              Sign In
            </button>
            <button
              className="btn btn-link text-light"
              onClick={props.handleBack}
            >
              Cancel
            </button>
          </div>
        </form>
      </div>
    );
  } else {
    return <h3 className="text-secondary">Loading...</h3>;
  }
};

export default UserForm;
