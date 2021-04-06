import { Component, OnInit } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { AuthService } from '../shared/auth/auth.service';
import { Router } from '@angular/router';
import {stringify} from '@angular/compiler/src/util';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss'],
})
export class LoginComponent implements OnInit {
  constructor(private auth: AuthService, private router: Router) {}

  loginForm: FormGroup;
  registerForm: FormGroup;

  formType = 'login'; // either 'login' or 'register'
  errorMessage: string;
  success = false;

  ngOnInit(): void {
    // todo get params
    this.formType = this.router.url.split('/')[1];

    // todo only for testing
    this.loginForm = new FormGroup({
      username: new FormControl('joe@makerspace.com', Validators.required),
      password: new FormControl('password', Validators.required),
    });

    this.registerForm = new FormGroup({
      username: new FormControl('joe@makerspace.com', Validators.required),
      password: new FormControl('password', Validators.required),
      confirmPassword: new FormControl('password', Validators.required),
    });
  }

  // todo change url instead?
  switchMode() {
    this.router
      .navigate([this.formType == 'login' ? 'register' : 'login'])
      .then();
  }

  // todo show loading indicators....

  login() {
    // todo check for success
    // todo getValue?

    // todo move stuff to api service
    this.errorMessage = '';
    let username = this.loginForm.get('username').value;
    let password = this.loginForm.get('password').value;

    if (this.loginForm.valid) {
      this.auth.login(username, password).subscribe(
        (res) => {
          try {
            console.log(res); // todo remove
            let user = res['user'];
            this.auth.user.next(user); // todo body?
            localStorage.setItem('User', JSON.stringify(user))
            this.success = true; // todo necessary?
            this.router.navigate(['dashboard']).then();
          } catch (e) {
            console.log(e);
            this.errorMessage = "Sorry, we're having issue with the server.";
          }
        },
        (err) => {
          console.log(err); // todo remove
          // todo handle incorrect password
          // todo handle email in use
          this.errorMessage = "Sorry, we're having trouble logging you in.";
        }
      );
    }
  }

  // todo add first name
  // todo add last name
  // todo add hardware id + information on how to find it
  // todo pass in information to register
  register() {
    let getValue = (field: string) => this.registerForm.get('username').value;

    this.errorMessage = '';
    if (this.registerForm.valid) {
      this.auth
        .register(
          getValue('username'),
          getValue('password'),
          'hardware_id', // todo fix
          'joe', // todo fix
          'goldberg' // todo fix
        )
        .subscribe(
          (res) => {
            try {
              this.success = true;
              console.log(res); // todo remove
            } catch (e) {
              console.log(e); // todo remove
              this.errorMessage = "Sorry, we're having issue with the server.";
            }
          },
          (err) => {
            console.log(err); // todo remove
            this.errorMessage =
              "Sorry, we're having trouble creating your account.";
          }
        );
    }

    // todo send confirmation email
    // todo on confirmation page, tell user to login after confirming
    // todo contact us page?
  }
}
