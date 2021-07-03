import { Injectable } from '@angular/core';
import {
  HttpRequest,
  HttpHandler,
  HttpEvent,
  HttpInterceptor,
  HttpErrorResponse
} from '@angular/common/http';
import { Observable } from 'rxjs';
import { tap } from "rxjs/operators";
import { AuthService } from "./auth.service";
import { Router } from "@angular/router";
import { CookieService } from "ngx-cookie-service";

@Injectable()
export class AuthInterceptor implements HttpInterceptor {

  constructor(
    private auth: AuthService,
    private router: Router,
    private cookieService: CookieService
  ) {
  }

  intercept(request: HttpRequest<unknown>, next: HttpHandler): Observable<HttpEvent<unknown>> {
    const authReq = request.clone({
      setHeaders: {
        'Content-Type': 'application/json',
        'X-CSRFToken': this.cookieService.get('csrftoken')      }
    })

    return next.handle(authReq).pipe(
      tap(
        (event) => {
          // if (event instanceof HttpResponse)
          //   console.log('Server response')
        },
        (err) => {
          if (err instanceof HttpErrorResponse) {
            if (err.status == 401 || err.status == 403) {
              this.router.navigate(['login']);
              console.log('Unauthorized')
            }
          }
        }
      )
    )
  }
}
