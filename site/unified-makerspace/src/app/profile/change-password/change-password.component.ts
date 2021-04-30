import { Component, OnInit } from '@angular/core';
import {FormBuilder, FormGroup, Validators} from '@angular/forms';
import {ApiService} from '../../shared/api/api.service';
import {showError} from '../../shared/funcs';
import {AuthService} from '../../shared/auth/auth.service';

@Component({
  selector: 'app-change-password',
  templateUrl: './change-password.component.html',
  styleUrls: ['./change-password.component.scss']
})
export class ChangePasswordComponent implements OnInit {

  constructor(
    private fb: FormBuilder,
    private api: ApiService,
    private auth: AuthService,
  ) { }


  showError: any;
  changePassword: FormGroup;


  ngOnInit(): void {
    this.changePassword = this.fb.group({
      password: ['', Validators.required],
      newPassword: ['', [Validators.required, Validators.minLength(6)]]
    })

    this.showError = showError(this.changePassword);
  }


  onSubmit() {

    this.changePassword['submitted'] = true;

    if (this.changePassword.valid) {
      this.api.changePassword({
        'password': this.changePassword.get('password').value,
        'new_password': this.changePassword.get('newPassword').value,
        'user_id': this.auth.user.getValue().user_id
      }).subscribe(res => {
        // todo this
      }, err => {
        this.changePassword['error'] = 'Sorry, the server is having some issues!';
      });
    }
  }

}
