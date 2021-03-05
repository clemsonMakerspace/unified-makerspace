import React from 'react';
import clsx from 'clsx';
import { makeStyles } from '@material-ui/core/styles';
import { BrowserRouter as Router, Route, Link } from 'react-router-dom';
import "../App.css";
import Button from '@material-ui/core/Button';
import complete from "../Assets/Complete.png";

const useStyles = makeStyles((theme) => ({
    root: {
        background: 'rgba(236,159,5,1)',
        borderRadius: 5,
        border: 0,
        color: 'white',
        height: 48,
        padding: '0 15px',
        fontFamily: "Helvetica Neue",
            fontStyle: "normal",
            fontWeight: "bold",
        hover: {
            background: 'rgba(236,159,5,1)',
        },
    },

    root2: {
        backgroundColor: "rgba(248,247,247,.5)",
        borderRadius: 5,
        border: 0,
        color: 'white',
        height: 48,
        padding: '0 10%',
        fontFamily: "Helvetica Neue",
            fontStyle: "normal",
            fontWeight: "bold",
        hover: {
            background: 'rgba(236,159,5,1)',
        },
    },
    baseroot:{
        borderStyle: "solid",
        borderColor: "rgba(172,134,150,1)",
        backgroundColor: "rgba(248,247,247,.15)",
        width: '90%',
        margin: "auto",
        borderRadius:"15px",
      },
    title: {
        fontFamily: "Helvetica Neue",
            fontStyle: "normal",
            fontWeight: "bold",
        fontSize: "120%",
        color: "white",
    },
}));



export default function CheckCompletionContainer( ) {
  const classes = useStyles();


  return (
    <div className= {classes.baseroot}>

        <div>
        <h1 style= {{ color:'white', fontSize: "30px", fontWeight: "normal",  fontFamily: "Helvetica Neue", paddingTop: 10 }} >
                Task Complete
        </h1>
        <h1 style= {{ color:'white', fontSize: "40px",  fontFamily: "Helvetica Neue",}} >
                Laser Cutter 1: Clean Lens
        </h1>
        <img src={complete} alt= "" className="Complete-logo" style={{float: "middle"}}/>
        <h1 style= {{ color:'white', fontSize: "35px", fontWeight: "normal",  fontFamily: "Helvetica Neue", paddingTop: 10 }} >
                Success
        </h1>

        <Button component={Link} to="/" className={clsx(classes.root2)}>
            Return to Home
        </Button>
        </div>

        <div style={{height: 20}}/>
    </div>
  )

}
