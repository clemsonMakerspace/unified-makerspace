import { Component, OnInit } from '@angular/core';
import {ApiService} from '../../../shared/api/api.service';
import {map} from 'rxjs/operators';
import {logger} from 'codelyzer/util/logger';
import {LayoutService} from '../../../shared/layout/layout.service';
import {HttpErrorResponse} from '@angular/common/http';

@Component({
  selector: 'app-user-table',
  templateUrl: './visitors-table.component.html',
  styleUrls: ['./visitors-table.component.scss']
})
export class VisitorsTableComponent implements OnInit {

  constructor(private api: ApiService,
      public layout: LayoutService) { }


  // todo currently using visits; change to vistors later

  error: HttpErrorResponse;

  tableFields = {
    first_name: 'First Name',
    last_name: 'Last Name',
    major: 'Major',
    degree: 'Degree',
    sign_in_time: 'Sign-in Time',
    sign_out_time: 'Sign-out time'
  }

  toggle() {

    this.layout.usersTableIsExpanded = !this.layout.usersTableIsExpanded ;
    if (this.layout.usersTableIsExpanded) {
      this.keys = Object.keys(this.tableFields);
    } else {
      this.keys = Object.keys(this.tableFields).slice(0,3);
    }
  }

  keys = Object.keys(this.tableFields).slice(0,3);
  visitors = []


  // pagination
  page = 1;
  pageSize = 6;


  ngOnInit(): void {

    this.api.getVisitors({}).subscribe((data)=> {
      // todo check
      data['visitors'].map(v => {
        v['sign_in_time'] = new Date(v['sign_in_time']*1000).toLocaleString();
        v['sign_out_time'] = new Date(v['sign_out_time']*1000).toLocaleString();
        this.api.getVisitorData(
          {'visitor_id': v['visitor_id']}
        ).subscribe(d => (
          this.visitors.push({...d['visitor'], ...v}))
          , () => ({...v, "error": true}) // todo fix this
        )
      })
    }, (err) => {
      this.error = err;
    })
  }

}
