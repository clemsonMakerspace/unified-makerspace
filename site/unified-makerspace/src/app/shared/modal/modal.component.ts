import { Component, OnInit } from '@angular/core';
import { ModalService } from '../modal.service';
import { FormControl, FormGroup, Validators } from '@angular/forms';

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

  constructor(public modal: ModalService) {}

  parseTags() {
    this.tags = this.taskForm.get('tags').value.trim().split(',');
  }

  ngOnInit(): void {
    document.body.style.top = String(-1 * this.initialScrollPos) + 'px';
    this.modal.modalStatus.subscribe((value) => {
      if (!value.open) {
        this.closeModal();
      }
    });

    // todo only for testing
    // todo change contact form
    // todo validation of parameters

    this.taskForm = new FormGroup({
      task_name: new FormControl('', Validators.required),
      tags: new FormControl('3D Printer, Urgent', Validators.required),
      people: new FormControl('', [Validators.required]),
      description: new FormControl('', Validators.required),
    });

    this.parseTags();
  }

  closeModal(): void {
    document.body.classList.remove('frozen');
    document.documentElement.style.scrollBehavior = 'auto';
    window.scrollTo(0, this.initialScrollPos);
    document.documentElement.style.scrollBehavior = 'smooth';
  }

  // todo use real api

  onSubmit(): void {
    if (this.taskForm.valid) {
      this.formSubmitted = true;
      this.formLoading = true; // todo stop loading eventually lmao
    }
  }

  showErrorFor(field: string): boolean {
    return (
      this.taskForm.get(field).invalid && this.taskForm.get(field).touched
    );
  }
}
