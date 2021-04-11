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
  // todo add some sort of slider

  errorMessage: string;
  machines = [];
  startTime: number;
  endTime: number;
  intervalFormat: string;

  ngOnInit(): void {
    // todo make this dynamic
    this.startTime = new Date(2021, 2, 1).getTime();
    this.endTime = Date.now();
    this.getMachines();
  }


  /* gets data for all machines */
  getMachines() {
    this.api.getMachinesStatus({
      'start_date': this.startTime,
      'end_date': this.endTime
    }).subscribe((res) => {
      this.machines = this.convertData(
        res.machines, this.startTime,
        this.endTime);
    }, (err) => {
      this.errorMessage = err.message;
    });
  }


  /* converts response to usable data */
  convertData(data, startTime: number, endTime: number) {

    let interval = endTime - startTime;
    let type = 'hours';
    let stepSize = 1000 * 60 * 60; // an hour
    let cutoff = 48; // max units

    // find the best step size for interval
    let hours = interval / stepSize;
    if (hours > cutoff) {
      stepSize *= 24; // one day
      type = 'days';
      if (hours > Math.pow(cutoff, 2)) {
        stepSize *= 7; // one week
        type = 'weeks';
      }
    }

    let steps = Math.floor(interval / stepSize);
    this.intervalFormat = `${steps} ${type}`;

    let ret = []; // return data
    let t = startTime;
    for (let i = 0; i < steps; i++) {
      let series = [];
      t += stepSize;
      for (const [key, value] of (<any> Object).entries(data)) {
        let state = 0;
        for (let v of (value as any)) {
          if (t >= v[0] && t <= v[1]) {
            state = 1; // todo add optimization.
            break;
          }
          if (t >= v[1]) {
            break;
          }
        }
        series.push({'firstName': key, 'value': state});
      }
      ret.push({'firstName': i + 1, 'series': series});
    }

    return ret;
  }


  // todo why is this not working

  /* tooltip for squares */
  tooltip(data) {
    console.log(data); // todo remove
    return (
      data.label +
      ' ' +
      {
        '1': 'Working',
        '0': 'Not Working',
      }[data.visits.toString()] +
      ' at hour ' +
      data.series
    );
  }
}
