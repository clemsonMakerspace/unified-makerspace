import {Component, OnInit} from '@angular/core';
import {FormBuilder, FormGroup, Validators} from '@angular/forms';
import {ApiService} from '../../../shared/api/api.service';
import {showError, useTestData} from '../../../shared/funcs';
import {NgbModal} from '@ng-bootstrap/ng-bootstrap';

@Component({
  selector: 'app-modal',
  templateUrl: './modal.component.html',
  styleUrls: ['./modal.component.scss'],
})
export class ModalComponent implements OnInit {

  // todo modal close
  // todo remove these
  // todo get list of machines?
  // todo rename modal?
  // todo add comments
  // todo validation of parameters

  // todo show message?
  // todo handle error
  // todo success parameter?


  constructor(private api: ApiService,
              private fb: FormBuilder,
              public modal: NgbModal) {
  }


  tags = [];
  users = [];

  taskForm: FormGroup;
  showError: any;


  ngOnInit(): void {

    /* get list of users for dropdown */
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
        'person': getValue('person') == 'new' ? getValue('newPerson') : getValue('person'),
        'task_name': getValue('taskName'),
        'description': getValue('description'),
        'tags': this.tags,
      }).subscribe((res) => {
        this.taskForm['success'] = true;
      }, (err) => {
        this.taskForm['error'] = 'Sorry an error occurred!';
      });
    }
  }


}
