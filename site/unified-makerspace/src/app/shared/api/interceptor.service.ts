import {Injectable} from '@angular/core';
import {HttpHandler, HttpInterceptor, HttpRequest} from '@angular/common/http';


@Injectable({
  providedIn: 'root',
})
export class InterceptorService implements HttpInterceptor{

  intercept(req: HttpRequest<any>, next: HttpHandler) {

    // todo also authenticate requests

    console.log(req.url, req);

    let jsonRequest = req.clone({
      headers: req.headers.append('Content-Type', 'application/json')
    })

    return next.handle(jsonRequest);
  }
}
