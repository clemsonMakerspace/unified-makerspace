import {Component, OnInit} from '@angular/core';
import {ApiService} from '../../../shared/api/api.service';
import {LayoutService} from '../../../shared/layout/layout.service';
import {HttpErrorResponse} from '@angular/common/http';
import {DataService} from '../../../shared/data/data.service';

@Component({
  selector: 'app-user-table',
  templateUrl: './visitors-table.component.html',
  styleUrls: ['./visitors-table.component.scss']
})
export class VisitorsTableComponent implements OnInit {

  constructor(private api: ApiService,
              private ds: DataService,
              public layout: LayoutService) {
  }


  // data for visits
  visits = [];
  visitors = {};

  // response key to display name mapping
  tableFields = {
    first_name: 'First Name',
    last_name: 'Last Name',
    major: 'Major',
    degree: 'Degree',
    sign_in_time_str: 'Sign-in Time',
    sign_out_time_str: 'Sign-out time'
  };


  // show first three keys by default
  keys = Object.keys(this.tableFields).slice(0, 3);

  // http errors
  error: HttpErrorResponse;

  // pagination
  page = 1;
  pageSize = 6;


  ngOnInit(): void {
    // first get visitors
    // then get visits
    // and then associate visits with visitors data
    this.getVisitors();
  }


  getVisitors() {

    this.api.getVisitorData({}).subscribe((res) => {
      res['visitors'].forEach((v) => {
        this.visitors[v['visitor_id']] = v;
      });

      if (res['visitors']) {
        this.getVisits();
      }

    }, (err) => this.error = err);
  }


  getVisits() {
    this.visits = [];
    this.api.getVisitors({}).subscribe((data) => {

      // get data for each visitor
      data['visits'].map(v => {

        // convert epoch to milliseconds
        v['sign_in_time_str'] = new Date(v['sign_in_time'] * 1000).toLocaleString();
        v['sign_out_time_str'] = new Date(v['sign_out_time'] * 1000).toLocaleString();

        let visitor = this.visitors[v['visitor_id']];
        if (visitor) {
          this.visits.push({...visitor, ...v});
        }

      });

      this.visits.sort(
        (a, b) =>
          (a.sign_in_time < b.sign_in_time)
            ? 1 : -1);

      this.ds.visits.next(this.visits);

    }, (err) => this.error = err);
  }


  /* switch between expanded and collapsed table */
  toggle() {
    // change value in layout service
    this.layout.usersTableIsExpanded = !this.layout.usersTableIsExpanded;

    if (this.layout.usersTableIsExpanded) {
      // show all keys
      this.keys = Object.keys(this.tableFields);
    } else {
      // show only first three keys when collapsed
      this.keys = Object.keys(this.tableFields).slice(0, 3);
    }
  }

}
