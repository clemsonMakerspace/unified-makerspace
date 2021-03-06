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
      id: 'bd7acbea-c1b1-46c2-aed5-3ad53abb28ba',
      machineType: 'Laser Cutters',
      machineName: [{
            Name: "Laser Cutter 1",
            SKU: "bd7acbea-c1b1-46c2-aed5-3ad53", //Temporary for now
        },
        {
            Name: "Laser Cutter 2",
            SKU: "bd7acbea-c1b1-46c2-aed5-3ad53", //Temporary for now
        },
        {
            Name: "Laser Cutter 3",
            SKU: "bd7acbea-c1b1-46c2-aed5-3ad53", //Temporary for now
        },
    ],
},
{
    id: 'bd7acbea-c1b1-46c2-aed5-3ad53abb28ba',
    machineType: '3D Printers: Mini',
    machineName: [{
          Name: "Mini 1",
          SKU: "bd7acbea-c1b1-46c2-aed5-3ad53", //Temporary for now
      },
      {
          Name: "Mini 2",
          SKU: "bd7acbea-c1b1-46c2-aed5-3ad53", //Temporary for now
      },
      {
          Name: "Mini 3",
          SKU: "bd7acbea-c1b1-46c2-aed5-3ad53", //Temporary for now
      },
      {
        Name: "Mini 4",
        SKU: "bd7acbea-c1b1-46c2-aed5-3ad53", //Temporary for now
      },
      {
        Name: "Mini 5",
        SKU: "bd7acbea-c1b1-46c2-aed5-3ad53", //Temporary for now
      },
  ],
},
  ];

function MachineDropDown( type,list){
  const classes = useStyles();

  const [open, setOpen] = React.useState(false);

  const handleClick = () => {
      setOpen(!open);
      console.log(open);
  };

  const items = []

  for (const [,value] of list.entries()) {
    items.push(
    <>
          <Link to ='/MachinePage'>
          <ListItem alignItems="flex-start" onClick={handleClick} className={classes.root}>
          <ListItemAvatar>
          <Avatar alt={value.occurance} className={classes.icons} src={type} />
          </ListItemAvatar>
          <ListItemText style= {{margin: 'auto', paddingLeft: "5px"}}

            primary= {
            <Typography
              component="span"
              className={classes.title}
            >
            {value.Name}
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

function IconPicker( machineType){
    if (machineType === "Laser Cutters"){
        return cutter;
    }
    else if ( machineType === "3D Printers: Mini"){
        return Mini;
    }
    else
        return Taz;

}

function MachineContainer( value){
const classes = useStyles();

const [open, setOpen] = React.useState(false);

const handleClick = () => {
    setOpen(!open);
    console.log(open);
};

return ( <>
    <div className={classes.root}>
    <ListItem alignItems="flex-start"  onClick={handleClick}>
    <ListItemAvatar>
    <Avatar alt={value.occurance} className={classes.icons} src={ IconPicker(value.machineType)} />
    </ListItemAvatar>
    <ListItemText style= {{margin: 'auto', paddingLeft: "5px"}}

      primary= {
      <Typography
        component="span"
        className={classes.title}
      >
      {value.machineType}
      </Typography>

      }
    />
    <ExpandMore className={classes.arrowIcons}/>

  </ListItem >

  <Collapse in={open} timeout="auto" unmountOnExit>
  <List component="div" disablePadding>
   {MachineDropDown(IconPicker(value.machineType), value.machineName )};
  </List>
  </Collapse>

  </div>
  <Divider variant="inset" component="li" style={{
paddingBottom: 10, backgroundColor: "transparent"}}  />
  </>);

}
export default function MachinesList() {
  const classes = useStyles();

  const items = [];

  for (const [,value] of DATA.entries()) {
    items.push(
        MachineContainer(value)
    )
  }

  return (
    < >
    <div style={{paddingTop: 10}}>
    <div className= {classes.baseroot} >
      <h1 style= {{textAlign:"left", color:'white', paddingTop: 10, paddingLeft: 10}} className={classes.title}>
        My Machines
      </h1>
      <Divider style= {{backgroundColor:"rgba(172,134,150,1)", height: 2, width: "95%", margin: "auto"}}/>
       <List >
       {items}
       </List>

    </div>
    </div>

    </>
  )

}
