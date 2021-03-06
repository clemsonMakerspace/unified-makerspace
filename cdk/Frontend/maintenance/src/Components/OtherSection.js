import React from 'react';
import { Link } from 'react-router-dom';
import { makeStyles } from '@material-ui/core/styles';
import List from '@material-ui/core/List';
import ListItem from '@material-ui/core/ListItem';
import Divider from '@material-ui/core/Divider';
import ListItemText from '@material-ui/core/ListItemText';
import ListItemAvatar from '@material-ui/core/ListItemAvatar';
import Avatar from '@material-ui/core/Avatar';
import Typography from '@material-ui/core/Typography';
import ArrowForwardIosIcon from '@material-ui/icons/ArrowForwardIos';

import history from "../Assets/History.png";
import createNewTask from "../Assets/createNewTask.png";
import createNewMachine from "../Assets/createNewMachine.png";
import account from "../Assets/Account.png"

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
      option: 'History',
    },
    {
      option: 'Create New Task',
    },
    {
      option: 'Configure New Machine',
    },
    {
      option: 'Manage Admin Settings',
    },
  ];


export default function UpcomingTasks() {
  const classes = useStyles();
  let LinkValue = '';
  const items = []

  for (const [,value] of DATA.entries()) {
    //this if/else is temporary until we have more pages to link to
    if(value.option === 'History'){
      LinkValue = 'MachineAllTasks';
    }
    else if(value.option === 'Create New Tasks'){
      LinkValue = 'MachineEditTasks';
    }
    else if(value.option === 'Configure New Machine'){
      LinkValue = 'ConfigureNewMachine';
    }
    else{LinkValue = 'MachineUpcomingTasks';}
    items.push(
    <>
          <Link to ={LinkValue}>
          <ListItem alignItems="flex-start" className={classes.root}>
          <ListItemAvatar>
          <Avatar alt={value.occurrence} className={classes.icons} src={IconPicker(value.option)} />
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
    <div style={{paddingTop: 10}}>
    <div className= {classes.baseroot}>
      <h1 style= {{textAlign:"left", color:'white', paddingTop: 10, paddingLeft: 10}} className={classes.title}>
        Other
      </h1>
      <Divider style= {{backgroundColor:"rgba(172,134,150,1)", height: 2, width: "95%", margin: "auto"}}/>
       <List >
       {items}
       </List>

    </div>
    </div>
  )

}

function IconPicker(option){
    if (option === "History"){
        return history;
    }
    else if (option === "Create New Task"){
        return createNewTask;
    }
    else if (option === "Configure New Machine"){
        return createNewMachine;
    }
    else if ( option === 'Manage Admin Settings'){
        return account;
    }
}
