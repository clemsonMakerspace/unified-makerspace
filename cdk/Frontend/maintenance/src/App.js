import React from 'react';
import Header from './Components/Header.js'
import './App.css';
import UpcomingTasks from './Components/UpcomingTasks.js';
import MachineLists from './Components/MachinesList.js';
import OtherSection from './Components/OtherSection.js';

function App() {
  return (
    <div className="App" background="#1F1F1F">
      <header className="App-header">
        {Header("Makerspace")}
      </header>
      <UpcomingTasks/>
      <MachineLists/>
      <OtherSection/>
      <div style={{paddingTop: 40}}>
      </div>
    </div>
  );
}

export default App;
