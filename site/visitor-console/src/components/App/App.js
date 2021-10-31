import React, { useState } from 'react';
import ModeSelect from '../ModeSelect/ModeSelect'
import UserForm from '../UserForm/UserForm'

export const STATES = {
  MAIN: 0,
  CLEMSON: 1,
  GUEST: 2
}

const App = () => {

  const [appMode, setAppMode] = useState(STATES["MAIN"])

  const handleClemsonUser = () => {
    // console.log("Clemson User");
    setAppMode(STATES["CLEMSON"]);
  }

  const handleGuestUser = () => {
    // console.log("Guest User");
    setAppMode(STATES["GUEST"]);
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
      <UserForm handleBack={handleBack} mode={appMode}></UserForm>
    )
  } else if (appMode === STATES["GUEST"]) {
    render = (
      <UserForm handleBack={handleBack} mode={appMode}></UserForm>
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