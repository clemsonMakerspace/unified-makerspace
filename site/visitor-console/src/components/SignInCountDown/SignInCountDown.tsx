import { State, Props } from "../App/App";
import Countdown from "react-countdown";
import { ReactElement } from "react";

const SignInCountDown = (props: Props) => {
  const renderer = (): ReactElement => (
    <div className="container p-3 text-center">
      <h3 className="text-light">
        Sign-in {props.mode === State.SIGN_IN ? "Successful" : "Failed"}
      </h3>
      <button className="btn btn-secondary" onClick={props.handleBack}>
        Continue
      </button>
    </div>
  );

  return (
    <Countdown
      date={Date.now() + 10000}
      renderer={renderer}
      onComplete={props.handleBack}
    />
  );
};

export default SignInCountDown;
