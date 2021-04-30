import { Component, OnInit } from '@angular/core';
import {ApiService} from '../../shared/api/api.service';

@Component({
  selector: 'app-users',
  templateUrl: './users.component.html',
  styleUrls: ['./users.component.scss']
})
export class UsersComponent implements OnInit {

  constructor(private api: ApiService) { }

  users = []
  page = 1;
  pageSize = 10;


  ngOnInit(): void {
    this.api.getUsers({}).subscribe((res)=> {
      this.users = res['users'];
      for (let user of this.users) {
        user['name'] = user.first_name + ' ' + user.last_name;
      }

      this.users = this.users.sort((a,b) => a['name'] > b['name'] ? 1 : -1);

    })
  }


}
