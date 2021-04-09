import {Component, OnInit} from '@angular/core';
import {ModalService} from '../../../shared/modal.service';
import {FormControl, FormGroup, Validators} from '@angular/forms';
import {ApiService} from '../../../shared/api.service';

@Component({
  selector: 'app-modal',
  templateUrl: './modal.component.html',
  styleUrls: ['./modal.component.scss'],
})
export class ModalComponent implements OnInit {
  initialScrollPos = window.scrollY;

  errMessage = '';
  formSubmitted = false;
  formLoading = false;

  tags = [];
  users = [];

  // todo add comments

  taskForm: FormGroup;

  constructor(public modal: ModalService, private api: ApiService) {
  }

  parseTags() {
    return this.taskForm.get('tags').value.toLowerCase().trim().split(',');
  }

  ngOnInit(): void {



    document.body.style.top = String(-1 * this.initialScrollPos) + 'px';

    /* subscribe to modal changes */
    this.modal.modalStatus.subscribe((value) => {
      if (!value.open) {
        this.closeModal();
      }
    });


    /* get list of users for dropdown */
    this.api.getUsers([]).subscribe((result) => {
      this.users = result.users.map((user) => user.first_name)
    })

    // todo validation of parameters

    this.taskForm = new FormGroup({
      taskName: new FormControl('', Validators.required),
      description: new FormControl('', Validators.required),
      tags: new FormControl('', Validators.required),
      person: new FormControl('', [Validators.required]),
      newPerson: new FormControl('') // todo fix this...!
    });


    console.log(this.tags);


  }


  // todo implement
  // todo use real api


  onSubmit(): void {
    let getValue = (field: string) => this.taskForm.get(field).value;



    // todo show message?
    // todo handle error
    // todo fields missing error

    this.formSubmitted = true;

    if (this.taskForm.valid) {
      this.formLoading = true;
      this.api.createTask({
        'person': getValue('person') == 'new' ? getValue('newPerson') : getValue('person'),
        'task_name': getValue('taskName'),
        'description': getValue('description'),
        'tags': this.tags,

      }).subscribe((res) => {
        this.formLoading = false;
      }, (err) => {
        this.formLoading = false;
        this.errMessage = 'Sorry an error occurred!'; // todo read err message
      });
    }
  }


  showError(field: string) {
    let f = this.taskForm.get(field);
    let error = '';
    if (f.dirty || this.formSubmitted) {
      if (f.invalid) {
        error = field + ' is not valid.';
      }
      if (f.value == '') {
        error = field + ' is required.';
      }
    }
    return error;
  }


  showCompletion() {
    return this.formSubmitted && this.taskForm.valid;
  }



  /* called by html code to close modal box */
  closeModal(): void {
    document.body.classList.remove('frozen');
    document.documentElement.style.scrollBehavior = 'auto';
    window.scrollTo(0, this.initialScrollPos);
    document.documentElement.style.scrollBehavior = 'smooth';
  }
}
