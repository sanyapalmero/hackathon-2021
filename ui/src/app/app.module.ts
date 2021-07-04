import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { HttpClientModule, HTTP_INTERCEPTORS } from '@angular/common/http';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { AuthComponent } from './login/auth.component';
import { AuthService } from "./login/auth.service";
import { AuthInterceptor } from "./login/auth.interceptor";
import { ReactiveFormsModule } from "@angular/forms";
import { CookieService } from "ngx-cookie-service";
import { LoginComponent } from './login/login/login.component';
import { NavbarComponent } from './navbar/navbar.component';
import { AvatarModule } from "primeng/avatar";

@NgModule({
  declarations: [
    AppComponent,
    AuthComponent,
    LoginComponent,
    NavbarComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,
    ReactiveFormsModule,
    AvatarModule,
  ],
  providers: [
    AuthService,
    {
      provide: HTTP_INTERCEPTORS,
      useClass: AuthInterceptor,
      multi: true
    },
    CookieService
  ],
  bootstrap: [AppComponent]
})
export class AppModule {
}
