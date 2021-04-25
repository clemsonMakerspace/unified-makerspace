import { Component, OnInit } from '@angular/core';
import {ApiService} from '../../../shared/api/api.service';
import {map} from 'rxjs/operators';
import {logger} from 'codelyzer/util/logger';

@Component({
  selector: 'app-user-table',
  templateUrl: './visitors-table.component.html',
  styleUrls: ['./visitors-table.component.scss']
})
export class VisitorsTableComponent implements OnInit {

  constructor(private api: ApiService) { }


  // todo currently using visits; change to vistors later

  tableFields = {
    first_name: 'First Name',
    last_name: 'Last Name',
    major: 'Major',
    // degree: 'Degree',
    // sign_in_time: 'Sign-in Time',
    // sign_out_time: 'Sign-out time'
  }


  keys = Object.keys(this.tableFields);

  visitors = []


  // todo limit to 50...?
  // todo handle errors
  ngOnInit(): void {

    this.api.getVisitors({}).subscribe((data)=> {
      // todo check
      data['visitors'].map(v => {
        this.api.getVisitorData(
          {'visitor_id': v['visitor_id']}
        ).subscribe(d => (
          this.visitors.push({...d['visitor'], ...v}))
          , () => ({...v, "error": true}) // todo fix this
        )
      })
    })




    setTimeout(() => {
      console.log(this.visitors);
      }, 2000)


  }

}
