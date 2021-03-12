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
import Header from '../Components/Header.js'
import '../App.css';
import UpcomingTasks from '../Components/UpcomingTasks.js';
import MachineDetails from '../Components/MachineDetails.js';
import MachineUpcomingTasks from './MachineUpcomingTasks.js';
import MachineAllTasks from '../Components/MachineAllTasks.js';
import MachineEditTasks from './MachineEditTasks.js';
import ConfigureNewMachine from '../ConfigureNewMachine.js';
import EditTask from '../EditTask.js';

import Taz from "../Assets/Taz.png";
import Mini from "../Assets/Mini.png";
import cutter from "../Assets/laserCutter.png";

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
}));

const DATA = [
    {
      option: 'Upcoming Tasks',
    },
    {
      option: 'History',
    },
    {
      option: 'Edit Tasks',
    },
    {
      option: 'Create New Task',
    },
    {
      option: 'Edit Machine Details',
    },
];

function MachineOptionsList( type,list){
  const classes = useStyles();

  const [open, setOpen] = React.useState(false);

  const handleClick = () => {
      setOpen(!open);
      console.log(open);
  };

  const items = []
  let LinkValue = '';

  for (const [,value] of DATA.entries()) {
    //this if/else is temporary until we have more pages to link to
    if(value.option === 'Edit Tasks'){
      LinkValue = '/MachineEditTasks';
    }
    else if(value.option === 'Edit Machine Details'){
      LinkValue = '/EditMachine';
    }
    else{LinkValue = '/MachineUpcomingTasks';}
    items.push(
    <>
          <Link to ={LinkValue}>
          <ListItem alignItems="flex-start" onClick={handleClick} className={classes.root}>
          <ListItemAvatar>
          <Avatar alt={value.option} className={classes.icons} src={type} />
          </ListItemAvatar>
          <ListItemText style= {{margin: 'auto', paddingLeft: "5px"}}

            primary= {
            <Typography
              component="span"
              className={classes.title}
            >
            {value.option}
            </Typography>

            }
          />
          <ArrowForwardIosIcon className={classes.arrowIcons}/>
        </ListItem >
        </Link>
        <Divider variant="inset" component="li" style={{
      paddingBottom: 10, backgroundColor: "transparent"}}  />
        </>
    )
  }

  return (
       <List >
       {items}
       </List>

  )
}

function MachinePage() {
  return (
    <div className="App" background="#1F1F1F">
      <header className="App-header">
        {Header("Makerspace")}
      </header>
      <MachineDetails/>
      <MachineOptionsList/>
      <div style={{paddingTop: 40}}>
      </div>
    </div>
  );
}

export default MachinePage;
