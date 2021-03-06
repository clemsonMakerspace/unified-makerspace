import React from 'react';
import Header from './Components/Header.js'
import './App.css';
import './Components/Form.css'
import MachineFormContainer from './Components/MachineFormContainer.js';
import MachineFormCompletionContainer from"./Components/MachineFormComplete.js";

class EditMachine extends React.Component {
  constructor(props){
    super(props);
    this.handleClick = this.handleClick.bind(this);
    this.complete= true ;
    this.state = {
      title: "Task Name",
      machine: "Machine Name"
    };
  }

  // componentDidMount () {
  //   console.log(this.props.location.state);
  //   this.setState = this.props.location.state;
  //   console.log(this.props.location.state.title);
  //   this.complete= true ;
  //   this.forceUpdate();
  //
  // }

  handleClick(value){
    this.complete = value;
  }

  render(){
  return (
    <div className="App" background="#1F1F1F">
      <header className="App-header">
        {Header("Edit Machine Details")}
      </header>

      {this.complete ? <MachineFormContainer handleClick={this.handleClick} state={this.props.location.state}/> : <MachineFormCompletionContainer/> }

      <div style={{paddingTop: 40}}>
      </div>
    </div>
  );
  }

}

export default EditMachine;
