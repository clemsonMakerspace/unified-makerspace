import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import List from '@material-ui/core/List';
import ListItem from '@material-ui/core/ListItem';
import Divider from '@material-ui/core/Divider';
import ListItemText from '@material-ui/core/ListItemText';
import ListItemAvatar from '@material-ui/core/ListItemAvatar';
import Avatar from '@material-ui/core/Avatar';
import Typography from '@material-ui/core/Typography';
import ArrowForwardIosIcon from '@material-ui/icons/ArrowForwardIos';
import {  useHistory } from 'react-router-dom';
import { BrowserRouter as Router, Route, Link } from 'react-router-dom';
import "../App.css";
import "./upcomingTasks.css";

import nightly from "../Assets/nightly.png";

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
      id: 'bd7acbea-c1b1-46c2-aed5-3ad53abb28ba',
      machine: 'Laser Cutter 1',
      title: 'Clean Lens',
      date: "Oct 21st",
      time: "9 PM",
      occurance: "nighty",
      
    },
    {
      id: '3ac68afc-c605-48d3-a4f8-fbd91aa97f63',
      machine: 'Laser Cutter 2',
      title: 'Clean Lens',
      date: "Oct 21st ",
      time: "9 PM",
      occurance: "nighty",
    },
    {
      id: '58694a0f-3da1-471f-bd96-145571e29d72',
      machine: 'Laser Cutter 3',
      title: 'Clean Lens',
      date: "Oct 21st",
      time: "9 PM",
      occurance: "nighty",
    },
  ];


function taskContainer(value, classes){
  
  return(<>
            <Link style={{textDecoration: 'none'}} to={{pathname:"/completeTask",
           state:{
             title: "Clean Lens",
             machine: "Laser Cutter 1",
           }}}  >
            <ListItem  alignItems="flex-start" className={classes.root}>
            <ListItemAvatar>
            <Avatar alt={value.occurance} className={classes.icons} src={nightly} />
            </ListItemAvatar>
            <ListItemText style= {{margin: 'auto', paddingLeft: "5px"}}
              
              primary= {
              <Typography
                component="span"
                className={classes.title}
              >
              {value.machine+": "+ value.title}
              </Typography>
              
              }
              secondary={
                <React.Fragment>
                  <Typography
                    component="span"
                    variant="body2"
                    className={classes.inline}
                    color="textPrimary"
                    
                  >
                  {"Complete By: "+value.time + " on "+ value.date}
                  </Typography>
                </React.Fragment>
              }
            />
            <ArrowForwardIosIcon className={classes.arrowIcons}/>
          </ListItem >
          
          <Divider variant="inset" component="li" style={{
        paddingBottom: 10, backgroundColor: "transparent"}}  />
           </Link>
           </>);
}

export default function UpcomingTasks() {
  const classes = useStyles();

  const items = [];

  const handleClick = () => <Link  to="/completeTask" />;
  const history = useHistory();

  for (const [,value] of DATA.entries()) {
    items.push(
        taskContainer(value, classes, handleClick)
    )
  }

  return (
    <div className= {classes.baseroot}>
      <h1 style= {{textAlign:"left", color:'white', paddingTop: 10, paddingLeft: 10}} className={classes.title}>
        Upcoming Tasks
      </h1>
      <Divider style= {{backgroundColor:"rgba(172,134,150,1)", height: 2, width: "95%", margin: "auto"}}/>
       <List >
       {items}
       </List>
    
    </div>
  )

}

