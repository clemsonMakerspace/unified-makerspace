import { Component, OnInit } from '@angular/core';
import {AbstractControl, FormBuilder, FormControl, FormGroup, ValidationErrors, ValidatorFn, Validators} from '@angular/forms';
import { AuthService } from '../shared/auth/auth.service';
import { Router } from '@angular/router';
import * as majors from './majors.json';
import get = Reflect.get;


export function UserValidator(control: AbstractControl)
  : any | null {
  return   (!!control.get('isUser').value == !!control.get('userToken').value) ? null : {'error': true};
}


// todo remove later
export function getFormValidationErrors(form: FormGroup) {

  const result = [];
  Object.keys(form.controls).forEach(key => {

    const controlErrors: ValidationErrors = form.get(key).errors;
    if (controlErrors) {
      Object.keys(controlErrors).forEach(keyError => {
        result.push({
          'control': key,
          'error': keyError,
          'value': controlErrors[keyError]
        });
      });
    }
  });

  return result;
}

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss'],
})
export class LoginComponent implements OnInit {
  constructor(private auth: AuthService,
              private router: Router,
              private fb: FormBuilder) {}

  loginForm: FormGroup;
  registerForm: FormGroup;
  visitorForm: FormGroup;

  formType = 'login'; // either 'login' or 'register'
  errorMessage: string;
  formSubmitted: boolean;
  success = false;
  majors = []


  registerMode = 0;
  showVisitorForm = false;

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
      email: new FormControl('joe@makerspace.com', [Validators.required, Validators.email]),
      password: new FormControl('password', Validators.required),
      confirmPassword: new FormControl('password', Validators.required),
      isUser: new FormControl(''),
      userToken: new FormControl(''),
    }, UserValidator);


    this.visitorForm = this.fb.group({
      major: ['', Validators.required],
      degree: ['', Validators.required],
      hardwareId: ['', Validators.required]
    })
  }

  showError(field: string) {
    let f = this.registerForm.get(field);
    let error = "";
    if (f.touched || this.formSubmitted) {
      if (f.invalid) {
        error = field + " is not valid."
        if (f.value == '') {
          error = field + " is required."
        }
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

  // todo capitalize shit


  // [ngClass]="{'disabled': registerForm.invalid}"

  register() {
    this.formSubmitted = true;
    this.errorMessage = '';
    let getValue = (field: string) => this.registerForm.get(field).value;
    let name = getValue('name').split(' ')
    let email = getValue('email');
    let password = getValue('password');

      if (this.registerForm.valid) {
      if (getValue('isUser')) {
        this.createUser(
          email,
          password,
          name[0],
          name[1],
          getValue('userToken')
        );
      } else {
        this.showVisitorForm = true;
      }
    }

    // todo send confirmation email
    // todo on confirmation page, tell user to login after confirming
    // todo contact us page?
    // todo page to enter confirmation code
  }



  // todo implement

  createUser(email, password, firstName, lastName, userToken) {
    this.auth
      .createUser(
        email,
        password,
        firstName,
        lastName,
        userToken
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
      )
  }


  // todo implement
  handleError(err) {

  }



}
