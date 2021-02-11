import {Component, OnInit} from '@angular/core';
import {ModalService} from '../modal.service';
import {FormControl, FormGroup, Validators} from '@angular/forms';

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
  tags = []

  contactForm: FormGroup;


  constructor(public modal: ModalService) {
  }


  parseTags() {
    this.tags = this.contactForm.get('tags').value.trim().split(',');
  }



  ngOnInit(): void {
    document.body.style.top = String(-1 * this.initialScrollPos) + 'px';
    this.modal.modalStatus.subscribe((value) => {
      if (!value.open) {
        this.closeModal();
      }
    });

    // todo only for testing

    this.contactForm = new FormGroup({
      task: new FormControl('', Validators.required),
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
    if (this.contactForm.valid) {
      this.formSubmitted = true;
      this.formLoading = true;
    }
  }

  showErrorFor(field: string): boolean {
    return (
      this.contactForm.get(field).invalid && this.contactForm.get(field).touched
    );
  }

}
