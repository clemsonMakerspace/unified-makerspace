import { Component, OnDestroy, OnInit } from '@angular/core';
import { AuthService } from '../shared/auth/auth.service';
import {Title} from '@angular/platform-browser';
import {LayoutService} from '../shared/layout/layout.service';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.scss'],
})
export class DashboardComponent implements OnInit {
  constructor(public auth: AuthService,
              public layout: LayoutService,
              private title: Title) {}

  ngOnInit(): void {
    this.title.setTitle('Dashboard');
  }
}
