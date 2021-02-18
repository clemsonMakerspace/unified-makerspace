import {Component, OnDestroy, OnInit} from '@angular/core';
import {ModalService} from '../shared/modal.service';



@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.scss']
})
export class DashboardComponent implements OnInit {

  constructor(public modal: ModalService) { }

  ngOnInit(): void {}




}
