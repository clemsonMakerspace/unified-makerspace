import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-users',
  templateUrl: './users.component.html',
  styleUrls: ['./users.component.scss'],
})
export class UsersComponent implements OnInit {
  constructor() {}

  ngOnInit(): void {}

  getUsersByRole(role: string) {
    return this.users.filter((user) => user['Role'] == role);
  }

  roles = ['Manager', 'Maintainer', 'User'];
  users = [
    {
      Name: 'Joe',
      Role: 'Manager',
      Permissions: {},
    },
    {
      Name: 'Candace',
      Role: 'Manager',
      Permissions: {},
    },
    {
      Name: 'Dr.Nicky',
      Role: 'Maintainer',
      Permissions: {},
    },
    {
      Name: 'Delilah',
      Role: 'Maintainer',
      Permissions: {},
    },
    {
      Name: 'Paco',
      Role: 'User',
      Permissions: {},
    },
  ];
}
