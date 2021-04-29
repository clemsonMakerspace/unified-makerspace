import {Component, OnInit} from '@angular/core';
import {AbstractControl, FormBuilder, FormGroup, ValidationErrors, Validators} from '@angular/forms';
import {AuthService} from '../../shared/auth/auth.service';
import {Router} from '@angular/router';
import {showError, useTestData} from 'src/app/shared/funcs';
import {HttpErrorResponse} from '@angular/common/http';


/* ensures that userToken is entered if user */
function UserValidator(control: AbstractControl)
  : null | ValidationErrors {
    if (!!control.get('isUser').value) {
      if (!!control.get('userToken').value) {
        return null;
      }
      return {'token': true}
    }
}

function ConfirmPasswordValidator(control: AbstractControl):
  null | ValidationErrors {
  return control.get('confirmPassword').value === control.get('password').value
    ? null : {'confirmPassword': true};
}

@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.scss']
})
export class RegisterComponent implements OnInit {

  constructor(private fb: FormBuilder,
              private auth: AuthService,
              public router: Router) {
  }

  // todo are you sure you want to leave this page?


  registerForm: FormGroup;
  showError;

  get isUser() {
    return this.registerForm.get('isUser').value;
  }

  get state() {
    return this.auth.regState;
  }


  ngOnInit(): void {

    // enable user to register again
    if (this.auth.regState == 'success') {
      this.auth.regState = 'register';
    }

    this.registerForm = this.fb.group({
      firstName: ['', Validators.required],
      lastName: ['', Validators.required],
      email: ['', [Validators.required, Validators.email]],
      password: ['', [Validators.required, Validators.minLength(6)]],
      confirmPassword: ['', [Validators.required]],
      isUser: [''],
      userToken: ['']
    }, {
      validators: [UserValidator,
        ConfirmPasswordValidator]
    });


    this.showError = showError(this.registerForm);
    useTestData(this.registerForm, 'user');

  }

  onSubmit() {
    this.registerForm['submitted'] = true;
    this.registerForm['error'] = '';
    if (this.registerForm.valid) {
      if (this.isUser) {
        this.createUser(this.registerForm.value);
      } else {
        // save info so it can be used by next page
        this.auth.newUserInfo = this.registerForm.value;
        this.auth.regState = 'visitor';
      }
    }
  }


  createUser(arg: any) {
    this.auth
      .createUser(arg)
      .subscribe(
        (res) => {
          this.auth.regState = 'success';
        },
        (err) => {
          this.handleError(err);
        }
      );
  }

  handleError(err: HttpErrorResponse) {

    let error = 'Sorry, we\'re having trouble creating your account';
    if (err.status == 400) {
      error = 'This email is already in use!';
    } else if (err.status == 405) {
      error = 'This provided user token is invalid!';
    } else if (err.status == 406) {
      error = 'This provided user token is expired!';
    }
    this.registerForm['error'] = error;
  }


}
