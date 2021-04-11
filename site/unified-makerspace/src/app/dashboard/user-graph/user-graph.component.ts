import { Component, OnDestroy, OnInit } from '@angular/core';
import { NgxChartsModule } from '@swimlane/ngx-charts';
import { BrowserModule } from '@angular/platform-browser';
import {ApiService} from '../../shared/api/api.service';
import {Visit} from '../../shared/models';

@Component({
  selector: 'app-user-graph',
  templateUrl: './user-graph.component.html',
  styleUrls: ['./user-graph.component.scss'],
})
export class UserGraphComponent implements OnInit, OnDestroy {
  constructor(
    private api: ApiService
  ) {}

  // todo handle error better?


  errorMessage: string;
  startTime: number;
  endTime: number;
  interval: number; // todo keep?

  visits: any;

  ngOnInit(): void {

    this.getVisits();
  }

  /* gets all visits in a certain period */
  getVisits() {
    this.api.getVisitors({
      start_date: this.startTime,
      end_date: this.endTime
    }).subscribe((res) => {
      this.visits = this.convertData(res.visitors);
    }, (err) => {
      this.errorMessage = err.message;
    });
  }


  convertData(data: Visit[]) {
    // todo implement
  }

  /* exports users data to csv file */
  exportUserData() {
    let rowDelimiter = '\n';
    let columnDelimiter = ',';
    let formattedData = 'data:text/csv;charset=utf-8,';

    //setup header of csv as All Users, New Users, Day
    formattedData += 'Day' + columnDelimiter;
    this.visits.forEach(function (item, index) {
      formattedData += item.firstName + columnDelimiter;
    });
    formattedData = formattedData.slice(0, -1) + rowDelimiter; //replace last comma with newline

    let temp = this.visits[1];
    //for each day listed in the series, record data
    this.visits[0].series.forEach(function (item, index) {
      formattedData +=
        item.firstName +
        columnDelimiter +
        item.value +
        columnDelimiter +
        temp.series[index].value +
        rowDelimiter;
    });

    //Download data as a csv
    let encodedUri = encodeURI(formattedData);
    var link = document.createElement('a');
    link.setAttribute('href', encodedUri);
    link.setAttribute('download', 'Users.csv');
    link.id = 'csv-dl';
    document.body.appendChild(link);
    link.click();
  }

  // todo fix later

  /* remove csv link on leaving page */
  ngOnDestroy() {
    let csv = document.getElementById("csv-dl")
      if (csv){csv.remove()}
  }
}
