import { Injectable } from '@angular/core';
import { HttpClient } from "@angular/common/http";
import { tap } from "rxjs/operators";
import { LocalStorage } from "../local-storage";
import { BehaviorSubject } from "rxjs";

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  public user$ = new BehaviorSubject(JSON.parse(<string>this.localStorage.getItem('user')));

  private url = 'api'

  constructor(private http: HttpClient,
              private localStorage: LocalStorage) {
  }

  login(value: any) {
    return this.http.post<User>(this.url + '/auth/login/', value).pipe(
      tap(value => {
        this.user$.next(value);
        this.localStorage.setItem('user', JSON.stringify(value));
      })
    );
  }

  logout() {
    return this.http.post(this.url + '/auth/logout/', {}).pipe(
      tap(() => {
        this.user$.next(null);
        this.localStorage.removeItem('user');
      })
    );
  }
}

interface User {
  id: string
  username: string,
}
