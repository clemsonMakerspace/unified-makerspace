import { Component, OnInit } from '@angular/core';
import { FormControl, FormGroup, Validators } from '@angular/forms';
import { AuthService } from '../shared/auth/auth.service';
import { Router } from '@angular/router';
import * as majors from './majors.json';

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
  formSubmitted: boolean;
  success = false;
  majors = []

  ngOnInit(): void {

    // todo get params
    this.formType = this.router.url.split('/')[1];
    this.majors = majors['default'];


    // todo only for testing - remove when done
    this.loginForm = new FormGroup({
      email: new FormControl('joe@makerspace.com', Validators.required),
      password: new FormControl('password', Validators.required),
    });


    // todo validate majors

    // todo testing
    let nameRegex = "[a-zA-Z]+\ [a-zA-Z]+";
    this.registerForm = new FormGroup({
      name: new FormControl('joe goldberg', [Validators.required, Validators.pattern(nameRegex)]),
      major: new FormControl('literature', [Validators.required]),
      email: new FormControl('joe@makerspace.com', [Validators.required, Validators.email]),
      password: new FormControl('password', Validators.required),
      confirmPassword: new FormControl('password', Validators.required),
      isUser: new FormControl('')
    });
  }


  showError(field: string) {
    let f = this.registerForm.get(field);
    let error = ""
    if (f.dirty || this.formSubmitted) {
      if (f.invalid) {
        error = field + " is not valid."
      }
      if (f.value == '') {
        error = field + " is required."
      }
    }
    return error;
  }


  // todo change url instead?
  switchMode() {
    this.router
      .navigate([this.formType == 'login' ? 'register' : 'login'])
      .then();
  }

  // todo better password strength

  // todo show loading indicators....

  login() {
    // todo check for success
    // todo getValue?

    // todo move stuff to api service
    this.errorMessage = '';
    let email = this.loginForm.get('email').value;
    let password = this.loginForm.get('password').value;

    if (this.loginForm.valid) {
      this.auth.login(email, password).subscribe(
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
          // todo handle incorrect password
          // todo handle email in use
          this.errorMessage = "Sorry, we're having trouble logging you in.";
        }
      );
    }
  }

  // todo add hardware id + information on how to find it
  // todo pass in information to register
  // todo capitalize shit


  register() {
    this.formSubmitted = true;
    let getValue = (field: string) => this.registerForm.get(field).value;
    let name = getValue('name').split(' ')

    this.errorMessage = '';
    if (this.registerForm.valid) {
      this.auth
        .register(
          getValue('email'),
          getValue('password'),
          'hardware_id', // todo fix
          name[0],
          name[1]
        )
        .subscribe(
          (res) => {
            try {
              this.success = true;
            } catch (e) {
              this.errorMessage = "Sorry, we're having issue with the server.";
            }
          },
          (err) => {
            this.errorMessage =
              "Sorry, we're having trouble creating your account.";
          }
        );
    }

    // todo send confirmation email
    // todo on confirmation page, tell user to login after confirming
    // todo contact us page?
    // todo page to enter confirmation code
  }


  // todo implement
  handleError(err) {

  }



}
