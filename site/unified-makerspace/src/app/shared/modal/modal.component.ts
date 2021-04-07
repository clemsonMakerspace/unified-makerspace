import {Component, OnInit} from '@angular/core';
import {ModalService} from '../modal.service';
import {FormControl, FormGroup, Validators} from '@angular/forms';
import {ApiService} from '../api.service';

@Component({
  selector: 'app-modal',
  templateUrl: './modal.component.html',
  styleUrls: ['./modal.component.scss'],
})
export class ModalComponent implements OnInit {
  initialScrollPos = window.scrollY;

  formSubmitted = false;
  formLoading = false;
  errMessage = '';

  tags = [];
  persons = []; // todo change this later

  taskForm: FormGroup;

  constructor(public modal: ModalService, private api: ApiService) {
  }

  parseTags() {
    return this.taskForm.get('tags').value.trim().split(',');
  }

  ngOnInit(): void {

    // todo add comments
    document.body.style.top = String(-1 * this.initialScrollPos) + 'px';
    this.modal.modalStatus.subscribe((value) => {
      if (!value.open) {
        this.closeModal();
      }
    });


    this.api.getUsers([]).subscribe((result) => {
      this.persons = result.users.map((user) => user.first_name)
    })

    // todo validation of parameters

    this.taskForm = new FormGroup({
      taskName: new FormControl('', Validators.required),
      description: new FormControl('', Validators.required),
      tags: new FormControl('', Validators.required),
      person: new FormControl('', [Validators.required]),
      newPerson: new FormControl('') // todo fix this...!
    });

  }

  // todo get a list of maintainers

  // todo implement
  // todo move to modal...?

  // todo use real api
  // todo add date to complete by

  // todo change spinner to cogwheel


  onSubmit(): void {
    let getValue = (field: string) => this.taskForm.get(field).value;


    // todo show message?
    // todo handle error
    // todo fields missing error

    if (this.taskForm.valid) {
      this.formSubmitted = true;
      this.formLoading = true; // todo stop loading eventually lmao
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
    if (f.dirty) {
      if (f.invalid) {
        error = field + ' is not valid.';
      }
      if (f.value == '') {
        error = field + ' is required.';
      }
    }
    return error;
  }

  closeModal(): void {
    document.body.classList.remove('frozen');
    document.documentElement.style.scrollBehavior = 'auto';
    window.scrollTo(0, this.initialScrollPos);
    document.documentElement.style.scrollBehavior = 'smooth';
  }
}
