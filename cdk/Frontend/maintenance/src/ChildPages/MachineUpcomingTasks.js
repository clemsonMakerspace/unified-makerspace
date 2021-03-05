import React from 'react';
import Header from '../Components/Header.js'
import '../App.css';
import UpcomingTasks from '../Components/UpcomingTasks.js';

function MachineUpcomingTasks() {
  return (
    <div className="App" background="#1F1F1F">
      <header className="App-header">
        {Header("Upcoming Tasks")}
      </header>
      <UpcomingTasks/>
      <div style={{paddingTop: 40}}>
      </div>
    </div>
  );
}

export default MachineUpcomingTasks;
