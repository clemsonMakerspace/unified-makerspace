import React from 'react';
import Header from './Components/Header.js';

import './App.css';

import TaskCompletionContainer from './Components/CompleteTaskContainer.js';
import CheckCompletionContainer from"./Components/CompleteCheck.js";

class CompleteTask extends React.Component{
  constructor(props){
    super(props);
    this.handleClick = this.handleClick.bind(this);
    this.complete= true ;
    this.state = {
      title: "Task Name",
      machine: "Machine Name"
    };
  }
  
  componentDidMount = () => {
    this.setState({title: this.props.location.state.title, machine: this.props.location.state.machine });

    this.complete= true ;
    this.forceUpdate();
  
  }
  handleClick(value){
    this.complete = value; 
    this.setState.title = "words";
  }

  render(){
  return (
    <div className="App" background="#1F1F1F">
        <header className="App-header">
          {Header(this.state.machine ? this.state.machine: "Header")}
        </header>

      {this.complete ? <TaskCompletionContainer handleClick={this.handleClick} state={this.props.location.state}/> : <CheckCompletionContainer/> }
       

        <div style={{paddingTop: 40}}>
        </div>
    </div>
  );}

}

export default CompleteTask;