import {Component, OnInit} from '@angular/core';
import {ModalService} from '../../shared/modal.service';

@Component({
  selector: 'app-tasks',
  templateUrl: './tasks.component.html',
  styleUrls: ['./tasks.component.scss']
})
export class TasksComponent implements OnInit {

  constructor(public modal: ModalService) {
  }

  tasks = [{
    task: 'Replace 3D-Printer Cartridge',
    person: 'Ellie',
    status: 'Completed',
  },
    {
      task: 'Install new CNC-Router',
      person: 'Beck',
      status: 'In-Progress'
    },
    {
      task: 'Update the Sign-in System',
      person: 'Peach',
      status: 'Not Started'
    }
  ];


  ngOnInit(): void {
  }

  clearTasks(): void {
    this.tasks = this.tasks.filter((task) =>
      task.status !== 'Completed'
    );

  }
}
