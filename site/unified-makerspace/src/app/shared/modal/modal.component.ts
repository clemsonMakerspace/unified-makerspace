import { Component, OnInit } from '@angular/core';
import { ModalService } from '../modal.service';
import { FormControl, FormGroup, Validators } from '@angular/forms';
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
  // todo make this dynamic
  tags = [];

  taskForm: FormGroup;

  constructor(public modal: ModalService, private api: ApiService) {}

  parseTags() {
    return this.taskForm.get('tags').value.trim().split(',');
  }

  ngOnInit(): void {
    document.body.style.top = String(-1 * this.initialScrollPos) + 'px';
    this.modal.modalStatus.subscribe((value) => {
      if (!value.open) {
        this.closeModal();
      }
    });

    // todo only for testing
    // todo validation of parameters

    // todo machines

    this.taskForm = new FormGroup({
      taskName: new FormControl('', Validators.required),
      description: new FormControl('', Validators.required),
      tags: new FormControl('3D Printer, Urgent', Validators.required),
      person: new FormControl('', [Validators.required]),
      newPerson: new FormControl('')
    });

    this.tags = this.parseTags();
  }

  // todo get a list of maintainers

  // todo implement
  // todo move to modal...?

  // todo use real api
  // todo add date of completion
  // todo put some gear icon?


  onSubmit(): void {
    let getValue = (field: string) => this.taskForm.get(field).value;


    // todo show message?
    // todo handle error
    this.formSubmitted = true;
    this.formLoading = true; // todo stop loading eventually lmao
    if (this.taskForm.valid) {
      this.api.createTask({
        'person': getValue('person') == 'new' ? getValue('newPerson') : getValue('person'),
        'task_name': getValue('taskName'),
        'description': getValue('description'),
        'tags': this.tags,

      }).subscribe((res)=> {
        this.formLoading = false;
      });
    }
  }


  showError(field: string) {
    let f = this.taskForm.get(field);
    let error = ""
    if (f.dirty) {
      if (f.invalid) {
        error = field + " is not valid."
      }
      if (f.value == '') {
        error = field + " is required."
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
