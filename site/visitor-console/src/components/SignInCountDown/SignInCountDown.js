import React from 'react';
import Countdown from 'react-countdown';

const SignInCountDown = (props) => {
    const renderer = ({seconds}) => (
        <div className="container p-3 text-center">
        <h3 className="text-light">Sign-in {props.mode === 3 ? "Successful" : "Failed"}</h3>
        <button className="btn btn-secondary" onClick={props.handleBack}>Continue</button>
        </div>
      );

    return (
        <Countdown date={Date.now() + 10000} renderer={renderer} onComplete={props.handleBack} on />
    );
}
 
export default SignInCountDown;
