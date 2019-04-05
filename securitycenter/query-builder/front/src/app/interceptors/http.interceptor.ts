import { HttpClientModule, HTTP_INTERCEPTORS } from '@angular/common/http';

import { Injectable } from '@angular/core';

import {
    HttpRequest,
    HttpHandler,
    HttpEvent,
    HttpHeaders,
    HttpInterceptor,
    HttpErrorResponse,
  } from '@angular/common/http';

  import { Observable } from 'rxjs/Observable';
  import 'rxjs/add/observable/throw';
  import 'rxjs/add/operator/do';

@Injectable()
export class RequestInterceptor implements HttpInterceptor {

    intercept(request: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {
        // const customReq = request.clone();

        return next
        .handle(request)
        .do((event: HttpEvent<any>) => {}, (err: any) => {
            if (err instanceof HttpErrorResponse) {
                if (err.status === 0 || err.status === 401) {
                    throw new Error('Session Expired');
                }
            }
        });
    }
}
