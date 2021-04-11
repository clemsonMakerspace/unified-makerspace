import { Component, OnDestroy, OnInit } from '@angular/core';
import { NgxChartsModule } from '@swimlane/ngx-charts';
import { BrowserModule } from '@angular/platform-browser';

@Component({
  selector: 'app-user-graph',
  templateUrl: './user-graph.component.html',
  styleUrls: ['./user-graph.component.scss'],
})
export class UserGraphComponent implements OnInit, OnDestroy {
  constructor() {}

  ngOnInit(): void {}

  data = [
    {
      firstName: 'All Users',
      series: [
        {
          firstName: 'Today',
          value: 2,
        },
        {
          firstName: 'Yesterday',
          value: 7,
        },
        {
          firstName: 'Wednesday',
          value: 4,
        },
        {
          firstName: 'Tuesday',
          value: 9,
        },
      ],
    },
    {
      firstName: 'New Users',
      series: [
        {
          firstName: 'Today',
          value: 1,
        },
        {
          firstName: 'Yesterday',
          value: 3,
        },
        {
          firstName: 'Wednesday',
          value: 2,
        },
        {
          firstName: 'Tuesday',
          value: 4,
        },
      ],
    },
  ];

  // exporting users data to csv file
  exportUserData() {
    let rowDelimiter = '\n';
    let columnDelimiter = ',';
    let formattedData = 'data:text/csv;charset=utf-8,';

    //setup header of csv as All Users, New Users, Day
    formattedData += 'Day' + columnDelimiter;
    this.data.forEach(function (item, index) {
      formattedData += item.firstName + columnDelimiter;
    });
    formattedData = formattedData.slice(0, -1) + rowDelimiter; //replace last comma with newline

    let temp = this.data[1];
    //for each day listed in the series, record data
    this.data[0].series.forEach(function (item, index) {
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

  ngOnDestroy() {
    // document.getElementById("csv-dl").remove()
  }
}
