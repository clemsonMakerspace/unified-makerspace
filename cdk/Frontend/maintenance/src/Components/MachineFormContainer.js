import React from 'react';
import clsx from 'clsx';
import { makeStyles } from '@material-ui/core/styles';
import { BrowserRouter as Router, Route, Link } from 'react-router-dom';
import "../App.css";
import "./Form.css";
import Button from '@material-ui/core/Button';
import uploadImage from "../Assets/UploadImage.png";


class MachineFormContainer extends React.Component {

    render(){

        return (
          <div className= {"baseroot"}>

              <div style={{visibility: "visible" }}>
              <div  style={{display: "flex", flexDirection: "row", width: "80%", margin:"auto"}}>

<div class="container">
  <Link to={{pathname:"/ConfigureNewMachine"}}>
    <img type="uploadImage" src={uploadImage}/>
  </Link>
  <form action="action_page.php">
    <div class="row">
      <div class="col-25">
        <label for="MachineName">Machine Name</label>
      </div>
      <div class="col-75">
        <input type="text" id="MachineName" name="MachineName" placeholder="Machine name..."/>
      </div>
    </div>
    <div class="row">
      <div class="col-25">
        <label for="MachineType">Machine Type</label>
      </div>
      <div class="col-75">
        <select id="MachineType" name="MachineType">
          <option value="tazXL">3D Printer: Taz XL</option>
          <option value="tazmini">3D Printer: Taz Mini</option>
          <option value="lasercutter">Laser Cutter</option>
        </select>
      </div>
    </div>
    <br></br>
    <div class="row">
      <saveChanges>
      <Button component={Link} to="/ConfigureNewMachine" onclick={this.props.handleClick(false)} className={clsx("root")}>
      Save Changes
      </Button>
      </saveChanges>
    </div>
  </form>
</div>
              </div>

            <div style={{height: 20}}/>
          </div>

        </div>
        );
        }

}
export default MachineFormContainer;
