import {Component, OnInit} from '@angular/core';
import {ApiService} from '../../shared/api/api.service';

@Component({
  selector: 'app-machines',
  templateUrl: './machines.component.html',
  styleUrls: ['./machines.component.scss'],
})
export class MachinesComponent implements OnInit {
  constructor(private api: ApiService) {
  }

  // todo better err handling?
  // todo fix links on the first page
  // todo check for permissions for showing stuff

  // todo change length automatically based on screen size

  errorMessage: string;
  machines = [];
  startTime: number;
  endTime: number;
  intervalFormat: string;
  intervalLength = 'hours';


  // todo change slider value and use that
  ngOnInit(): void {
    // default start time is 24 hours ago
    let dt = new Date()
    dt.setHours(dt.getHours() - 24);
    this.startTime = dt.getTime();

    // end time is always now
    this.endTime = Date.now();
    this.getMachines(this.startTime, this.endTime);
    this.startTime = 1; // todo remove later
  }

  /* send request after 500 ms of inactivity */
  onSliderChange(value: number) {
    setTimeout(() => {
      if (value == this.startTime) {
        this.getMachines(this.toTime(value), this.endTime);
      }
    }, 500)
  }

  /* slider interpolator */
  /*
    quadratic curve fitting
    y = 364.8263 - 8.458279*x + 0.04823032*x^2
    ┌────────┬──────────────┐
    │ slider │ value (days) │
    ├────────┼──────────────┤
    │      0 │          365 │
    │     60 │           30 │
    │     70 │            7 │
    │     80 │            1 │
    │    100 │            0 │
    └────────┴──────────────┘
   */

  toDays(value: number):number {
    let v = (102 - value)/24;
    if (value < 75) {
      v = 364.8263 - 8.4582 * value + 0.04823 * Math.pow(value, 2);
    }
    return v;
  }

  // todo call todays?
  toTime(value: number):number {
    let v = (102 - value)/24;
    if (value < 75) {
      v = 364.8263 - 8.4582 * value + 0.04823 * Math.pow(value, 2);
    }
    let d = new Date();
    d.setHours(d.getHours() - v*24);
    return d.getTime();
  }



  /* gets data for all machines */
  getMachines(startTime: number, endTime: number) {
    this.api.getMachinesStatus({
      'start_date': startTime,
      'end_date': endTime
    }).subscribe((res) => {
      let data = res['statuses'];
      if (data === undefined) { // for backward compatibility
        data = res['machines'];
      }
      this.machines = this.convertData(
        data, startTime, endTime);
    }, (err) => {
      this.errorMessage = err.message;
    });
  }


  /* converts response to usable data */
  convertData(data, startTime: number, endTime: number) {

    let interval = endTime - startTime;
    let type = 'hours';
    let stepSize = 1000 * 60 * 60; // an hour

    // find the best step size for interval
    let hours = interval / stepSize;
    if (hours > 24) {
      stepSize *= 24; // one day
      type = 'days';
      if (hours > 30*24) {
        stepSize *= 7; // one week
        type = 'weeks';
      }
    }

    let steps = Math.floor(interval / stepSize);

    // terminate if greater than year
    // to prevent browser from crashing
    if (steps > 52) {
      console.log('Excess range. Not calculating.', steps);
      return this.machines;
    }


    // set global variables
    this.intervalFormat = `${steps} ${type}`;
    this.intervalLength = type;

    let ret = []; // return data
    let t = startTime;
    for (let i = 0; i < steps; i++) {
      let series = [];
      t += stepSize;
      for (const [key, value] of (<any> Object).entries(data)) {
        let state = 1;
        for (let v of (value as any)) {
          if (t >= v[0] && t <= v[1]) {
            state = 0; // todo add optimization?
            break;
          }
          if (t >= v[1]) {
            break;
          }
        }
        series.push({'name': key, 'value': state});
      }
      ret.push({'name': i + 1, 'series': series});
    }

    return ret;
  }


  /* tooltip for squares */
  tooltip(data) {
    return (
      data.label +
      ' ' +
      {
        '1': 'was working',
        '0': 'was not working',
      }[data.data.toString()] +
      ' at ' + this.intervalLength + ' ' +
      data.series
    );
  }
}
