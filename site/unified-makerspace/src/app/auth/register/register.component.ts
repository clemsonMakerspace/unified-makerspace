import {Component, OnInit} from '@angular/core';
import {AbstractControl, FormBuilder, FormGroup, Validators} from '@angular/forms';
import {AuthService} from '../../shared/auth/auth.service';
import {Router} from '@angular/router';
import {showError} from 'src/app/shared/funcs';


/* ensures that userToken is entered if user */
export function UserValidator(control: AbstractControl)
  : any | null {
  return (!!control.get('isUser').value == !!control.get('userToken').value) ? null : {'error': true};
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

  // todo put this in separate file?
  testUser = {
    'firstName': 'joe',
    'lastName': 'goldberg',
    'email': 'joe@makerspace.com',
    'password': 'password',
    'confirmPassword': 'password',
    'isUser': false,
    'userToken': ''
  };

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
      this.auth.regState = 'register'; // todo change to start?
    }

    this.registerForm = this.fb.group({
      firstName: ['', Validators.required],
      lastName: ['', Validators.required],
      email: ['', [Validators.required, Validators.email]],
      password: ['', [Validators.required, Validators.minLength(6)]],
      confirmPassword: ['', Validators.required],
      isUser: [''],
      userToken: ['']
    }, UserValidator);


    this.showError = showError(this.registerForm);
    this.registerForm.setValue(this.testUser);

  }


  // todo add tool tips
  // todo userValidator not working?
  // todo stronger password (min length)
  // todo are you sure you want to leave this page?
  // todo min length -> error handling

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


  // todo update success page
  // todo on confirmation page, tell user to login after confirming
  // todo contact us page?

  createUser(arg: any) {
    this.auth
      .createUser(arg)
      .subscribe(
        // ignore response
        (res) => this.auth.regState = 'success',
        (err) => {
          this.registerForm['error'] =
            'Sorry, we\'re having trouble creating your account.';
        }
      );
  }

  // todo possible failures:
  // todo incorrect password
  // todo email in use


}
