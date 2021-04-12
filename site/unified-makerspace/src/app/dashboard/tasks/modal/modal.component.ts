import {Component, OnInit} from '@angular/core';
import {FormBuilder, FormControl, FormGroup, Validators} from '@angular/forms';
import {ApiService} from '../../../shared/api/api.service';
import {showError, useTestData} from '../../../shared/funcs';

@Component({
  selector: 'app-modal',
  templateUrl: './modal.component.html',
  styleUrls: ['./modal.component.scss'],
})
export class ModalComponent implements OnInit {

  // todo modal close
  errMessage = '';
  // todo remove these
  // todo remove modal service
  formSubmitted = false;
  formLoading = false;

  showError: any;

  tags = [];
  users = [];

  // todo add comments

  taskForm: FormGroup;

  constructor(private api: ApiService,
              private fb: FormBuilder) {
  }

  ngOnInit(): void {


    // todo get list of machines?
    // todo rename modal?


    /* get list of users for dropdown */
    this.api.getUsers([]).subscribe((result) => {
      this.users = result.users.map((user) => user.first_name)
    })

    // todo validation of parameters


    // todo should be able to create new person??

    this.taskForm = this.fb.group({
      taskName: ['', Validators.required],
      description: [''], // todo use N/A or if...
      tags: ['', Validators.required], // todo optional?
      person: ['', Validators.required]
    })


    this.showError = showError(this.taskForm)
    useTestData(this.taskForm, 'task');
    this.tags = this.parseTags()

  }

  parseTags(): string[] {
    let tags  = this.taskForm.get('tags').value
    return tags.toString().toLowerCase().trim().split(',');
  }



  // todo implement


  onSubmit(): void {

    let getValue = (field: string) => this.taskForm.get(field).value;



    // todo show message?
    // todo handle error
    // todo fields missing error



    this.taskForm['submitted'] = true;

    if (this.taskForm.valid) {

      this.formLoading = true;

      this.api.createTask({
        'person': getValue('person') == 'new' ? getValue('newPerson') : getValue('person'),
        'task_name': getValue('taskName'),
        'description': getValue('description'),
        'tags': this.tags,
      }).subscribe((res) => {
        this.formLoading = false; // todo remove
      }, (err) => {
        this.formLoading = false;
        this.errMessage = 'Sorry an error occurred!'; // todo read err message
      });
    }
  }


  // todo remove
  showCompletion() {
    return this.formSubmitted && this.taskForm.valid;
  }


}
