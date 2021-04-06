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
      name: 'All Users',
      series: [
        {
          name: 'Today',
          value: 2,
        },
        {
          name: 'Yesterday',
          value: 7,
        },
        {
          name: 'Wednesday',
          value: 4,
        },
        {
          name: 'Tuesday',
          value: 9,
        },
      ],
    },
    {
      name: 'New Users',
      series: [
        {
          name: 'Today',
          value: 1,
        },
        {
          name: 'Yesterday',
          value: 3,
        },
        {
          name: 'Wednesday',
          value: 2,
        },
        {
          name: 'Tuesday',
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
      formattedData += item.name + columnDelimiter;
    });
    formattedData = formattedData.slice(0, -1) + rowDelimiter; //replace last comma with newline

    let temp = this.data[1];
    //for each day listed in the series, record data
    this.data[0].series.forEach(function (item, index) {
      formattedData +=
        item.name +
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
