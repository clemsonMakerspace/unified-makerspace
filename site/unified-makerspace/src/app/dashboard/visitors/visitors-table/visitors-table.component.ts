import {Component, OnInit} from '@angular/core';
import {ApiService} from '../../../shared/api/api.service';
import {LayoutService} from '../../../shared/layout/layout.service';
import {HttpErrorResponse} from '@angular/common/http';

@Component({
  selector: 'app-user-table',
  templateUrl: './visitors-table.component.html',
  styleUrls: ['./visitors-table.component.scss']
})
export class VisitorsTableComponent implements OnInit {

  constructor(private api: ApiService,
              public layout: LayoutService) {
  }


  // data for visitors
  visitors = [];


  // response key to display name mapping
  tableFields = {
    first_name: 'First Name',
    last_name: 'Last Name',
    major: 'Major',
    degree: 'Degree',
    sign_in_time: 'Sign-in Time',
    sign_out_time: 'Sign-out time'
  };


  // show first three keys by default
  keys = Object.keys(this.tableFields).slice(0, 3);

  // http errors
  error: HttpErrorResponse;

  // pagination
  page = 1;
  pageSize = 6;


  ngOnInit(): void {

    // fetch data on start
    this.api.getVisitors({}).subscribe((data) => {
      data['visitors'].map(v => {
        // convert epoch to milliseconds
        v['sign_in_time'] = new Date(v['sign_in_time'] * 1000).toLocaleString();
        v['sign_out_time'] = new Date(v['sign_out_time'] * 1000).toLocaleString();

        // get data for each visitor
        this.api.getVisitorData(
          {'visitor_id': v['visitor_id']}
        ).subscribe(d => (
            this.visitors.push({...d['visitor'], ...v}))
          , () => ({...v, 'error': true}) // todo fix this
        );
      });
    }, (err) => {
      this.error = err;
    });

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
