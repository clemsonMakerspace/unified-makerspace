import React from 'react';
import Header from '../Components/Header.js'
import '../App.css';
import MachineAllTasks from '../Components/MachineAllTasks.js';

function MachineEditTasks() {
  return (
    <div className="App" background="#1F1F1F">
      <header className="App-header">
        {Header("Laser Cutter 1")}
      </header>
      <MachineAllTasks/>
      <div style={{paddingTop: 40}}>
      </div>
    </div>
  );
}

export default MachineEditTasks;
