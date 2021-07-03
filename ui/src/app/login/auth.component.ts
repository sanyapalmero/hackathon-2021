import { Component, OnInit } from '@angular/core';
import { FormControl, FormGroup, Validators } from "@angular/forms";
import { AuthService } from "./auth.service";
import { Router } from "@angular/router";

@Component({
  selector: 'app-auth',
  templateUrl: './auth.component.html',
  styleUrls: ['./auth.component.scss']
})
export class AuthComponent implements OnInit {
  loginForm = new FormGroup({
    username: new FormControl('root', Validators.required),
    password: new FormControl('rootroot', Validators.required),
  });

  constructor(
    private auth: AuthService,
    private router: Router,
  ) {
  }

  ngOnInit(): void {
  }

  login() {
    this.auth.login(this.loginForm.value).toPromise()
      .then(() => this.router.navigate(['/']));
  }

}
