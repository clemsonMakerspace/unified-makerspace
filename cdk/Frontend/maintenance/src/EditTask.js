import React from 'react';
import Header from './Components/Header.js';

import './App.css';

import TaskFormContainer from './Components/TaskFormContainer.js';
import TaskFormCompletionContainer from"./Components/TaskFormComplete.js";

class EditTask extends React.Component{
  constructor(props){
    super(props);
    this.handleClick = this.handleClick.bind(this);
    this.complete= true ;
    this.state = {
      title: "Task Name",
      machine: "Machine Name"
    };
  }

  componentDidMount () {
    console.log(this.props.location.state);
    this.setState = this.props.location.state;
    console.log(this.props.location.state.title);
    this.complete= true ;
    this.forceUpdate();

  }
  handleClick(value){
    this.complete = value;
  }

  render(){
  return (
    <div className="App" background="#1F1F1F">
        <header className="App-header">
          {Header(this.state.title ? this.state.title : "Header")}
        </header>

      {this.complete ? <TaskFormContainer handleClick={this.handleClick} state={this.props.location.state}/> : <TaskFormCompletionContainer/> }


        <div style={{paddingTop: 40}}>
        </div>
    </div>
  );}

}

export default EditTask;
