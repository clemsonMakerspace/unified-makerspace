import {Component, OnInit} from '@angular/core';
import {AuthService} from '../../shared/auth/auth.service';
import {Router} from '@angular/router';
import {FormBuilder, FormGroup, Validators} from '@angular/forms';
import {showError, useTestData} from 'src/app/shared/funcs';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss']
})
export class LoginComponent implements OnInit {

  constructor(private auth: AuthService,
              public router: Router,
              private fb: FormBuilder) {
  }

  loginForm: FormGroup;
  showError: any;

  ngOnInit(): void {

    this.loginForm = this.fb.group({
      email: ['', Validators.required],
      password: ['', Validators.required]
    });

    this.showError = showError(this.loginForm);
    useTestData(this.loginForm, 'user');

  }

  // todo show loading indicators....
  // todo possible failures:
  // todo incorrect password
  // todo email in use

  login() {

    // todo move stuff to api service

    this.loginForm['submitted'] = true;
    this.loginForm['error'] = '';

    if (this.loginForm.valid) {
      this.auth.login(this.loginForm.value).subscribe(
        (res) => {

          let user = res['user'];
          if (user) {
            this.auth.user.next(user);
            localStorage.setItem('User', JSON.stringify(user));
            this.router.navigate(['dashboard']).then();
          } else {
            this.loginForm['error'] = 'Sorry, we\'re having issue with the server.';
          }


        },
        (err) => {
          // todo handle incorrect password
          // todo handle email in use
          this.loginForm['error'] = 'Sorry, we\'re having trouble logging you in.';
        }
      );
    }
  }


}
