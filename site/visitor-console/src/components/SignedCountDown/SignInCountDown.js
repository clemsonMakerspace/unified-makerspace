import React from 'react';

const SignedInCountDown = (props) => {
    let sec = 3;
    const countDown = () => {
        if (sec >= 0) document.getElementById("timer").innerHTML = `Return To Homepage In ${sec--}`;
        else {
            clearInterval(interval)
            props.handleBack();
        }
    }
    let interval = setInterval(countDown, 1000)

    console.log(props.mode)
    
    if (props.mode === 3) {
        return (
            <div className="bg-white w-50 rounded text-center">
                <p>Sign In Successful</p>
                <p id="timer"></p>
            </div>
        )
    }
    return (
        <div className="bg-white w-50 rounded text-center">
            <p>Sign In Unsuccessful</p>
            <p id="timer"></p>
        </div>
    )
}
 
export default SignedInCountDown;
