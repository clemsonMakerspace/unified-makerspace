import { Component, OnInit } from '@angular/core';
import {FormBuilder, FormGroup, Validators} from '@angular/forms';
import {ApiService} from '../../shared/api/api.service';
import {showError} from '../../shared/funcs';

@Component({
  selector: 'app-reset-password',
  templateUrl: './reset-password.component.html',
  styleUrls: ['./reset-password.component.scss']
})
export class ResetPasswordComponent implements OnInit {

  constructor(private fb: FormBuilder, private api: ApiService) { }

  resetForm: FormGroup;
  showError;

  ngOnInit(): void {
    this.resetForm = this.fb.group({
      'email': ['', [Validators.required, Validators.email]]
    })

    this.showError = showError(this.resetForm);
  }



  onSubmit() {
    this.resetForm['error'] = false;
    if (this.resetForm.valid) {
      this.api.resetPassword(this.resetForm.value).subscribe((res) => {
        this.resetForm['success'] = true;
      }, (err) => {
        this.resetForm['error'] = err.error;
      })
    }
  }

}
