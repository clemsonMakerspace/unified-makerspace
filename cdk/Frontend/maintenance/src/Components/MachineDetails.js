import React from 'react';
import { Link } from 'react-router-dom';
import { makeStyles } from '@material-ui/core/styles';
import List from '@material-ui/core/List';
import ListItem from '@material-ui/core/ListItem';
import Divider from '@material-ui/core/Divider';
import ListItemText from '@material-ui/core/ListItemText';
import ListItemAvatar from '@material-ui/core/ListItemAvatar';
import Avatar from '@material-ui/core/Avatar';
import Collapse from '@material-ui/core/Collapse';
import Typography from '@material-ui/core/Typography';
import ExpandMore from '@material-ui/icons/ExpandMore';
import ArrowForwardIosIcon from '@material-ui/icons/ArrowForwardIos';
import MachinePage from '../ChildPages/MachinePage.js'

import Taz from "../Assets/Taz.png";
import Mini from "../Assets/Mini.png";
import Cutter from "../Assets/laserCutter.png";

const useStyles = makeStyles((theme) => ({
  root: {
    width: '85%',
    borderRadius: "15px",
    alignSelf: "center",
    justifyContent: 'center',
    margin: "auto ",
    backgroundColor: "rgba(248,247,247,.5)",
  },
  baseroot:{
    borderStyle: "solid",
    borderColor: "rgba(172,134,150,1)",
    width: '90%',
    margin: "auto",
    borderRadius:"15px",
  },
  title: {
    fontFamily: "Helvetica Neue",
		fontStyle: "normal",
		fontWeight: "bold",
    fontSize: "24px",
    color: "white",
  },
  arrowIcons:{
    margin: "auto",
    color: "white",
    width: theme.spacing(5),
    height: theme.spacing(5),
  },
  icons:{
    width: theme.spacing(7),
    height: theme.spacing(7),
  },
  inline: {
    fontFamily: "Helvetica Neue",
		fontStyle: "normal",
    display: 'inline',
    color: 'white',
  },
  img: {
    width: '400px',
    height: '400px',
    textAlign: "center",
  },
}));

//this next line is obviously temporary until we figure out how to pass the machine type to the machine page
const MachineType = "Laser Cutter";

function IconPicker(MachineType){
    if (MachineType === "Laser Cutter"){
        return Cutter;
    }
    else if (MachineType === "3D Printers: Mini"){
        return Mini;
    }
    else
        return Taz;
}

export default function MachineDetails() {
  const classes = useStyles();

  const items = [];

  return (
    < >
    <div>
      <div style={{paddingTop: 10}}>
        <div style= {{alignItems:"center", justifyContent:"center", color:'white', paddingTop: 10}}>
          <img src={IconPicker(MachineType)} style={{width: "300px"}}/>
        </div>
        <h1 style= {{textAlign:"center", color:'white', paddingTop: 10}}>
          {MachineType}
        </h1>
      </div>
    </div>
    </>
  )

}
