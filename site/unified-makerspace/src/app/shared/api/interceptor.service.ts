import {Injectable} from '@angular/core';
import {HttpHandler, HttpInterceptor, HttpRequest} from '@angular/common/http';
import {AuthService} from '../auth/auth.service';


@Injectable({
  providedIn: 'root',
})
export class InterceptorService implements HttpInterceptor{

  constructor(private auth: AuthService){}

  intercept(req: HttpRequest<any>, next: HttpHandler) {

    // todo also authenticate requests

    let request = req.clone({ // all outgoing requests are json
      headers: req.headers.append('Content-Type', 'application/json')
    })


    if (this.auth.isUserLoggedIn()) {
      request = request.clone({ // all outgoing requests are json
        headers: req.headers.append('Authorization', this.auth.user.getValue()['auth_token'])
      })
    }

    // todo remove this
    console.log(request);

    return next.handle(request);
  }
}
