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

  contactForm: FormGroup;


  constructor(public modal: ModalService) {
  }

  ngOnInit(): void {
    document.body.style.top = String(-1 * this.initialScrollPos) + 'px';
    document.body.classList.add('frozen');
    this.modal.modalStatus.subscribe((value) => {
      if (!value.open) {
        this.closeModal();
      }
    });

    this.contactForm = new FormGroup({
      task: new FormControl('', Validators.required),
      machine: new FormControl('', Validators.required),
      people: new FormControl('', [Validators.required]),
      description: new FormControl('', Validators.required),
    });

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
      // this.api
      //   .post('contact', {
      //     name: this.contactForm.get('name').value,
      //     email: this.contactForm.get('email').value,
      //     message: this.contactForm.get('message').value,
      //   })
      //   .subscribe(
      //     (res) => {
      //       // todo check for server side errors...?
      //       this.formLoading = false;
      //       setTimeout(() => this.modal.close(), 3000);
      //     },
      //     (err) => {
      //       console.log(err); // todo for debugging
      //       this.formLoading = false;
      //       this.errMessage = err.statusText;
      //     }
      //   );
    }
  }

  showErrorFor(field: string): boolean {
    return (
      this.contactForm.get(field).invalid && this.contactForm.get(field).touched
    );
  }

}
