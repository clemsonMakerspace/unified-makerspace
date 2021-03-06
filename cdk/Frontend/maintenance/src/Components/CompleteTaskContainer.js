import React from 'react';
import clsx from 'clsx';
import { makeStyles } from '@material-ui/core/styles';
import { BrowserRouter as Router, Route, Link } from 'react-router-dom';
import "../App.css";
import "./CompleteTask.css";
import Button from '@material-ui/core/Button';
import nightly from "../Assets/nightly.png";


class TaskCompletionContainer extends React.Component {
    constructor(props){
        super(props);
        this.state={title: "name", machine: "machine name"};
    }

    componentDidMount = () => {
        this.setState({title: this.props.state.title, machine: this.props.state.machine});
        this.forceUpdate();
    }

    render(){

        return (
          <div className= {"baseroot"}>

              <div style={{visibility: "visible" }}>
              <div  style={{display: "flex", flexDirection: "row", width: "80%", margin:"auto"}}>
                  <img src={nightly} alt="" className="Event-logo"/>

                  <div style={{display: "flex", flexDirection: "column"}}>
                      <h1 style= {{textAlign:"left", color:'white', paddingTop: 10, paddingLeft: 10}} className={"title"}>
                      Task: {this.state.title}
                      </h1>
                      <h1 style= {{textAlign:"left", color:'white',  paddingLeft: 10}} className={"title"}>
                      Machine: {this.state.machine}
                      </h1>
                      <h2 style= {{textAlign:"left", color:'white',  paddingLeft: 10}} className={"title"}>
                      Required Completetion Date: {}
                      </h2>
                  </div>
                  </div>

                  <h3 style={{textAlign:"left", paddingLeft: "7%", color:'white', fontWeight:"italic" }}>
                  Description: Using a Microfiber cloth wipe remove build up from the laser cutter lens 
                  </h3>

                  <Button component={Link} to="/completeTask" onclick={this.props.handleClick(false)} className={clsx("root")}>
                  Mark Complete
                  </Button>

                  <div style={{height: 20}}/>
              </div>

          </div>
        );
        }

}
export default TaskCompletionContainer;
