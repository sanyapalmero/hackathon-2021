import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { DashboardComponent } from './dashboard.component';
import { DashboardService } from "./services/dashboard.service";
import { RouterModule, Routes } from "@angular/router";

const routes: Routes = [
  {
    path: "", component: DashboardComponent
  },
]

@NgModule({
  declarations: [
    DashboardComponent
  ],
  imports: [
    CommonModule,
    RouterModule.forChild(routes),
  ],
  providers: [
    DashboardService
  ]
})
export class DashboardModule { }
