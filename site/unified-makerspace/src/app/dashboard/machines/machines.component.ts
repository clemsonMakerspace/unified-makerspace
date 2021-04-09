import { Component, OnInit } from '@angular/core';
import {ApiService} from '../../shared/api.service';

@Component({
  selector: 'app-machines',
  templateUrl: './machines.component.html',
  styleUrls: ['./machines.component.scss'],
})
export class MachinesComponent implements OnInit {
  constructor(private api: ApiService) {}

  // todo move modal to inside tasks...

  machines = [];

  // todo what is this for?
  stateMap = {
    '1': 'Working',
    '.5': 'Being Used',
    '.25': 'Being Repaired',
    '0': 'Not Working',
  };


  // todo in the future add support for more times
  // todo fix links on the first page
  // todo check for permissions for showing stuff

  ngOnInit(): void {
    this.getMachines();
  }

  // todo handle when machine can't be loading
  // todo front page

  getMachines() {
    let startDate = Date.now();
    let endDate = Date.now();
    this.api.getMachinesStatus({
      'start_date': startDate,
      'end_date': endDate
    }).subscribe((res)=> {
      // todo handle errors and stuff
      this.machines = res.machines;
    })

  }


  // todo create function to convert from received data
  // todo why is this not working



  tooltip(data) {
    if (!this.stateMap) {
      return '';
    }
    console.log(data); // todo remove
    return (
      data.label +
      ' ' +
      this.stateMap[data.data.toString()] +
      ' at hour ' +
      data.series
    );
  }
}
