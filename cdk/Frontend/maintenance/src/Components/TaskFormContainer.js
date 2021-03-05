import React from 'react';
import clsx from 'clsx';
import { makeStyles } from '@material-ui/core/styles';
import { BrowserRouter as Router, Route, Link } from 'react-router-dom';
import "../App.css";
import "./Form.css";
import Button from '@material-ui/core/Button';


class TaskFormContainer extends React.Component {

    render(){

        return (
          <div className= {"baseroot"}>

              <div style={{visibility: "visible" }}>
              <div  style={{display: "flex", flexDirection: "row", width: "80%", margin:"auto"}}>

<div class="container">
  <form action="action_page.php">
    <div class="row">
      <div class="col-25">
        <label for="TaskName">Task Name</label>
      </div>
      <div class="col-75">
        <input type="text" id="TaskName" name="TaskName" placeholder="Task name..."/>
      </div>
    </div>
    <div class="row">
      <div class="col-25">
        <label for="MachineName">Machine Name</label>
      </div>
      <div class="col-75">
        <input type="text" id="MachineName" name="MachineName" placeholder="Machine name..."/>
      </div>
    </div>
    <div class="row">
      <div class="col-25">
        <label for="CompletionTime">Completetion Time</label>
      </div>
      <div class="col-75">
        <select id="CompletionTime" name="CompletionTime">
          <option value="endofshift">7:00 pm (end of shift)</option>
          <option value="endofday">11:59 pm (end of day)</option>
        </select>
      </div>
    </div>
    <div class="row">
      <div class="col-25">
        <label for="Frequency">Frequency</label>
      </div>
      <div class="col-75">
        <select id="Frequency" name="Frequency">
          <option value="once">Once</option>
          <option value="nightly">Nightly</option>
          <option value="weekly">Weekly</option>
          <option value="monthly">Monthly</option>
        </select>
      </div>
    </div>
    <div class="row">
      <div class="col-25">
        <label for="StartDate">Start Date</label>
      </div>
      <div class="col-75">
        <select id="StartDate" name="StartDate">
          <option value="today">Today</option>
          <option value="other">Other?</option>
        </select>
      </div>
    </div>
    <div class="row">
      <div class="col-25">
        <label for="Description">Description</label>
      </div>
      <div class="col-75">
        <textarea id="Description" name="Description" placeholder="Description..." style={{height: 200}}></textarea>
      </div>
    </div>
    <br></br>
    <div class="row">
      <saveChanges>
      <Button component={Link} to="/EditTask" onclick={this.props.handleClick(false)} className={clsx("root")}>
      Save Changes
      </Button>
      </saveChanges>
    </div>
  </form>
</div>
              </div>

            <div style={{height: 20}}/>
          </div>

        </div>
        );
        }

}
export default TaskFormContainer;
