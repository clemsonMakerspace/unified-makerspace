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
  ngOnInit(): void {
    this.api.getUsers((res)=> {
      this.users = res['users'];
    })
  }


}
