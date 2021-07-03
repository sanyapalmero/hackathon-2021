import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { HttpClientModule, HTTP_INTERCEPTORS } from '@angular/common/http';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { TuiButtonModule, TuiLinkModule, TuiRootModule } from "@taiga-ui/core";
import { AuthComponent } from './login/auth.component';
import { AuthService } from "./login/auth.service";
import { AuthInterceptor } from "./login/auth.interceptor";
import { ReactiveFormsModule } from "@angular/forms";
import { TuiAvatarModule, TuiInputModule, TuiInputPasswordModule, TuiIslandModule } from "@taiga-ui/kit";
import { CookieService } from "ngx-cookie-service";
import { LoginComponent } from './login/login/login.component';
import { NavbarComponent } from './navbar/navbar.component';

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
    TuiRootModule,
    ReactiveFormsModule,
    TuiInputModule,
    TuiInputPasswordModule,
    TuiIslandModule,
    TuiButtonModule,
    TuiAvatarModule,
    TuiLinkModule
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
