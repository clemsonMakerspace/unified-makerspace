import React from 'react';
import ReactDOM from 'react-dom';
import './styles/style.scss';
import App from './components/App/App';

document.body.className="bg-dark";

ReactDOM.render(
  <React.StrictMode>
    <App></App>
  </React.StrictMode>,
  document.getElementById('root')
);