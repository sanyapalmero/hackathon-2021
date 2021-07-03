import { Component, OnInit } from '@angular/core';
import { AuthService } from "../auth.service";
import { Router } from "@angular/router";

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss']
})
export class LoginComponent implements OnInit {
  user$ = this.auth.user$;

  constructor(public auth: AuthService,
              private router: Router) {
  }

  ngOnInit(): void {
  }

  logout() {
    this.auth.logout().toPromise()
      .then(() => this.router.navigate(['/login']));
  }

}
