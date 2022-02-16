import { useState, Dispatch, SetStateAction, ReactElement } from 'react';
import ModeSelect from '../ModeSelect/ModeSelect'
import UserForm from '../UserForm/UserForm'
import SignInCountDown from '../SignInCountDown/SignInCountDown'
import Registration from '../Registration/Registration';
import NotFoundPage from '../NotFoundPage/NotFoundPage';
import { Routes, Route } from "react-router-dom";
import Footer from '../Footer';

export enum State {
  MAIN,
  CLEMSON,
  GUEST,
  SIGN_IN,
  FAILED_SIGN_IN
}

export interface Props {
  handleClemsonUser?: () => void;
  handleGuestUser?: () => void;
  handleSignInMessage?: (isIn: boolean) => void;
  handleBack?: () => void;
  mode?: State;
}

const App = () => {

  const [appMode, setAppMode]: [State, Dispatch<SetStateAction<State>>] = useState<State>(State.MAIN)

  const handleClemsonUser = (): void => {
    setAppMode(State.CLEMSON);
  }

  const handleGuestUser = (): void  => {
    setAppMode(State.GUEST);
  }

  const handleSignInMessage = (isIn: boolean): void  => {
    isIn ? setAppMode(State.SIGN_IN) : setAppMode(State.FAILED_SIGN_IN)
  }

  const handleBack = (): void  => {
    setAppMode(State.MAIN);
  }


  let render: ReactElement = (
    <ModeSelect 
    handleClemsonUser={handleClemsonUser} 
    handleGuestUser={handleGuestUser}/>
  );
  if (appMode === State.CLEMSON) {
    render = (
      <UserForm handleSignInMessage={handleSignInMessage}
      handleBack={handleBack} mode={appMode}></UserForm>
    )
  } else if (appMode === State.GUEST) {
    render = (
      <UserForm handleSignInMessage={handleSignInMessage}
      handleBack={handleBack} mode={appMode}></UserForm>
    )
  } else if (appMode === State.SIGN_IN) {
    render = (
      <SignInCountDown handleBack={handleBack} mode={appMode}></SignInCountDown>
    )
  } else if (appMode === State.FAILED_SIGN_IN) {
    render = (
      <SignInCountDown handleBack={handleBack} mode={appMode}></SignInCountDown>
    )
  }
  
  return (
    <Routes>
      <Route path="/" element={
        <div className="container bg-primary p-5 rounded" style={{height: "400px"}}>
          <h1 className="text-secondary fw-bold mb-4 text-center">Visit the Makerspace!</h1>
          <div className="d-flex justify-content-center">
            {render}
          </div>
          <Footer />
        </div>
      } />
      <Route path="register" element={<Registration />} />
      <Route path="*" element={<NotFoundPage />}/>
    </Routes>
  )
};

export default App;