import React from 'react';
import { BrowserRouter as Router, Route, Link } from 'react-router-dom';
import "../App.css";
import home_logo from "../Assets/home.png";
import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import Typography from '@material-ui/core/Typography';
import Button from '@material-ui/core/Button';
import IconButton from '@material-ui/core/IconButton';



function Header ( name ){
 
    return (
        <>
        <AppBar position="static"  style={{ background: '#1F1F1F', boxShadow: 'none' }}>
        <Toolbar >
            <IconButton  component={Link} to="/" edge="start"  color="inherit" aria-label="home">
            <img src={home_logo} className="App-logo" alt=""/>
            </IconButton>
            <Typography variant="h4" style={{fontSize:"xx-large"}} >
            {name}
            </Typography>
            <Button color="inherit" style={{position: 'absolute', right: "10pt"}}>Meg Nuttall</Button>
        </Toolbar>
        </AppBar>
        </>
    );
}

export default Header;
