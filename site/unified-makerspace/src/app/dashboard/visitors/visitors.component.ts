import { Component, OnInit } from '@angular/core';
import {LayoutService} from '../../shared/layout/layout.service';

@Component({
  selector: 'app-visitors',
  templateUrl: './visitors.component.html',
  styleUrls: ['./visitors.component.scss']
})
export class VisitorsComponent implements OnInit {

  constructor(public layout: LayoutService) { }

  ngOnInit(): void {
  }

}
