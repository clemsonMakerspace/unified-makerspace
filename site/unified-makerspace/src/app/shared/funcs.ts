import {FormGroup} from '@angular/forms';
import * as lodash from 'lodash';
import {environment} from '../../environments/environment';


/* returns a functional that handles common form errors */
export function showError(form: FormGroup) {
  return function err(field: string,
                      crossError=null) {

    // todo add comments

    let errorMap = {
      'length': '$ must be six digits.',
      'list': '$ is not in the list.',
      'required': '$ is required.',
      'minlength': '$ must be at least {requiredLength} characters.',
      'email': '@ is not a valid email.',
      'token': 'Token is required. Contact your administrator for assistance',
      'confirmPassword': 'Passwords do not match.'
    };

    let f = form.get(field);
    field = lodash.startCase(field);     // camel case to title case
    let error = '';
    if (f.touched || form['submitted']) {

      if (crossError) {
        if (form.errors && crossError in form.errors) {
          return errorMap[crossError];
        }
      }

      if (f.invalid) {
        let errorName = Object.keys(f.errors)[0];
        error = errorMap[errorName];
        if (!error) {
          error = field + ' is not valid.';
        } else {
          error = error.replace('@', f.value);
          error = error.replace('$', field);
          error = error.replace(/{([A-aZ-z]*)}/,
            (v, p1) => {
              return f.errors[errorName][p1];
            });
        }
      }

    }
    return error;
  };
}


/* fills form with test data */
export function useTestData(control: FormGroup, object: string) {
  if (!environment.production) {
    for (let [c, v] of Object.entries(control.controls)) {
      v.setValue(environment[object][c]);
    }
  }
}
