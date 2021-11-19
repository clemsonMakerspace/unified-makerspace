import React from 'react';
import ReactDOM from 'react-dom';
import './styles/style.scss';
import App from './components/App/App';
import bg from './asset/background.webp'
import logo from './asset/makerspace_logo.webp'
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Registration from './components/Registration/Registration';

document.body.className="bg-dark";

ReactDOM.render(
  <React.StrictMode>
    <div style={{backgroundImage: `url(${bg})`, height: "100%"}}>
    <img src={logo} />
    <Router>
      <Routes>
        <Route path="/register" element={<Registration />}/>
        <Route path="*" element={<App />}/>
      </Routes>
    </Router>
    </div>
  </React.StrictMode>,
  document.getElementById('root')
);