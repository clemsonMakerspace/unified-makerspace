import {Component, OnInit} from '@angular/core';
import {ApiService} from '../../shared/api/api.service';
import {Task, User} from 'src/app/shared/models';
import {NgbModal} from '@ng-bootstrap/ng-bootstrap';

@Component({
  selector: 'app-tasks',
  templateUrl: './tasks.component.html',
  styleUrls: ['./tasks.component.scss'],
})
export class TasksComponent implements OnInit {

  constructor(private modal: NgbModal, private api: ApiService) {
  }

  tasks: Task[];
  users: User[];
  errorMessage: string;


  /* type to status mappings */
  status_map = {
    0: 'Not Completed',
    1: 'In-Progress',
    2: 'Completed'
  };

  open(content) {
    this.modal.open(content, {
      size: 'lg'
    });
  }

  ngOnInit(): void {
    this.getUsers();
  }

  /* gets users and then tasks */
  getUsers() {
    this.api.getUsers([]).subscribe((res) => {
      this.users = res['users'];
      this.getTasks();
    }, (err) => this.handleError(err));
  }

  /* updates `tasks` array with new tasks */
  getTasks() {
    this.api.getTasks([]).subscribe((res) => {
      this.tasks = res['tasks'];
      this.tasks.forEach(((task, i) => {
          for (let user of this.users) {
            if (user.user_id == task.assigned_to) {
              this.tasks[i].assigned_to = user.first_name;
            }
          }
          for (let task of this.tasks) {
            task.state = this.status_map[task.status];
          }
        }
      ));
    }, (err) => this.handleError(err));
  }


  clearTasks(): void {
    for (let task of this.tasks.filter((task) => task.state == 'Completed')) {
      this.resolveTask(task.task_id);
    }
  }

  resolveTask(taskId: string) {
    this.api.resolveTask({
      'task_id': taskId
    }).subscribe((res) => {
      this.getTasks();
    }, (err) => this.handleError(err));
  }


  handleError(err: Error) {
    this.errorMessage = err.message;
  }

  /* export task data to csv */
  exportTaskData() {
    let rowDelimiter = '\n';
    let columnDelimiter = ',';
    let formattedData = 'data:text/csv;charset=utf-8,';

    //setup header of csv as Task, Person, Status
    formattedData +=
      'Task' +
      columnDelimiter +
      'Person' +
      columnDelimiter +
      'Status' +
      rowDelimiter;

    //loop through tasks and add data to csv
    this.tasks.forEach(function(item, index) {
      formattedData +=
        item.task_name +
        columnDelimiter +
        item.assigned_to +
        columnDelimiter +
        item.status +
        rowDelimiter;
    });

    //Download data as a csv
    let encodedUri = encodeURI(formattedData);
    var link = document.createElement('a');
    link.setAttribute('href', encodedUri);
    link.setAttribute('download', 'Tasks.csv');
    document.body.appendChild(link);
    link.click();
  }

}
