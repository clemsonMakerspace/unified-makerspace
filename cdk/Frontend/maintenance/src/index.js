import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import {
  Route,
  BrowserRouter as Router,
  Switch
} from "react-router-dom";
import CompleteTask from './CompleteTask';
import MachinePage from './ChildPages/MachinePage'
import MachineUpcomingTasks from './ChildPages/MachineUpcomingTasks'
import MachineEditTasks from './ChildPages/MachineEditTasks'
import MachineAllTasks from './Components/MachineAllTasks'
import EditMachine from './EditMachine'
import ConfigureNewMachine from './ConfigureNewMachine'
import EditTask from './EditTask.js';
import App from './App';
import * as serviceWorker from './serviceWorker';

const routing = (
  <Router>
      <Switch>
        <Route exact path="/" component={App} />
        <Route path="/completeTask" render={(props) => (
              <CompleteTask {...props} isAuthed={true} />
            )}/>
        <Route path="/EditTask" render={(props) => (
              <EditTask {...props} isAuthed={true} />
            )}/>
        <Route path="/MachinePage" component={MachinePage} />
        <Route path="/MachineUpcomingTasks" component={MachineUpcomingTasks} />
        <Route path="/MachineAllTasks" component={MachineAllTasks} />
        <Route path="/MachineEditTasks" component={MachineEditTasks} />
        <Route path="/EditMachine" component={EditMachine} />
        <Route path="/ConfigureNewMachine" component={ConfigureNewMachine} />
      </Switch>
  </Router>
)

ReactDOM.render(
  routing, document.getElementById("root")
);

// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://bit.ly/CRA-PWA
serviceWorker.unregister();
