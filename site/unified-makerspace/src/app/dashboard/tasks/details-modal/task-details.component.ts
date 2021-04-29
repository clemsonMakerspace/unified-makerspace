import {Component, Input, OnInit} from '@angular/core';
import {NgbModal} from '@ng-bootstrap/ng-bootstrap';

@Component({
  selector: 'app-task-details',
  templateUrl: './task-details.component.html',
  styleUrls: ['./task-details.component.scss']
})
export class TaskDetailsComponent implements OnInit {

  constructor(public modal: NgbModal) { }

  @Input('task') task;

  ngOnInit(): void {

    // todo remove
    console.warn(this.task);
  }

}
