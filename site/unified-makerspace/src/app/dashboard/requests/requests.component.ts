import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-requests',
  templateUrl: './requests.component.html',
  styleUrls: ['./requests.component.scss'],
})
export class RequestsComponent implements OnInit {
  constructor() {}

  ngOnInit(): void {}

  requests = [
    {
      name: 'Will',
      request: '3D printer ink is out.',
      date: 'Today',
    },
    {
      name: 'Blythe',
      request: 'The wrenches are difficult to find.',
      date: 'Two weeks ago',
    },
  ];
}
