import React, { useState } from 'react';
import ModeSelect from '../ModeSelect/ModeSelect'
import UserForm from '../UserForm/UserForm'
import SignInCountDown from '../SignInCountDown/SignInCountDown'

export const STATES = {
  MAIN: "MAIN",
  CLEMSON: "CLEMSON",
  GUEST: "GUEST",
  SIGN_IN: "SIGN_IN",
  FAILED_SIGN_IN: "FAILED_SIGN_IN"
}

const App = () => {

  const [appMode, setAppMode] = useState(STATES["MAIN"])

  const handleClemsonUser = () => {
    setAppMode(STATES["CLEMSON"]);
  }

  const handleGuestUser = () => {
    setAppMode(STATES["GUEST"]);
  }

  const handleSignInMessage = (isIn) => {
    isIn ? setAppMode(STATES["SIGN_IN"]) : setAppMode(STATES["FAILED_SIGN_IN"])
  }

  const handleBack = () => {
    setAppMode(STATES["MAIN"]);
  }



  let render;
  if (appMode === STATES["MAIN"]) {
    render = (
      <ModeSelect 
        handleClemsonUser={handleClemsonUser} 
        handleGuestUser={handleGuestUser}>
      </ModeSelect>
    )
  } else if (appMode === STATES["CLEMSON"]) {
    render = (
      <UserForm handleSignInMessage={handleSignInMessage}
      handleBack={handleBack} mode={appMode}></UserForm>
    )
  } else if (appMode === STATES["GUEST"]) {
    render = (
      <UserForm handleSignInMessage={handleSignInMessage}
      handleBack={handleBack} mode={appMode}></UserForm>
    )
  } else if (appMode === STATES["SIGN_IN"]) {
    render = (
      <SignInCountDown handleBack={handleBack} mode={appMode}></SignInCountDown>
    )
  } else if (appMode === STATES["FAILED_SIGN_IN"]) {
    render = (
      <SignInCountDown handleBack={handleBack} mode={appMode}></SignInCountDown>
    )
  }

  return (
    <div className="container bg-primary p-5 rounded" style={{height: "400px"}}>
      <h1 className="text-secondary fw-bold mb-4 text-center">Visit the Makerspace!</h1>
      <div className="d-flex justify-content-center">
        {render}
      </div>
    </div>
  )
};

export default App;