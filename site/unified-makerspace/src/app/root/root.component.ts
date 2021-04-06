import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-root',
  templateUrl: './root.component.html',
  styleUrls: ['./root.component.scss'],
})
export class RootComponent implements OnInit {
  constructor() {}

  ngOnInit(): void {}

  machines = [
    '3D Printer #1',
    '3D Printer #2',
    'Satellite Controller',
    'Mars Rover',
  ];
}
