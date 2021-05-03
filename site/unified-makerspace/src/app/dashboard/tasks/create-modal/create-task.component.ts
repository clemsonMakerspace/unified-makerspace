import {Component, OnInit} from '@angular/core';
import {FormBuilder, FormGroup, Validators} from '@angular/forms';
import {ApiService} from '../../../shared/api/api.service';
import {showError, useTestData} from '../../../shared/funcs';
import {NgbModal} from '@ng-bootstrap/ng-bootstrap';

@Component({
  selector: 'app-create-task',
  templateUrl: './create-task.component.html',
  styleUrls: ['./create-task.component.scss'],
})
export class CreateTaskComponent implements OnInit {

  // todo get list of machines?

  constructor(private api: ApiService,
              private fb: FormBuilder,
              public modal: NgbModal) {
  }


  tags = [];
  users = [];

  taskForm: FormGroup;
  showError: any;

  ngOnInit(): void {

    // get list of users for dropdown
    this.api.getUsers([]).subscribe((result) => {
      this.users = result.users.map((user) => user.first_name);
    });


    this.taskForm = this.fb.group({
      taskName: ['', Validators.required],
      description: [''],
      tags: ['', Validators.required],
      person: ['', Validators.required]
    });

    // fill with test data
    useTestData(this.taskForm, 'task');

    this.showError = showError(this.taskForm);
    this.tags = this.parseTags();

  }

  /* convert comma separated string of tags to array */
  parseTags(): string[] {
    let tags = this.taskForm.get('tags').value;
    return tags.toString().toLowerCase().trim().split(',');
  }


  onSubmit(): void {

    let getValue = (field: string) =>
      this.taskForm.get(field).value;
    this.taskForm['error'] = '';
    this.taskForm['submitted'] = true;

    if (this.taskForm.valid) {
      this.api.createTask({
        'person': getValue('person'),
        'task_name': getValue('taskName'),
        'description': getValue('description4'),
        'tags': this.tags,
      }).subscribe((res) => {
        this.taskForm['success'] = true;
      }, () => {
        this.taskForm['error'] = 'Sorry an error occurred!';
      });
    }
  }


}
