import {Component, OnDestroy, OnInit} from '@angular/core';
import {ApiService} from '../../../shared/api/api.service';
import {Visit, Visitor} from '../../../shared/models';
import {HttpErrorResponse} from '@angular/common/http';
import {DataService} from '../../../shared/data.service';

@Component({
  selector: 'app-visitors-graph',
  templateUrl: './visitors-graph.component.html',
  styleUrls: ['./visitors-graph.component.scss'],
})
export class VisitorsGraphComponent implements OnInit, OnDestroy {
  constructor(
    private api: ApiService,
    private ds: DataService,
  ) {
  }

  // todo slider labels...?

  startTime: number;
  endTime: number;

  // raw visit data
  visits: Visit[];

  // converted data
  visitsGraphData: any;

  error: HttpErrorResponse;


  ngOnInit(): void {
    // default start time is 7 days ago
    let dt = new Date();
    dt.setDate(dt.getDate() - 7);
    this.startTime = dt.getTime();

    // end time is always now
    this.endTime = Date.now();
    this.getVisits(this.startTime, this.endTime);
    this.startTime = -7; // for slider

  }

  /* gets all visits in a certain period */
  getVisits(startTime: number, endTime: number) {
    this.api.getVisitors({
      start_date: startTime / 1000,
      end_date: endTime / 1000
    }).subscribe((res) => {
      let data = res['visitors'];
      if (data === undefined) { // for backward compatibility
        data = res['visits'];
      }

      this.visits = data;
      this.visitsGraphData = this.convertData(data,
        startTime / 1000, endTime / 1000);
    }, (err) => {
      this.error = err;
    });
  }

  onSliderChange(value: number) {
    setTimeout(() => {
      if (value == this.startTime) {
        let d = new Date();
        d.setDate(d.getDate() + value);
        this.getVisits(d.getTime(), this.endTime);
      }
    }, 500);
  }


  /* converts response to usable data */
  convertData(data: Visit[], startTime: number, endTime: number) {

    let interval = endTime - startTime;
    let stepSize = 60 * 60 * 24; // a day
    let steps = Math.floor(interval / stepSize);

    // return data
    let ret = [{
      name: 'All Users',
      series: []
    }, {
      name: 'New Users',
      series: []
    }];


    let t = startTime;
    for (let i = 0; i < steps; i++) {

      let count = {'new': 0, 'all': 0,};

      // check if visit falls in time step
      for (const visit of (data as any)) {
        let d = visit.sign_in_time;
        if (d >= t && d <= t + stepSize) {
          count[visit.first_visit ? 'new' : 'all']++;
        }
      }

      // updates
      t += stepSize;
      ret[0].series.push({'name': i, 'value': count['all']});
      ret[1].series.push({'name': i, 'value': count['new']});

    }

    return ret;
  }

  /* exports users data to tsv file */
  exportUserData() {
    let rowDelimiter = '\n';
    let columnDelimiter = '\t';

    let csvString = 'data:text/csv;charset=utf-8,';
    let data = this.ds.visits.getValue();

    let keys = {
      first_name: 'First Name',
      last_name: 'Last Name',
      major: 'Major',
      degree: 'Degree',
      sign_in_time_str: 'Sign-in Time',
      sign_out_time_str: 'Sign-out time'
    };


    // header row
    csvString += Object.values(keys)
      .join(columnDelimiter) + rowDelimiter;

    // for each day listed in the series, record data
    data.forEach((item) => {
      console.log(item);
        Object.keys(keys).forEach((k) => {
          csvString += item[k] + columnDelimiter;
        })
        csvString += rowDelimiter;
      }
    );

    // download data as a csv
    let encodedUri = encodeURI(csvString);
    let link = document.createElement('a');
    link.setAttribute('href', encodedUri);
    link.setAttribute('download', 'Users.tsv');
    link.id = 'csv-dl';
    document.body.appendChild(link);
    link.click();
  }

  /* remove csv link when leaving page */
  ngOnDestroy() {
    let csv = document.getElementById('csv-dl');
    if (csv) {
      csv.remove();
    }
  }
}
