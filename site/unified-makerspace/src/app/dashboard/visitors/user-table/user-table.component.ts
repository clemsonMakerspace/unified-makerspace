import { Component, OnInit } from '@angular/core';
import {ApiService} from '../../../shared/api/api.service';

@Component({
  selector: 'app-user-table',
  templateUrl: './user-table.component.html',
  styleUrls: ['./user-table.component.scss']
})
export class UserTableComponent implements OnInit {

  constructor(private api: ApiService) { }


  // todo currently using visits; change to vistors later

  tableFields = {
    first_name: 'First Name'
  }



  tempTableFields: {

  }


  keys = Object.keys(this.tableFields);

  visitors: any;


  ngOnInit(): void {
    this.api.getVisitors({}).subscribe((data)=> {
      console.log("v", data);

      // todo also allow visits?
      this.visitors = data['visitors'];
    })
  }

}
