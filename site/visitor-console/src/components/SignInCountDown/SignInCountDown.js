import React from 'react';
import Countdown from 'react-countdown';

const SignInCountDown = (props) => {
    const renderer = ({seconds}) => (
        <div className="bg-white w-50 rounded text-center">
        <p>Sign In {props.mode === 3 ? "Successful" : "Failed"}</p>
        <button onClick={props.handleBack}>Return to Homepage Immediately</button>
        <p>Return in {seconds}</p>
        </div>
      );

    return (
        <Countdown date={Date.now() + 5000} renderer={renderer} onComplete={props.handleBack} on />
    );
}
 
export default SignInCountDown;
