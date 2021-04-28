import {Component, OnInit} from '@angular/core';
import {AuthService} from '../../shared/auth/auth.service';
import {Router} from '@angular/router';
import {FormBuilder, FormGroup, Validators} from '@angular/forms';
import {showError, useTestData} from 'src/app/shared/funcs';
import {HttpErrorResponse} from '@angular/common/http';

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


  login() {

    // todo move stuff to api service

    this.loginForm['submitted'] = true;
    this.loginForm['error'] = '';

    if (this.loginForm.valid) {
      this.auth.login(this.loginForm.value).subscribe(
        (res) => {

          let user = res['user'];
          if (user) {
            this.auth.user.next({...user, 'auth_token': user['auth_token']});
            localStorage.setItem('User', JSON.stringify(user));
            this.router.navigate(['dashboard']).then();
          } else {
            console.log(res); // todo remove
            this.loginForm['error'] = 'Sorry, we\'re having issue with the server.';
          }
        },
        (err: HttpErrorResponse) => {
          this.handleError(err);
        }
      );
    }
  }


  handleError(err: HttpErrorResponse) {
    let error = 'Sorry, we\'re having trouble logging you in.';
    if (err.status == 401) {
      error = 'Sorry, your password is incorrect.';
    } else if (err.status == 408) {
      error = "Sorry, this email is not associated with any account."
    }
    this.loginForm['error'] = error;
  }


}
